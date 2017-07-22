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

