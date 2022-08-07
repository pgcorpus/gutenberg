# -*- coding: utf-8 -*-
"""Functions to download, parse and filter Gutenberg's bookshelves."""

import os
import glob
import numpy as np
import pandas as pd
import lxml.html
import subprocess


def get_bookshelves():
    """
    Scrap the bookshelves data from gutenbergs wiki.

    This function uses `wget` to scrap all the html
    files corresponding to a bookshelves. The html files
    are stored in `metadata/bookshelves`.

    """
    sp_args = ["wget",
               "--random-wait", "-r", 
               "-p", "--no-parent", 
               "-e", "robots=off", 
               "-U", "mozilla", 
               "https://www.gutenberg.org/ebooks/bookshelf/"
               ]
    subprocess.call(sp_args)

    # move it to metadata dir
    sp_args = "mv www.gutenberg.org/ebooks/bookshelf/* metadata/bookshelves_html/"
    subprocess.call(sp_args, shell=True)

    # cleanup
    sp_args = ["rm", "-rf", "www.gutenberg.org"]
    subprocess.call(sp_args)
    # in the new version of the website and with these parameters of the wget (gets also other links within the crawled page)
    # we get also other files, copy of the bookshelves but with different ordering
    # remove them
    sp_args = ["rm", "-rf", "metadata/bookshelves_html/*.opds*"]
    subprocess.call(sp_args)
    sp_args = ["rm", "-rf", "metadata/bookshelves_html/*?sort*"]
    subprocess.call(sp_args)
    sp_args = ["rm", "-rf", "metadata/bookshelves_html/*?start*"]
    subprocess.call(sp_args)
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
    BS = [path.split("/")[-1] for path in BS_paths]

    BS_dict = {}
    BS_num_to_category_str_dict = {}
    for path in BS_paths:
        bs = path.split("/")[-1]
        BS_dict[bs] = []
        with open(path, "r", encoding="UTF-8") as foo:
            dom = lxml.html.fromstring(foo.read())
            # select the url in href for all a tags(links)
            for link in dom.xpath('//a/@href'):
                # links to ebooks that are not searches
                if link.find("ebooks") > -1 and link.find("search") == -1:
                    PGid = "PG"+link.split("/")[-1]
                    BS_dict[bs].append(PGid)
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
