# -*- coding: utf-8 -*-
"""Functions to download, parse and filter Gutenberg's bookshelves."""

import os
import glob
import numpy as np
import pandas as pd
import lxml.html
import subprocess
import shutil
from .utils import is_win32

def rm_dir(*args):
    subprocess.call(["rm", "-rf"] + args)

if is_win32:
    rm_dir = shutil.rmtree
    def rm_pattern(path):
        for file in glob.glob(path.replace('/', os.path.sep)):
            os.remove(file)
else:
    rm_pattern = rm_dir

def get_bookshelves():
    """
    Scrap the bookshelves data from gutenbergs wiki.

    This function uses `wget` to scrap all the html
    files corresponding to a bookshelves. The html files
    are stored in `metadata/bookshelves`.

    """
    sp_args = ["wget",
               "--random-wait", "-r",
               "--no-parent", 
               "-e", "robots=off", 
               "-U", "mozilla", 
               "https://www.gutenberg.org/ebooks/bookshelf/"
               ]
    subprocess.call(sp_args)

    # move it to metadata dir
    if is_win32:
        dst = "metadata/bookshelves_html/"
        if not os.path.exists(dst):
            os.mkdir(dst)
        for src_path in glob.glob("www.gutenberg.org/ebooks/bookshelf/*"):
            shutil.move(src_path, dst)
    else:
        sp_args = "mv www.gutenberg.org/ebooks/bookshelf/* metadata/bookshelves_html/"
        subprocess.call(sp_args, shell=True)

    # cleanup
    if os.path.exists("www.gutenberg.org"):
        rm_dir("www.gutenberg.org")
    # in the new version of the website and with these parameters of the wget (gets also other links within the crawled page)
    # we get also other files, copy of the bookshelves but with different ordering
    # remove them
    rm_pattern("metadata/bookshelves_html/*.opds*")
    rm_pattern("metadata/bookshelves_html/*?sort*")
    rm_pattern("metadata/bookshelves_html/*?start*")
    return None

def parse_bookshelves():
    """
    Parse the bookshelves html files.

    Builds up a dictionary of bookshelf_category:list(book_ids) and 
    a dictionary of bookshelf_category:list(title_category)
    from the individual html files of each bs.
    
    Prints the errors.
    """
    # parse the data
    BS_paths = glob.glob("metadata/bookshelves_html/*")
    # BS = [os.path.split(path)[-1] for path in BS_paths]

    BS_dict = {}
    BS_num_to_category_str_dict = {}
    for path in BS_paths:
        _, bs = os.path.split(path)
        PG_header = '' if bs == "index.html" else "PG"
        BS_dict[bs] = []
        with open(path, "r", encoding="UTF-8") as foo:
            dom = lxml.html.parse(path)
            # select the url in href for all a tags(links)
            for link in dom.xpath('//a/@href'):
                # links to ebooks that are not searches
                if link.find("ebooks") > -1 and link.find("search") == -1:
                    book_id = link.split("/")[-1]
                    if book_id.isdigit():
                        BS_dict[bs].append(PG_header + book_id)
            # get title of the category
            title_categories = dom.findall('.//title') # './/title' finds recursively the element with tag 'title'
            # check if there is only one title in the metadata of the category
            if len(title_categories) == 0:
                # debug prints
                print('No category title')
                print(path, list(dom), dom.text_content())
                title_category = None
            elif len(title_categories) == 1:
                title_category = title_categories[0].text
            else:
                # get only first title but check also others
                title_category = title_categories[0].text
                print([title_categories[i].text for i in range(len(title_categories))])
            BS_num_to_category_str_dict[bs] = title_category
        # delete empty BSs
        if len(BS_dict[bs]) == 0:
            del BS_dict[bs]
            del BS_num_to_category_str_dict[bs]
    return BS_dict, BS_num_to_category_str_dict
