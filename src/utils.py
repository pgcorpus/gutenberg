# -*- coding: utf-8 -*-

import re

NUMBER_RE = re.compile(r'\d+')

def get_langs_dict():
    """
    A dictionary mapping language codes to full language names
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

def get_PG_number(file):
    """
    Simply gets the PG number from different possible text files.
    Patterns are: 12345-0.txt or pg12345.txt.utf8
    """
    # stem removes only one ending, second is always '.txt'
    PG_number = NUMBER_RE.search(file.stem)
    assert PG_number is not None, file + "\n" + PG_number
    return PG_number.group()


def list_duplicates_in_mirror(mirror_dir):
    """
    Look for duplicates in 'mirror_dir', and list them.
    Typical case is, there's two files corresponding to the
    same PG identifier:

    1) mirror/1/2/3/4/12345/12345-0.txt
    2) mirror/cache/epub/12345/pg12345.txt.utf-8

    We populate 1) and list 2) as a duplicate
    """
    dups_list = []
    for file in mirror_dir.rglob("*-0.txt"):
        # file.name must have exactly one "." and one "-"
        if (file.name.count(".") == 1 and file.name.count("-") == 1):
            PGnumber = get_PG_number(file)
            possible_duplicate = mirror_dir / "cache" / "epub" / PGnumber / ("pg"+PGnumber+".txt.utf8")
            if possible_duplicate.is_file():
                dups_list.append(possible_duplicate)
    return dups_list


def populate_raw_from_mirror(mirror_dir,
                             raw_dir,
                             dups_list,
                             overwrite=False,
                             quiet=False):
    """
    Populate the raw/ directory using the .mirror/ directory.

    This function traverses 'mirror_dir' and copies all .txt files
    into 'raw_dir'. Notice it also adds the "PG" suffix.

    It ignores files with more than one dash (strange files)
    and those not in UTF-8 encoding (not ending in -0.txt).

    Parameters
    ----------
    mirror_dir : pathlib.Path
    raw_dir : pathlib.Path
    overwrite : bool
        Whether to overwrite files in raw.
    dups_list : list of strings
        A list of duplicates produced by list_duplicates_in_mirror.
        Files in this list are not copied into raw.

    """
    # patterns to match are 12345-0.txt or pg12345.txt.utf8
    for file in mirror_dir.rglob("[p1-9][g0-9][0-9]*.txt"):
        # check that file is not in dups_list
        if file not in dups_list:
            # avoid files with more "." or "-" than expected
            if (file.name.count(".")==1 and file.name.count("-")==1) \
            or (file.name.count(".")==2 and file.name.count("-")==0):
                PGnumber = get_PG_number(file)
                target = raw_dir / ("PG" + PGnumber + "_raw.txt")
                if overwrite or not target.is_file():
                    target.hardlink_to(file)

        # if file was not in dupes list and we are not quiet
        elif not quiet:
            print("# WARNING: file %s skipped due to duplication" % file.name)
