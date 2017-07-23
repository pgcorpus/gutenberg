#/bin/bash

mkdir -p data/mirror
mkdir -p data/raw
mkdir -p data/text
mkdir -p data/tokens
mkdir -p data/counts

#rsync -av --del --include '*/' --include '*99-0.txt' --exclude '*' aleph.gutenberg.org::gutenberg data/mirror/

echo 'import sys
sys.path.append("src")
from utils import populate_raw_from_mirror
populate_raw_from_mirror(mirror_dir = "data/mirror/",raw_dir = "data/raw/")' | python
