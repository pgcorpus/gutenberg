"""
Process counts for all PG data.

Written by
M. Gerlach and F. Font-Clos

"""
import os
from os.path import join
import argparse
import glob
import ast
import pandas as pd
import concurrent.futures
import io
import re

from src.pipeline import process_book
from src.utils import get_langs_dict, check_not_empty, is_win32


if __name__ == '__main__':
    from src.tokenizer import nltk_dir
    import nltk
    nltk.download("punkt", nltk_dir) # avoid lookup error

    parser = argparse.ArgumentParser(
        "Processing raw texts from Project Gutenberg:"
        " i) removing headers,ii) tokenizing, and iii) counting words.")
    # raw folder
    parser.add_argument(
        "-r", "--raw",
        help="Path to the raw-folder",
        default='data/raw/',
        type=str)
    # text folder
    parser.add_argument(
        "-ote", "--output_text",
        help="Path to text-output (text_dir)",
        default='data/text/',
        type=str)
    # tokens folder
    parser.add_argument(
        "-oto", "--output_tokens",
        help="Path to tokens-output (tokens_dir)",
        default='data/tokens/',
        type=str)
    # counts folder
    parser.add_argument(
        "-oco", "--output_counts",
        help="Path to counts-output (counts_dir)",
        default='data/counts/',
        type=str)
    # pattern to specify subset of books
    parser.add_argument(
        "-p", "--pattern",
        help="Pattern to specify a subset of books",
        default='*',
        type=str)

    # quiet argument, to supress info
    parser.add_argument(
        "-q", "--quiet",
        action="store_true",
        help="Quiet mode, do not print info, warnings, etc"
    )

    # log file
    parser.add_argument(
        "-l", "--log_file",
        help="Path to log file",
        default=".log",
        type=str)
    
    # check if existing files are empty
    parser.add_argument(
        "-c", "--check_empty",
        action="store_true",
        help="Whether to check if existing files are empty")
    
    # whether to ignore UTF-8 decoding errors
    parser.add_argument(
        "--ignore",
        action="store_true",
        help="Whether to ignore UTF-8 decoding errors")
    
    # multi-threading/processing choice
    parser.add_argument(
        "--pool",
        help="Whether to use multi-processing or multi-threading",
        default="process",
        choices=["process", "thread"],
        type=str)

    # add arguments to parser
    args = parser.parse_args()
    raw_dir, text_dir, tokens_dir, counts_dir = args.raw, args.output_text, args.output_tokens, args.output_counts
    
    if is_win32:
        print("Windows detected")
        raw_dir = raw_dir.replace('/', '\\')
        text_dir = text_dir.replace('/', '\\')
        tokens_dir = tokens_dir.replace('/', '\\')
        counts_dir = counts_dir.replace('/', '\\')

    # check whether the out-put directories exist
    if os.path.isdir(text_dir) is False:
        raise ValueError("The directory for output of texts '%s' "
                         "does not exist" % (text_dir))
    if os.path.isdir(tokens_dir) is False:
        raise ValueError("The directory for output of tokens '%s' "
                         "does not exist" % (tokens_dir))
    if os.path.isdir(counts_dir) is False:
        raise ValueError("The directory for output of counts '%s' "
                         "does not exist" % (counts_dir))

    # load metadata
    metadata = pd.read_csv("metadata/metadata.csv").set_index("id")

    # load languages dict
    langs_dict = get_langs_dict()

    # loop over all books in the raw-folder
    pbooks = 0

    # find out which jobs were already done
    re_pattern = args.pattern.replace('*', '.*') # wild card roughly equals .* in regex
    pattern_text = re.compile('(PG%s)_text.txt' % (re_pattern))
    pattern_tokens = re.compile('(PG%s)_tokens.txt' % (re_pattern))
    pattern_counts = re.compile('(PG%s)_counts.txt' % (re_pattern))
    exist_text = {pattern_text.fullmatch(f) for f in 
                  glob.glob('PG%s_text.txt' % (args.pattern), root_dir=text_dir)}
    exist_tokens = {pattern_tokens.fullmatch(f) for f in 
                    glob.glob('PG%s_tokens.txt' % (args.pattern), root_dir=tokens_dir)}
    exist_counts = {pattern_counts.fullmatch(f) for f in 
                    glob.glob('PG%s_counts.txt' % (args.pattern), root_dir=counts_dir)}
    
    exist_text = {f.group(1) for f in exist_text if f}
    exist_tokens = {f.group(1) for f in exist_tokens if f}
    exist_counts = {f.group(1) for f in exist_counts if f}
    done_jobs = exist_text & exist_tokens & exist_counts
    del exist_text, exist_tokens, exist_counts

    if args.check_empty:
        with eval("concurrent.futures.%sPoolExecutor()" % args.pool.capitalize()) as pool:
            tmp0 = [(os.path.join(text_dir, PG_id) + "_text.txt", PG_id) for PG_id in done_jobs]
            tmp1 = [(os.path.join(tokens_dir, PG_id) + "_tokens.txt", PG_id) for PG_id in done_jobs]
            tmp2 = [(os.path.join(counts_dir, PG_id) + "_counts.txt", PG_id) for PG_id in done_jobs]
            validate_jobs0 = {pool.submit(check_not_empty, f) : PG_id for f, PG_id in tmp0}
            validate_jobs1 = {pool.submit(check_not_empty, f) : PG_id for f, PG_id in tmp1}
            validate_jobs2 = {pool.submit(check_not_empty, f) : PG_id for f, PG_id in tmp2}
            validation_results = {PG_id : 0 for PG_id in done_jobs}
            if not args.quiet:
                print("%d books to check for completion (3 passes required)" % len(done_jobs))
            for job_type in [validate_jobs0, validate_jobs1, validate_jobs2]:
                pbooks = 0
                for job in concurrent.futures.as_completed(job_type):
                    if job.result():
                        validation_results[job_type[job]] += 1
                    pbooks += 1
                    if (not args.quiet) and (pbooks % 100 == 0):
                        print("%6d books checked for completion" % pbooks, end="\r")
            done_jobs = {PG_id for PG_id in validation_results if validation_results[PG_id] == 3}
            if not args.quiet:
                print("%d books seem to be processed but have empty file(s)" %(len(validation_results) - len(done_jobs)))
            del tmp0, tmp1, tmp2, validate_jobs0, validate_jobs1, validate_jobs2, validation_results

    with eval("concurrent.futures.%sPoolExecutor()" % args.pool.capitalize()) as pool:
        book_process_jobs = dict()
        for filename in glob.glob(join(raw_dir, 'PG%s_raw.txt' % (args.pattern))):
            # The process_books function will fail very rarely, whne
            # a file tagged as UTf-8 is not really UTF-8. We kust
            # skip those books.
            # get PG_id
            PG_id = os.path.split(filename)[-1].split("_")[0]

            if PG_id not in done_jobs:
                # get language from metadata
                # default is english
                language = "english"
                try:
                    # language is a string representing a list of languages codes
                    lang_id = ast.literal_eval(metadata.loc[PG_id, "language"])[0]
                    if lang_id in langs_dict.keys():
                        language = langs_dict[lang_id]
                except KeyError:
                    if not args.quiet:
                        msg = "# WARNING: metadata for '%s' not found" % filename
                        print(msg)
                        if args.log_file:
                            with io.open(args.log_file, "a") as f:
                                f.write(msg + '\n')

                # process the book: strip headers, tokenize, count
                book_process_jobs[
                    pool.submit(
                        process_book,
                        path_to_raw_file=filename,
                        text_dir=text_dir,
                        tokens_dir=tokens_dir,
                        counts_dir=counts_dir,
                        overwrite_all=True,
                        language=language,
                        log_file=args.log_file,
                        ignore=args.ignore)
                ] = PG_id
        
            pbooks += 1
            if not args.quiet:
                print("%d book processing jobs started..." % pbooks, end="\r")
        
        print("\n%d book processing jobs created in total" % len(book_process_jobs))

        pbooks = 0
        for job in concurrent.futures.as_completed(book_process_jobs):
            PG_id = book_process_jobs[job]
            if args.log_file:
                try:
                    log_content = job.result()
                    with io.open(args.log_file, "a") as f:
                        f.write(log_content)
                except UnicodeDecodeError:
                    if not args.quiet:
                        print("# WARNING: cannot process '%s' (encoding not UTF-8)" % PG_id)
                except LookupError as e:
                    print("Very likely that an NLTK resource needs to be downloaded")
                    raise e
                except Exception as e:
                    if not args.quiet:
                        print("# WARNING: cannot process '%s' (unkown error)" % PG_id)
                        raise e
            pbooks += 1
            if not args.quiet:
                print("Processed %d books..." % pbooks, end="\r")
        print("\ndone")
