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
```bash
python process_data.py
```
This will fill in the `text/`, `tokens/` and `counts/` folders.


## Dependencies

Assuming you have python3, just run

```bash
pip install requirements.txt
```
and you will get all dependencies installed.
