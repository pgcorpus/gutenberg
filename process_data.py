import os,sys,argparse
import glob

sys.path.append("src/")
from pipeline import process_book

if __name__=='__main__':

    parser = argparse.ArgumentParser(
        "Processing raw texts from Project Gutenberg:"\
        " i) removing headers,ii) tokenizing, and iii) counting words.")
    ## raw folder
    parser.add_argument(
        "-r", "--raw",
        help="Path to the raw-folder",
        default='data/raw/',
        type=str)
    ## text folder
    parser.add_argument(
        "-ote", "--output_text",
        help="Path to text-output (text_dir)",
        default='data/text/',
        type=str)
    ## tokens folder
    parser.add_argument(
        "-oto", "--output_tokens",
        help="Path to tokens-output (tokens_dir)",
        default='data/tokens/',
        type=str)
    ## counts folder
    parser.add_argument(
        "-oco", "--output_counts",
        help="Path to counts-output (counts_dir)",
        default='data/counts/',
        type=str)
    ## pattern to specify subset of books
    parser.add_argument(
        "-p", "--pattern",
        help="Patttern to specify a subset of books",
        default='*',
        type=str)

    # quiet argument, to supress info
    parser.add_argument("-q","--quiet",
        action="store_true",
        help="Quiet mode, do not print info, warnings, etc"
        )

    ## add arguments to parser
    args = parser.parse_args()

    ## check whether the out-put directories exist
    if os.path.isdir(args.output_text) == False:
        raise ValueError("The directory for output of texts '%s' does not exist"%(args.output_text))
    if os.path.isdir(args.output_tokens) == False:
        raise ValueError("The directory for output of tokens '%s' does not exist"%(args.output_tokens))
    if os.path.isdir(args.output_counts) == False:
        raise ValueError("The directory for output of counts '%s' does not exist"%(args.output_counts))

    ## loop over all books in the raw-folder
    pbooks=0 
    for filename in glob.iglob( os.path.join( args.raw,'PG%s_raw.txt'%(args.pattern) ) ):
        # The process_books function will fail very rarely, whne
        # a file tagged as UTf-8 is not really UTF-8. We kust 
        # skip those books.  
        try:
            # process the book: strip headers, tokenize, count
            process_book(
                path_to_raw_file=filename,
                text_dir=args.output_text,
                tokens_dir=args.output_tokens,
                counts_dir=args.output_counts
                )
            pbooks += 1
            if not args.quiet:
                print("Processed %d books..."%pbooks,end="\r")
        except:
            if not args.quiet:
                print("# WARNING: cannot process '%s'"%filename)
