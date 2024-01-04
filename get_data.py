"""
Project Gutenberg parsing with python 3.

Written by
M. Gerlach & F. Font-Clos

"""
from src.utils import populate_raw_from_mirror, list_duplicates_in_mirror, remove_empty_dirs, is_win32
from src.metadataparser import make_df_metadata
from src.bookshelves import get_bookshelves
from src.bookshelves import parse_bookshelves

import argparse
import os
import subprocess
import pickle

if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        "Update local PG repository.\n\n"
        "This script will download all books currently not in your\n"
        "local copy of PG and get the latest version of the metadata.\n"
        )
    
    # mirror dir
    parser.add_argument(
        "-m", "--mirror",
        help="Path to the mirror folder that will be updated via rsync.",
        default='data/.mirror/',
        type=str)

    # raw dir
    parser.add_argument(
        "-r", "--raw",
        help="Path to the raw folder.",
        default='data/raw/',
        type=str)

    # metadata dir
    parser.add_argument(
        "-M", "--metadata",
        help="Path to the metadata folder.",
        default='metadata/',
        type=str)

    # pattern matching
    parser.add_argument(
        "-p", "--pattern",
        help="Patterns to get only a subset of books.",
        default='*',
        type=str)

    # update argument
    parser.add_argument(
        "-k", "--keep_rdf",
        action="store_false",
        help="If there is an RDF file in metadata dir, do not overwrite it.")

    # update argument
    parser.add_argument(
        "-owr", "--overwrite_raw",
        action="store_true",
        help="Overwrite files in raw.")

    # quiet argument, to supress info
    parser.add_argument(
        "-q", "--quiet",
        action="store_true",
        help="Quiet mode, do not print info, warnings, etc"
        )
    
    # clean argument, to supress info
    parser.add_argument(
        "-c", "--clean",
        action="store_true",
        help="Clean the mirror directory to remove any empty folders"
        )
    
    # rsync command
    parser.add_argument(
        "--rsync",
        help="Specify an alternative rsync command",
        default='rsync',
        type=str)
    
    # rsync command
    parser.add_argument(
        "--procedures",
        help='''Procedures to go through, defaults to \"pdlmb\": 
        - [p]ull mirror files
        - find [d]uplicates
        - hard [l]ink from mirror to raw
        - get [m]etadata
        - get [b]ookshelf information''',
        default='pdlmb',
        type=str)

    # create the parser
    args = parser.parse_args()
    mirror_dir, raw_dir, metadata_dir = args.mirror, args.raw, args.metadata
    
    if is_win32:
        print("Windows detected, please make sure wget is installed and added to PATH")
        mirror_dir = mirror_dir.replace('/', '\\')
        raw_dir = raw_dir.replace('/', '\\')
        metadata_dir = metadata_dir.replace('/', '\\')

    # check that all dirs exist
    if not os.path.isdir(mirror_dir):
        raise ValueError("The specified mirror directory does not exist.")
    if not os.path.isdir(raw_dir):
        raise ValueError("The specified raw directory does not exist.")
    if not os.path.isdir(metadata_dir):
        raise ValueError("The specified metadata directory does not exist.")

    # Update the .mirror directory via rsync
    # --------------------------------------
    # We sync the 'mirror_dir' with PG's site via rsync
    # The matching pattern, explained below, should match
    # only UTF-8 files.

    # pass the -v flag to rsync if not in quiet mode
    if args.quiet:
        vstring = ""
    else:
        vstring = "v"

    # Pattern to match the +  but not the - :
    #
    # + 12345 .   t   x  t .            utf  8
    # - 12345 .   t   x  t .      utf8 .gzi  p
    # + 12345 -   0   .  t x                 t 
    #---------------------------------------------
    #        [.-][t0][x.]t[x.]    *         [t8]
    includes = ["*/", "[p123456789][g0123456789]%s[.-][t0][x.]t[x.]*[t8]" % args.pattern]
    excludes = ["*"]
    sp_args = ' '.join([args.rsync, "-am%s" % vstring] + ["--include=\"%s\"" % i for i in includes] + \
        ["--exclude=\"%s\"" % i for i in excludes] + ["aleph.gutenberg.org::gutenberg", mirror_dir])
    
    # If specified, remove any empty directory that might be caused by bugs or wrong patterns in rsync
    if args.clean:
        remove_empty_dirs(mirror_dir, args.quiet)

    # Subprocess call (default arguments):
    # rsync -amv --include="*/" --include="[p123456789][g0123456789]*[.-][t0][x.]t[x.]*[t8]" --exclude="*" aleph.gutenberg.org::gutenberg data/.mirror/
    if 'p' in args.procedures:
        subprocess.call(sp_args) 

    # Get rid of duplicates
    # ---------------------
    # A very small portion of books are stored more than
    # once in PG's site. We keep the newest one, see
    # erase_duplicates_in_mirror docstring.
    dups_list = list_duplicates_in_mirror(mirror_dir=mirror_dir) if 'd' in args.procedures else []

    # Populate raw from mirror
    # ------------------------
    # We populate 'raw_dir' hardlinking to
    # the hidden 'mirror_dir'. Names are standarized
    # into PG12345_raw.txt form.
    if 'l' in args.procedures:
        populate_raw_from_mirror(
            mirror_dir=mirror_dir,
            raw_dir=raw_dir,
            overwrite=args.overwrite_raw,
            dups_list=dups_list,
            quiet=args.quiet
        )

    # Update metadata
    # ---------------
    # By default, update the whole metadata csv
    # file each time new data is downloaded.
    if 'm' in args.procedures:
        make_df_metadata(
            path_xml=os.path.join(metadata_dir, 'rdf-files.tar.bz2'),
            path_out=os.path.join(metadata_dir, 'metadata.csv'),
            update=args.keep_rdf
        )

    # Bookshelves
    # -----------
    # Get bookshelves and their respective books and titles as dicts
    if 'b' in args.procedures:
        get_bookshelves()
        BS_dict, BS_num_to_category_str_dict = parse_bookshelves()
        with open("metadata/bookshelves_ebooks_dict.pkl", 'wb') as fp:
            pickle.dump(BS_dict, fp)
        with open("metadata/bookshelves_categories_dict.pkl", 'wb') as fp:
            pickle.dump(BS_num_to_category_str_dict, fp)