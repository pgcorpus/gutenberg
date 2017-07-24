# -*- coding: utf-8 -*-
import os
import shutil


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

def populate_raw_from_mirror(
    mirror_dir = "../data/mirror/",
    raw_dir = "../data/raw/",
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

                # copy files
                source = os.path.join(dirName,fname)
                target = os.path.join(raw_dir,"PG"+PGnumber+"_raw.txt")
                
                # DETECT ENCODING
                if os.path.isfile(target):
                    print("# WARNING: '%s' already exists!",target)
                    print("# current source: '%s'",source)
                if (not os.path.isfile(target)) or overwrite:
                    shutil.copy2(source,target)
