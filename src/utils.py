# -*- coding: utf-8 -*-
import os
import shutil
import subprocess


def get_PG_number(string):
    """
    Simply gets the PG number from different possible text files.
    Patterns are: 12345-0.txt or 12345.txt.utf-8 or pg12345.txt.utf8
    """
    # 12345-0.txt
    if string.find("-0.txt")>-1:
        PG_number = string.replace("-0.txt","")

    # no files match this!
    # # 12345.txt.utf-8
    # elif string.find(".txt.utf-8")>-1:
    #     PG_number =  string.replace(".txt.utf-8","")

    # pg12345.txt.utf8
    elif string.find(".txt.utf8")>-1:
            PG_number =  string.replace(".txt.utf8","").replace("pg","")

    assert PG_number.isnumeric()
    return PG_number



def erase_duplicates_in_mirror(
    mirror_dir = None,
    ):
    """
    Look for duplicates in 'mirror_dir', and delete them.
    Typical case is, there's two files corresponding to the
    same PG identificator:

    1) mirror/1/2/3/4/12345/12345-0.txt
    2) mirror/cache/epub/12345/pg12345.txt.utf-8

    We keep 1) and delete 2)
    """
    for dirName, subdirList, fileList in os.walk(mirror_dir):
        for fname in fileList:
            if len(fname.split("-"))<=2 and (fname[-6::]=="-0.txt"):
                PGnumber = get_PG_number(fname)
                possible_duplicate = os.path.join(mirror_dir,"cache","epub",PGnumber,"pg"+PGnumber+".txt.utf8")
                if os.path.isfile(possible_duplicate):
                    print("# WARNING:","PG"+str(PGnumber),"found twice, cache version deleted.")
                    os.remove(possible_duplicate)


def populate_raw_from_mirror(
    mirror_dir = None,
    raw_dir = None,
    overwrite = False
    ):
    """
    Populate the raw/ directory using the mirror/ directory.

    This function traverses 'mirror_dir' and copies all .txt files
    into 'raw_dir'. Notice it also adds the "PG" suffix.

    It ignores files with more than one dash (strange files)
    and those not in UTF-8 encoding (not ending in -0.txt).

    Parameters
    ----------
    overwrite : bool
        Whether to overwrite files in raw.

    """
    for dirName, subdirList, fileList in os.walk(mirror_dir):
        for fname in fileList:
            # ignore strange files and file not in UTF8
            # patterns to match are 12345-0.txt or pg12345.txt.utf8
            if len(fname.split("-"))<=2 and (fname[-6::]=="-0.txt" or fname[-9::]==".txt.utf8"):
                # get PG number
                PGnumber = get_PG_number(fname)

                
                
                source = os.path.join(dirName,fname)
                target = os.path.join(raw_dir,"PG"+PGnumber+"_raw.txt")
                
                if os.path.isfile(target):
                    print("# WARNING:",target,"already exists!")
                    print("# current source: ",source)
                if (not os.path.isfile(target)) or overwrite:
                    subprocess.call(["ln","-f",source,target])
