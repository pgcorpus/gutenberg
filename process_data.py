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

from src.pipeline import process_book
from src.utils import get_langs_dict, is_win32


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
    
    with concurrent.futures.ProcessPoolExecutor() as pool:
        book_process_jobs = []
        for filename in glob.glob(join(raw_dir, 'PG%s_raw.txt' % (args.pattern))):
            # The process_books function will fail very rarely, whne
            # a file tagged as UTf-8 is not really UTF-8. We kust
            # skip those books.
            # get PG_id
            PG_id = os.path.split(filename)[-1].split("_")[0]

            # get language from metadata
            # default is english
            language = "english"
            # language is a string representing a list of languages codes
            lang_id = ast.literal_eval(metadata.loc[PG_id, "language"])[0]
            if lang_id in langs_dict.keys():
                language = langs_dict[lang_id]

            # process the book: strip headers, tokenize, count
            book_process_jobs.append(pool.submit(
                process_book,
                path_to_raw_file=filename,
                text_dir=text_dir,
                tokens_dir=tokens_dir,
                counts_dir=counts_dir,
                language=language,
                log_file=args.log_file))
            
            pbooks += 1
            if not args.quiet:
                print("%d book processing jobs started..." % pbooks, end="\r")
        
        print()
        pbooks = 0
        for job in concurrent.futures.as_completed(book_process_jobs):
            if args.log_file:
                try:
                    log_content = job.result()
                    with io.open(args.log_file, "a") as f:
                        f.write(log_content)
                except UnicodeDecodeError:
                    if not args.quiet:
                        print("# WARNING: cannot process '%s' (encoding not UTF-8)" % filename)
                except KeyError:
                    if not args.quiet:
                        print("# WARNING: metadata for '%s' not found" % filename)
                except LookupError as e:
                    print("Very likely that an NLTK resource needs to be downloaded")
                    raise e
                except Exception as e:
                    if not args.quiet:
                        print("# WARNING: cannot process '%s' (unkown error)" % filename)
                        raise e
            pbooks += 1
            if not args.quiet:
                print("Processed %d books..." % pbooks, end="\r")
            
