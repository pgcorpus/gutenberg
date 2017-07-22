# -*- coding: utf-8 -*-
from cleanup import strip_headers
from tokenizer import tokenize_text
import io
import os

def process_book(
	path_to_raw=None,
	text_dir="../data/text",
	tokens_dir="../data/tokens",
	counts_dir="../data/counts",
	tokenize_f=tokenize_text,
	cleanup_f=strip_headers,
	counting_f=None
	):

	# get PG number
    PG_number = path_to_raw.split("/")[-1].split("_")[0][2:]

    # read raw file
    with io.open(path_to_raw) as f:
        text = f.read()

    # clean it up
    clean = cleanup_f(text)

    # write text file
    target_file = os.path.join(text_dir,"PG%s_text.txt"%PG_number)
    with io.open(target_file,"w") as f:
        f.write(clean)

    tokens = tokenize_f(clean)

    # write tokens file
    # TODO

