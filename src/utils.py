# -*- coding: utf-8 -*-
import os
import shutil

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
            if len(fname.split("-"))==2 and fname[-6::]=="-0.txt" :
                # get PG number
                PGnumber = fname.split("-")[0]

                # copy files
                source = os.path.join(dirName,fname)
                target = os.path.join(raw_dir,"PG"+PGnumber+"_raw.txt")
                
                # DETECT ENCODING
                
                if not os.path.isfile(target) or overwrite:
                    shutil.copy2(source,target)