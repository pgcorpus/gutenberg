# -*- coding: utf-8 -*-
"""This is the default tokenizer.
   Call tokenize and pass a text (i.e. as a string).
   You will get a list of tokens
"""

import nltk
nltk.data.path=["src/nltk_data"]

from nltk.tokenize.treebank import TreebankWordTokenizer
from nltk.tokenize import sent_tokenize


def tokenize_text(text, language="english"):
    '''Tokenize a string into a list of tokens.
    Use NLTK's Treebankwordtokenizer.
    Note that we first split into sentences using NLTK's sent_tokenize.
    We additionally call a filtering function to remove un-wanted tokens.
    
    IN:
    - text, str
    OUT:
    - list of strings
    '''
    ## list of tokens
    list_tokens = []
    
    ## split text into sentences
    sentences=sent_tokenize(text, language=language)
    
    ## define the tokenizer
    tokenizer = TreebankWordTokenizer()
    ## loop over all sentences
    for sent in sentences:
        ## tokenize the sentence
        sent_tokenized = tokenizer.tokenize(sent)
        ## lowercase the tokens
        ## add tokens to list of tokens
        list_tokens += sent_tokenized
    list_tokens = filter_tokens(list_tokens)
    return list_tokens

def filter_tokens(list_tokens):
    '''Remove un-wanted tokens from list of tokens
    We only keep words that return TRUE for string.isaplha()
    We lowercase every token with string.lower()
    '''
    list_tokens_filter = [h.lower() for h in list_tokens if h.isalpha()]
    return list_tokens_filter