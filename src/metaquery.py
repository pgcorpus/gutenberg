# -*- coding: utf-8 -*-
"""
Query metadata. Get id's of books with given
- language
- author
- subject
- date
- ...

"""

import os 
import pandas as pd
import numpy as np
from collections import Counter
import re
import glob

class meta_query(object):

    def __init__(self, path='../metadata/metadata.csv', filter_exist=True):
        '''filter_exist: Only keep entries in metadata for which we have the downloaded text.
        '''

        self.df = pd.read_csv(path) ## the dataframe on which we apply filters
        if filter_exist == True: ## filter the books for which we have the data
            path_text = os.path.abspath(os.path.join(path,os.pardir,os.pardir,'data','text'))
            list_files = []
            for file in list(glob.glob( path_text+'/PG*_text.txt' )):
                list_files += [file]
            list_ids = sorted([ h.split('/')[-1].split('_text')[0] for h in list_files ])
            df = self.df
            df_new = df[df['id'].isin(list_ids)]
            self.df = df_new
        self.df_original = self.df ## keep the original dataframe

    def reset(self):
        '''reset df to original dataframe (remove all filters)
        '''
        self.df = self.df_original

    def get_ids(self):
        '''return list of PG-ids of filtered dataframe
        '''
        list_book_ids = self.df['id']
        return list(list_book_ids)

    def get_df(self):
        '''return the filtered dataframe
        '''
        return self.df

    def filter_lang(self,lang_sel,how='only'):
        """
        Filter metadata by language.

        Parameters
        ----------
        lang_sel : str
            Two-letter language code.
        how : str
            'only' to select books that only contain lang_sel
            'any' to select books that contain lang_sel and maybe other langs
        """
        if how == 'only':
            s = self.df[self.df['language'] == "['%s']"%(lang_sel)]
        elif how =='any':
            s = self.df[self.df['language'].str.contains("'%s'"%(lang_sel)).replace(np.nan,False)]
        else:
            s = meta
        self.df = s

    ### LANGUAGE
    def get_lang(self):
        list_lang = [[k for k in h.strip("[]")[1:-1].replace("', '","_").split('_')] for h in self.df['language'].dropna()]
        list_lang_flat = [item for sublist in list_lang for item in sublist]
        list_lang_set = sorted(list(set(list_lang_flat)))
        return list_lang_set

    def get_lang_counts(self):
        list_lang = [[k for k in h.strip("[]")[1:-1].replace("', '","_").split('_')] for h in self.df['language'].dropna()]
        list_lang_flat = [item for sublist in list_lang for item in sublist]
        return Counter(list_lang_flat)
    ### SUBJECTS
    def get_subjects(self):
        list_subjects = [[k for k in h.strip("{}")[1:-1].replace("', '","_").split('_')] for h in self.df['subjects'].replace('set()',np.nan).dropna()]
        list_subjects_flat = [item for sublist in list_subjects for item in sublist]
        list_subjects_set = sorted(list(set(list_subjects_flat)))
        return list_subjects_set

    def get_subjects_counts(self):
        list_subjects = [[k for k in h.strip("{}")[1:-1].replace("', '","_").split('_')] for h in self.df['subjects'].replace('set()',np.nan).dropna()]
        list_subjects_flat = [item for sublist in list_subjects for item in sublist]
        return Counter(list_subjects_flat)

    def filter_subject(self,subject_sel,how='only'):
        ## filter metadata for subjects
        ## how == 'only', books that only contain subject
        ## how == 'any', all books that contain subject (and potentially others too)
        if how == 'only':
            s = self.df[self.df['subjects'] == "{'%s'}"%(subject_sel)]
        elif how =='any':
            s = self.df[self.df['subjects'].str.contains("'%s'"%(re.escape(subject_sel))).replace(np.nan,False)]
        else:
            s = meta
        self.df = s

    ### TIME
    def filter_year(self,y_sel,hmin=20):
        '''
        We filter all books, where 
        - authoryearofbirth <= y_sel - hmin
        - authoryearofdeath > y_sel
        Note: 
        - 1842 books with only authoryearofbirth 
        - 847 books with only authoryearofdeath
        - 13996 books missing both
        '''
        if isinstance(y_sel,(list,np.ndarray)):
            s = self.df[ (self.df['authoryearofbirth'] <= y_sel[1] - hmin)&(self.df['authoryearofdeath']>y_sel[0])]
        else:
            s = self.df[ (self.df['authoryearofbirth'] <= y_sel - hmin)&(self.df['authoryearofdeath']>y_sel)]
        self.df = s

    ### AUTHOR
    def filter_author(self,s_sel):
        s = self.df[ self.df['author'].str.contains(re.escape(s_sel),case=False).replace(np.nan,False)] 
        self.df = s

    ### Sort by the n most downloaded
    def filter_downloads(self,n=-1):
        ### keep only the n most downloaded
        ### if n = -1, keep all
        s = self.df.sort_values('downloads',ascending=False)
        if n>0:
            s=s.iloc[:n]
        self.df = s




