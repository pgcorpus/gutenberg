# -*- coding: utf-8 -*-
from .cleanup import strip_headers
from .tokenizer import tokenize_text
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
    overwrite_all=False,
    language="english",
    log_file=""
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

    Overwrite policy
    ----------------
    By default a book is processed in full except if all the 
    files already exist (raw,text,tokens and counts). The overwrite_all
    keyword can cahnge this behaviour.

    Parameters
    ----------
    overwrite_all : bool
        If set to True, everything is processed regargless of existing files.
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

    if overwrite_all or\
        (not os.path.isfile(os.path.join(text_dir,"PG%s_text.txt"%PG_number))) or \
        (not os.path.isfile(os.path.join(tokens_dir,"PG%s_tokens.txt"%PG_number))) or \
        (not os.path.isfile(os.path.join(counts_dir,"PG%s_counts.txt"%PG_number))):
        # read raw file
        with io.open(path_to_raw_file, encoding="UTF-8") as f:
            text = f.read()

        # clean it up
        clean = cleanup_f(text)

        # write text file
        target_file = os.path.join(text_dir,"PG%s_text.txt"%PG_number)
        with io.open(target_file,"w", encoding="UTF-8") as f:
            f.write(clean)

        # compute tokens
        tokens = tokenize_f(clean, language=language)
   
        # write tokens file
        target_file = os.path.join(tokens_dir,"PG%s_tokens.txt"%PG_number)
        with io.open(target_file,"w", encoding="UTF-8") as f:
            f.write("\n".join(tokens)+"\n")

        # compute counts
        counts = Counter(tokens)
        
        # write counts file
        target_file = os.path.join(counts_dir,"PG%s_counts.txt"%PG_number)
        with io.open(target_file,"w", encoding="UTF-8") as f:
            f.write("\n".join([w+"\t"+str(c) for w,c in counts.most_common()])+"\n")

        # write log info if log_file is not None
        if log_file != "":
            raw_nl = text.count("\n")
            clean_nl = clean.count("\n")
            L = len(tokens)
            V = len(counts)
            with io.open(log_file, "a") as f:
               f.write("PG"+str(PG_number)+"\t"+language+"\t"+str(raw_nl)+"\t"+str(clean_nl)+"\t"+str(L)+"\t"+str(V)+"\n")
                
