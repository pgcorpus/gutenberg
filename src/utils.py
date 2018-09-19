# -*- coding: utf-8 -*-
import os
import shutil
import subprocess
import glob

def get_langs_dict():
    """
    A dictionary mapping languages codes to full languages names
    """
    langs_dict = {
        "cs": "czech",
        "da": "danish",
        "nl": "dutch",
        "en": "english",
        "et": "estonian",
        "fi": "finnish",
        "fr": "french",
        "de": "german",
        "el": "greek",
        "it": "italian",
        "no": "norwegian",
        "pl": "polish",
        "pt": "portuguese",
        "sl": "slovene",
        "es": "spanish",
        "sv": "swedish"
    }
    return langs_dict

def get_PG_number(string):
    """
    Simply gets the PG number from different possible text files.
    Patterns are: 12345-0.txt or pg12345.txt.utf8
    """
    # 12345-0.txt
    if string.find("-0.txt")>-1:
        PG_number = string.replace("-0.txt","")

    # pg12345.txt.utf8
    elif string.find(".txt.utf8")>-1:
            PG_number =  string.replace(".txt.utf8","").replace("pg","")

    if not PG_number.isnumeric():
        print(string)
        print(PG_number,"\n")
        assert PG_number.isnumeric()
    return PG_number


def list_duplicates_in_mirror(
    mirror_dir = None,
    ):
    """
    Look for duplicates in 'mirror_dir', and list them.
    Typical case is, there's two files corresponding to the
    same PG identificator:

    1) mirror/1/2/3/4/12345/12345-0.txt
    2) mirror/cache/epub/12345/pg12345.txt.utf-8

    We populate 1) and list 2) as a duplicate
    """
    dups_list = []
    for dirName, subdirList, fileList in os.walk(mirror_dir):
        for matchpath in glob.iglob(os.path.join(dirName,"*-0.txt")):
            fname = matchpath.split("/")[-1]
            # fname must have exactly one "." and one "-"
            if (len(fname.split("."))==2 and len(fname.split("-"))==2):
                PGnumber = get_PG_number(fname)
                possible_duplicate = os.path.join(mirror_dir,"cache","epub",PGnumber,"pg"+PGnumber+".txt.utf8")
                if os.path.isfile(possible_duplicate):
                    dups_list.append(possible_duplicate)
    return dups_list


def populate_raw_from_mirror(mirror_dir=None,
                             raw_dir=None,
                             overwrite=False,
                             dups_list=None,
                             quiet=False):
    """
    Populate the raw/ directory using the .mirror/ directory.

    This function traverses 'mirror_dir' and copies all .txt files
    into 'raw_dir'. Notice it also adds the "PG" suffix.

    It ignores files with more than one dash (strange files)
    and those not in UTF-8 encoding (not ending in -0.txt).

    Parameters
    ----------
    overwrite : bool
        Whether to overwrite files in raw.
    dups_list :  list of strings
        A list of duplicates produced by list_duplicates_in_mirror.
        Files in this list are not copied into raw.

    """
    for dirName, subdirList, fileList in os.walk(mirror_dir):
        # patterns to match are 12345-0.txt or pg12345.txt.utf8
        for matchpath in glob.iglob(os.path.join(dirName, "[p123456789][g0123456789][0-9]*")):
            fname = matchpath.split("/")[-1]
            # check that file is not in dups_list
            if matchpath not in dups_list:
                # avoid files with more "." or "-" than expected
                if (len(fname.split("."))==2 and len(fname.split("-"))==2 and fname[-6::]=="-0.txt")\
                or (len(fname.split("."))==3 and len(fname.split("-"))==1 and fname[-9::]==".txt.utf8"):
                    # get PG number
                    PGnumber = get_PG_number(fname)

                    source = os.path.join(dirName, fname)
                    target = os.path.join(raw_dir, "PG"+PGnumber+"_raw.txt")

                    if (not os.path.isfile(target)) or overwrite:
                        subprocess.call(["ln", "-f", source, target])

            # if file was not in dupes list and we are not quiet
            elif not quiet:
                print("# WARNING: file %s skipped due to duplication" % fname)



