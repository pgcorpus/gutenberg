mkdir -p data/mirror
mkdir -p data/raw
mkdir -p data/text
mkdir -p data/tokens
mkdir -p data/counts

rsync -av --del --include '*/' --include '*99-0.txt' --exclude '*' aleph.gutenberg.org::gutenberg data/mirror/
