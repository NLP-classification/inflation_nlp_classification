import re
import unicodedata
import pandas as pd
import numpy as np
import nltk
from nltk.tokenize.toktok import ToktokTokenizer
from nltk.corpus import stopwords
from sklearn.model_selection import train_test_split

def missing_rename(df):
    df = df.dropna()
    df.language = np.where(df.language == 'Jupyter Notebook', 'Python', df.language)
    df.language = np.where((df.language != 'Python') & (df.language != 'R') & (df.language != 'JavaScript'), 'Other', df.language)
    return df

def basic_clean(text):
    article = text.lower()
    article = unicodedata.normalize('NFKD', article)\
    .encode('ascii', 'ignore')\
    .decode('utf-8', 'ignore')
    article = re.sub(r"[^a-z0-9'\s]", '', article)
    return article 

def tokenize(basic_clean_text):
    tokenizer = nltk.tokenize.ToktokTokenizer()
    article = tokenizer.tokenize(basic_clean_text, return_str=True)
    return article

def lemmatize(tokenized_text):    
    wnl = nltk.stem.WordNetLemmatizer()    
    lemmas = [wnl.lemmatize(word) for word in tokenized_text.split()]    
    lemmatized_string = ' '.join(lemmas)    
    return lemmatized_string

def remove_stopwords(string, extra_words=None, exclude_words=None):    
    stopword_list = stopwords.words('english')    
    if exclude_words:        
        stopword_list = stopword_list + exclude_words
        
    if extra_words:        
        for word in extra_words:            
            stopword_list.remove(word)
            
    words = string.split()    
    filtered_words = [word for word in words if word not in stopword_list]    
    filtered_string = ' '.join(filtered_words)   
    return filtered_string

def prepare_df(df):
    df = missing_rename(df)
    df['clean'] = df['readme_contents'].apply(basic_clean).apply(tokenize).apply(remove_stopwords)
    df['lemmatized'] = df['clean'].apply(lemmatize)    
    return df

from sklearn.model_selection import train_test_split

def split_data_for_explore(df):
    train_validate, test = train_test_split(df,test_size=0.2, random_state=123)
    train, validate = train_test_split(train_validate,test_size=0.3, random_state=123)
    
    return train, validate, test

ADDITIONAL_STOPWORDS = ['1','2','3','4','5','u']

def clean_for_explore(text):
    'A simple function to cleanup data'
    wnl = nltk.stem.WordNetLemmatizer()
    stopwords = nltk.corpus.stopwords.words('english') + ADDITIONAL_STOPWORDS
    text = (unicodedata.normalize('NFKD', text)
             .encode('ascii', 'ignore')
             .decode('utf-8', 'ignore')
             .lower())
    words = re.sub(r'[^\w\s]', '', text).split()
    return [wnl.lemmatize(word) for word in words if word not in stopwords]

def data_split_for_modeling(x_data, y_data):
    ''' splitting for x & y train,validate,test'''
    x_train_validate, x_test, y_train_validate, y_test = train_test_split(x_data, y_data, 
                                                                          stratify = y_data, 
                                                                          test_size=.2, random_state=123)
    
    x_train, x_validate, y_train, y_validate = train_test_split(x_train_validate, y_train_validate, 
                                                                stratify = y_train_validate, 
                                                                test_size=.3, 
                                                                random_state=123)
    
    return x_train, y_train, x_validate, y_validate, x_test, y_test