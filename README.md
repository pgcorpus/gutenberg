# Standardized Project Gutenberg Corpus
Easily generate a local, up-to-date copy of the Standardized Project Gutenberg Corpus (SPGC).

The Standardized Project Gutenberg Corpus was presented in 

(Publication)[url to doi]
M. Gerlach, F. Font-Clos
2018

There is a 'frozen' version of the SPGC corpus tagged *SPGC-2018-07-18* avaialble for download here: 

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.2422560.svg)](https://doi.org/10.5281/zenodo.2422560)

You should use this version if you want to reproduce the results of the paper, since books are added daily to Project Gutenberg. If you want the latest, most recent version of the corpus, we recommend you use this repository to generate the corpus locally on your computer.


## Installation
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



