# Standardized Project Gutenberg Corpus
Easily generate a local, up-to-date copy of the Standardized Project Gutenberg Corpus (SPGC).

The Standardized Project Gutenberg Corpus was presented in 

[A standardized Project Gutenberg corpus for statistical analysis of natural language and quantitative linguistics](https://arxiv.org/abs/1812.08092)  
M. Gerlach, F. Font-Clos, arXiv:1812.08092, Dec 2018

acompanied by a 'frozen' version of the corpus (SPGC-2018-07-18) as a Zenodo dataset: 

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.2422560.svg)](https://doi.org/10.5281/zenodo.2422560)

SPGC-2018-07-18 contains the `tokens/` and `counts/` files of all books that were part of Project Gutenbergh (PG) as of Jul 18, 2018, matching exactly those used in the paper. Since then, a few more thousands books have been added to PG, so if you want to exactly reproduce the results of the paper, then you should use SPGC-2018-07-18.

For **most other use cases**, however, you probably want the latest, most recent version of the corpus, in which case you should use this repository to **generate the corpus locally** on your computer. In particular, you will need to generate the corpus locally if you need to work with the original full text files in `raw/` and `text/`, since these are not included in the SPGC-2018-07-18 Zenodo dataset.

## Changes in this fork
- Windows support (still need to install `wget` and `cwRsync` (cwRsync tested with 5.4.1)
- Fixed stuffs in original code:
  - oversights (bookshelves info are never fetched, nltk missing download, utf-8 decoding error in ebook header, etc.)
  - bugs & typos
- Parallelised text processing
- Additional arguments for customization

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
> For Windows users, see the [**Usage**](#usage) section

## Processing the data
To process all the data in the `raw/` directory, run
```bash
python process_data.py
```
This will fill in the `text/`, `tokens/` and `counts/` folders.
> To avoid losing ebooks that are actually UTF-8 but mistakenly removed in the original code, see the [**Usage**](#usage) section

## Usage
**Recommended usage for `get_data.py` (Windows user):** 
```bash
python get_data.py --rsync "cwRsync_5.4.1/rsync"
```
(replace `cwRsync_5.4.1/rsync` with path to your rsync binary, `.exe` is not needed)

**Recommended usage for `process_data.py`:**
```bash
python process_data.py --ignore
```

**How to use `get_data.py` with customisation options:**
```
python get_data.py --help
usage: Update local PG repository.

This script will download all books currently not in your
local copy of PG and get the latest version of the metadata.

       [-h] [-m MIRROR] [-r RAW] [-M METADATA] [-p PATTERN] [-k] [-owr] [-q] [-c] [--rsync RSYNC] [--procedures PROCEDURES]

options:
  -h, --help            show this help message and exit
  -m MIRROR, --mirror MIRROR
                        Path to the mirror folder that will be updated via rsync.
  -r RAW, --raw RAW     Path to the raw folder.
  -M METADATA, --metadata METADATA
                        Path to the metadata folder.
  -p PATTERN, --pattern PATTERN
                        Patterns to get only a subset of books.
  -k, --keep_rdf        If there is an RDF file in metadata dir, do not overwrite it.
  -owr, --overwrite_raw
                        Overwrite files in raw.
  -q, --quiet           Quiet mode, do not print info, warnings, etc
  -c, --clean           Clean the mirror directory to remove any empty folders
  --rsync RSYNC         Specify an alternative rsync command
  --procedures PROCEDURES
                        Procedures to go through, defaults to "pdlmbs": [p]ull mirror files; find [d]uplicates; hard [l]ink from mirror to raw;   
                        get [m]etadata; get [b]ookshelf information; [s]tore bookshelf information
```

**How to use `process_data.py` with customisation options:**
```
python process_data.py --help
[nltk_data] Downloading package punkt to src/nltk_data...
[nltk_data]   Package punkt is already up-to-date!
usage: Processing raw texts from Project Gutenberg: i) removing headers,ii) tokenizing, and iii) counting words.
       [-h] [-r RAW] [-ote OUTPUT_TEXT] [-oto OUTPUT_TOKENS] [-oco OUTPUT_COUNTS] [-p PATTERN] [-q] [-l LOG_FILE] [-c] [--ignore]
       [--pool {process,thread}]

options:
  -h, --help            show this help message and exit
  -r RAW, --raw RAW     Path to the raw-folder
  -ote OUTPUT_TEXT, --output_text OUTPUT_TEXT
                        Path to text-output (text_dir)
  -oto OUTPUT_TOKENS, --output_tokens OUTPUT_TOKENS
                        Path to tokens-output (tokens_dir)
  -oco OUTPUT_COUNTS, --output_counts OUTPUT_COUNTS
                        Path to counts-output (counts_dir)
  -p PATTERN, --pattern PATTERN
                        Pattern to specify a subset of books
  -q, --quiet           Quiet mode, do not print info, warnings, etc
  -l LOG_FILE, --log_file LOG_FILE
                        Path to log file
  -c, --check_empty     Whether to check if existing files are empty
  --ignore              Whether to ignore UTF-8 decoding errors
  --pool {process,thread}
                        Whether to use multi-processing or multi-threading
```
