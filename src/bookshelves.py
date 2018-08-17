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
               "-A", "*Bookshelf*",
               "-p", "--no-parent",
               "-e", "robots=off",
               "-U", "mozilla",
               "http://www.gutenberg.org/wiki/Category:Bookshelf"
               ]
    subprocess.call(sp_args)

    # move it to metadata dir
    sp_args = "mv www.gutenberg.org/wiki/*Bookshelf* metadata/bookshelves/"
    subprocess.call(sp_args, shell=True)

    # cleanup
    sp_args = ["rm", "-rf", "www.gutenberg.org"]
    subprocess.call(sp_args)


def parse_bookshelves():
    """
    Parse the bookshelves html files.

    Builds up a Dataframe of books x bookshelves
    from the inidvidual html files of each bs.

    """
    # parse the data
    BS_paths = glob.glob("metadata/bookshelves/*Bookshelf*")
    BS = [path.split("/")[-1] for path in BS_paths]

    BS_dict = {}
    for path in BS_paths:
        bs = path.split("/")[-1]
        BS_dict[bs] = []
        with open(path, "r") as foo:
            dom = lxml.html.fromstring(foo.read())
            # select the url in href for all a tags(links)
            for link in dom.xpath('//a/@href'):
                # links to ebooks that are not searches
                if link.find("ebooks") > -1 and link.find("search") == -1:
                    PGid = "PG"+link.split("/")[-1]
                    BS_dict[bs].append(PGid)

        # delete empty BSs
        if len(BS_dict[bs]) == 0:
            del BS_dict[bs]

    # recompose list of BSs
    BS = list(BS_dict.keys())

    # list of unique PGids
    PGids = list(set(np.concatenate(list(BS_dict.values()))))
    # put in a DataFrame
    df = pd.DataFrame(index=PGids, columns=BS)
    for k, v in BS_dict.items():
        df.loc[v, k] = True
    return df


def filter_bookshelves(df, min_books=50, max_books=150):
    """Filter bookshelves by size, overlap and language."""
    # filter by size
    sdf = df.loc[:, (df.sum() > min_books) & (df.sum() <= max_books)].dropna(how="all")

    # deal with overlaps
    sdf = sdf.loc[sdf.sum(axis=1) == 1].dropna(how="all", axis=1)
    sdf = sdf.drop("Esperanto_(Bookshelf)", axis=1).dropna(how="all")

    # filter by language
    from src.metaquery import meta_query
    mq = meta_query(path="metadata/metadata.csv")
    mq.filter_lang("en", how="only")
    allPGs = mq.df.set_index("id").index
    sdf = sdf.loc[np.intersect1d(sdf.index, allPGs)].dropna(how="all", axis=1)
    return sdf
