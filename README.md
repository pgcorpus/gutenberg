# Standardized Project Gutenberg Corpus
Easily generate a local, up-to-date copy of the Standardized Project Gutenberg Corpus (SPGC).

The Standardized Project Gutenberg Corpus was presented in 

[A standardized Project Gutenberg corpus for statistical analysis of natural language and quantitative linguistics](https://arxiv.org/abs/1812.08092)  
M. Gerlach, F. Font-Clos, arXiv:1812.08092, Dec 2018

acompanied by a 'frozen' version of the corpus (SPGC-2018-07-18) as a Zenodo dataset: 

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.2422560.svg)](https://doi.org/10.5281/zenodo.2422560)

SPGC-2018-07-18 contains the `tokens/` and `counts/` files of all books that were part of Project Gutenbergh (PG) as of Jul 18, 2018, matching exactly those used in the paper. Since then, a few more thousands books have been added to PG, so if you want to exactly reproduce the results of the paper, then you should use SPGC-2018-07-18.

For **most other use cases**, however, you probably want the latest, most recent version of the corpus, in which case you should use this repository to **generate the corpus locally** on your computer. In particular, you will need to generate the corpus locally if you need to work with the original full text files in `raw/` and `text/`, since these are not included in the SPGC-2018-07-18 Zenodo dataset.


## Installation
:warning: **Python 2.x is not supported** Please make sure your system runs Python 3.x. (https://pythonclock.org/).  

Clone this repository

```bash
git clone https://github.com/pgcorpus/gutenberg.git
```
enter the newly created `gutenberg` directory

```bash
cd gutenberg
```

To install any missing dependencies, just run

```bash
pip install -r requirements.txt
```

## Getting the data
To get a local copy of the PG data, just run
```
python get_data.py
```
This will download a copy of all UTF-8 books in PG and will create a csv file with metadata (e.g. author, title, year, ...).

Notice that if you already have some of the data, the program will only download those you are missing (we use `rsync` for this). It is hence easy to update the dataset periodically to keep it up-to-date by just running `get_data.py`.


## Processing the data
To process all the data in the `raw/` directory, run
```bash
python process_data.py
```
This will fill in the `text/`, `tokens/` and `counts/` folders.



