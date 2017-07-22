# gutenberg

## Mirroring the PG site
We rsync a mirror of the PG website at `data/mirror/`.
At the moment we work with 1% of the books, to create a local copy
you must run the following

```
mkdir -p data/mirror
rsync -av --del --include '*/' --include '*99-8.txt' --exclude '*' aleph.gutenberg.org::gutenberg data/mirror/
```

## Populating the raw text folder

At the moment, run the notebook in `nb_dev/`

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

