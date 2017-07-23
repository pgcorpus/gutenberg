# -*- coding: utf-8 -*-
from cleanup import strip_headers
from tokenizer import tokenize_text
from collections import Counter
import io
import os

def process_book(
	path_to_raw_file=None,
	text_dir=None,
	tokens_dir=None,
	counts_dir=None,
	tokenize_f=tokenize_text,
	cleanup_f=strip_headers,
	counting_f=None
	):
    """
    Process a book, from raw data to counts.

    The database is structured in the following levels of processing:

    1. raw: the book as downloaded from PG site.
    2. text: the book with headers/legal notices/etc removed.
    3. tokens: the tokenized book. One token per line.
    4. counts: the counts of all types. One type per line.

    This function takes a file at the 'raw' level and computes the counts,
    saving to disk the intermediate 'text' and 'tokens' files.

    """
    if text_dir is None:
        raise ValueError("You must specify a path to save the text files.")
        
    if tokens_dir is None:
        raise ValueError("You must specify a path to save the tokens files.")
        
    if counts_dir is None:
        raise ValueError("You must specify a path to save the counts files.")
        
    if path_to_raw_file is None:
        raise ValueError("You must specify a path to the raw file to process.")
        
	# get PG number
    PG_number = path_to_raw_file.split("/")[-1].split("_")[0][2:]

    # read raw file
    with io.open(path_to_raw_file) as f:
        text = f.read()

    # clean it up
    clean = cleanup_f(text)

    # write text file
    target_file = os.path.join(text_dir,"PG%s_text.txt"%PG_number)
    with io.open(target_file,"w") as f:
        f.write(clean)

    # compute tokens
    tokens = tokenize_f(clean)

    # write tokens file
    target_file = os.path.join(tokens_dir,"PG%s_tokens.txt"%PG_number)
    with io.open(target_file,"w") as f:
        f.write("\n".join(tokens))

    # compute counts
    counts = Counter(tokens)

    # write counts file
    target_file = os.path.join(counts_dir,"PG%s_counts.txt"%PG_number)
    with io.open(target_file,"w") as f:
        f.write("\n".join([w+"\t"+str(c) for w,c in counts.most_common()]))
    
    
