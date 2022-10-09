# -*- coding: utf-8 -*-
from src.utils import get_PG_number
from .cleanup import strip_headers
from .tokenizer import tokenize_text
from collections import Counter

def process_book(
	path_to_raw_file=None,
	text_dir=None,
	tokens_dir=None,
	counts_dir=None,
	tokenize_f=tokenize_text,
	cleanup_f=strip_headers,
    overwrite_all=False,
    language="english",
    log_file=None
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
    keyword can change this behaviour.

    Parameters
    ----------
    overwrite_all : bool
        If set to True, everything is processed regardless of existing files.
    """
    if text_dir is None:
        raise ValueError("You must specify a path to save the text files.")

    if tokens_dir is None:
        raise ValueError("You must specify a path to save the tokens files.")

    if counts_dir is None:
        raise ValueError("You must specify a path to save the counts files.")

    if path_to_raw_file is None:
        raise ValueError("You must specify a path to the raw file to process.")

    PG_number = get_PG_number(path_to_raw_file)
    text_path = text_dir / ("PG%s_text.txt" % PG_number)
    tokens_path = tokens_dir / ("PG%s_tokens.txt" % PG_number)
    counts_path = counts_dir / ("PG%s_counts.txt" % PG_number)

    if overwrite_all or not \
        all(f.is_file() for f in [text_path, tokens_path, counts_path]):
        # read raw file
        text = path_to_raw_file.read_text(encoding="UTF-8")

        # clean it up
        clean = cleanup_f(text)

        # write text file
        text_path.write_text(clean, encoding="UTF-8")

        # compute tokens
        tokens = tokenize_f(clean, language=language)

        # write tokens file
        tokens_path.write_text("\n".join(tokens)+"\n", encoding="UTF-8")

        # compute counts
        counts = Counter(tokens)

        # write counts file
        counts = "\n".join([w+"\t"+str(c) for w,c in counts.most_common()])+"\n"
        counts_path.write_text(counts, encoding="UTF-8")

        # write log info if log_file is not None
        if log_file is None:
            return

        log_data=[
            "PG"+PG_number,
            language,
            text.count("\n"),
            clean.count("\n"),
            len(tokens),
            len(counts),
        ]
        with log_file.open("a") as f:
           f.write('\t'.join(map(str, log_data))+"\n")

