# -*- coding: utf-8 -*-
"""Functions to download, parse and filter Gutenberg's bookshelves."""

from itertools import chain
from pathlib import Path
import shutil
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
    new_dir = Path("metadata/bookshelves_html")
    Path("www.gutenberg.org/ebooks/bookshelf").rename(new_dir)

    # cleanup
    shutil.rmtree("www.gutenberg.org")

    # in the new version of the website and with these parameters of the wget (gets also other links within the crawled page)
    # we get also other files, copy of the bookshelves but with different ordering
    # remove them
    for file in chain(
        new_dir.glob("*.opds*"),
        new_dir.glob("*?sort*"),
        new_dir.glob("*?start*")
    ):
        file.unlink()

    return None

def parse_bookshelves(path=Path("metadata/bookshelves_html")):
    """
    Parse the bookshelves html files.

    Builds up a dictionary of bookshelf_category:list(book_ids) and
    a dictionary of bookshelf_category:list(title_category)
    from the individual html files of each bs.

    Prints the errors.
    """
    # parse the data
    (path / ".dummy").unlink() # prevent hidden dummy file to be parsed
    BS_dict = {}
    BS_num_to_category_str_dict = {}
    for file in path.iterdir():
        bs = file.name
        BS_dict[bs] = []
        with file.open("r", encoding="UTF-8") as foo:
            dom = lxml.html.fromstring(foo.read())
            # select the url in href for all a tags(links)
            for link in dom.xpath('//a/@href'):
                # links to ebooks that are not searches
                if "ebooks" in link and not "search" in link:
                    PGid = "PG"+link.split("/")[-1]
                    BS_dict[bs].append(PGid)
            # get title of the category
            title_categories = dom.findall('.//title') # './/title' finds recursively the element with tag 'title'
            # check if there is only one title in the metadata of the category
            if len(title_categories) == 0:
                # debug prints
                print('No category title')
                print(file, list(dom), dom.text_content())
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
