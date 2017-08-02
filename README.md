# Project Gutenberg

## Getting the data
To get a local copy of the PG data, just run
```
python get_data.py
```
This will download a copy of all UTF-8 books in PG and will create a csv file with metadata (e.g. author, title, year, ...).

Notice that if you already have some of the data, the program will only download those you are missing (we use `rsync` for this). It is hence easy to update the dataset periodically to keep it up-to-date by just running `get_data.py`.


## Processing the data
To process all the data in the `raw/` directory, run
```
python process_data.py
```
This will fill in the `text/`, `tokens/` and `counts/` folders.


## Pip

Assuming you have python3, just run

```
pip install requirements_pip.txt
```
and you will get the required packages (see below)



## Conda Environment

Alternatively, you can use a conda-environment to run the scripts.
Install conda as described here https://www.digitalocean.com/community/tutorials/how-to-install-the-anaconda-python-distribution-on-ubuntu-16-04


create an environment called 'gutenberg' with all the required packages:
```
conda create --name gutenberg --file requirements.txt
```
using the `requirements.txt` file corresponding to your platform.

Activate the environment so that you can work with it: `source activate gutenberg`

Deactivate the environment: `source deactivate`

Add packages to the environment: `conda install --name gutenberg <package>`

Update requirements with `conda list --explicit > requirements-your-platform.txt`
to create platform-specific links, or `conda list -e > requirements.txt` for universal links.


## Packages needed if you dont want to use conda
+ python (3.)
+ NLTK
+ pandas
+ jupyter (optional, for the example notebooks)

