# gutenberg

## Mirroring the PG site
We rsync a mirror of the PG website at `data/mirror/`.
At the moment we work with 1% of the books, to create a local copy
you must run the following

```
mkdir -p data/mirror
rsync -av --del --include '*/' --include '*99-0.txt' --exclude '*' aleph.gutenberg.org::gutenberg data/mirror/
```

this will download only PG books ending in 99 and encoded in UTF-8 (-0.txt suffix)

## Populating the raw text folder
At the moment, run the notebook in `nb_dev/`


## Removing headers and tails
We take code from this repo: https://github.com/c-w/gutenberg  
Use the `cleanup` function in `src/cleanup.py`. There is an example
notebook in nb_dev 

## Conda Environment

Install conda as described here: https://www.digitalocean.com/community/tutorials/how-to-install-the-anaconda-python-distribution-on-ubuntu-16-04

create an environment called 'gutenberg' with all the required packages:
conda create --name gutenberg --file requirements.txt

Activate the environment so that you can work with it:
source activate gutenberg

Deactivate the environment:
source deactivate

Add packages:
conda install --name gutenberg <package>

Update requirements.txt - file
conda list --explicit > requirements.txt

## Packages needed if you dont want to use conda
python (3.)
NLTK
pandas
jupyter (optional, for the example notebooks)

