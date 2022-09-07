import re
import unicodedata
import pandas as pd
import numpy as np
import nltk
from nltk.tokenize.toktok import ToktokTokenizer
from nltk.corpus import stopwords
from sklearn.model_selection import train_test_split

def missing_rename(df):
    df = df.dropna() # drop all nulls
    df.language = np.where(df.language == 'Jupyter Notebook', 'Python', df.language) #convert jupyter notebook to python -based on random sampling and topic experience, most jupyter notebooks were python language with a few being Julia
    df.language = np.where((df.language != 'Python') & (df.language != 'R') & (df.language != 'JavaScript'), 'Other', df.language)# name all languages that are not Python, R, or JavaScript as 'Other'
    return df

def basic_clean(text):
    article = text.lower() #lower case all text
    article = unicodedata.normalize('NFKD', article)\
    .encode('ascii', 'ignore')\
    .decode('utf-8', 'ignore')#unicode data
    article = re.sub(r"[^a-z0-9'\s]", '', article) #remove all nonalphanumeric or space characters
    return article 

def tokenize(basic_clean_text):
    tokenizer = nltk.tokenize.ToktokTokenizer()#get tokenizer
    article = tokenizer.tokenize(basic_clean_text, return_str=True) #apply tokenizer
    return article

def lemmatize(tokenized_text):    
    wnl = nltk.stem.WordNetLemmatizer() #get lemmatizer    
    lemmas = [wnl.lemmatize(word) for word in tokenized_text.split()]   #use lemmatizer on each individual word 
    lemmatized_string = ' '.join(lemmas)    #join words together in a string, separated by a space
    return lemmatized_string

def remove_stopwords(string, extra_words=None, exclude_words=None):    
    stopword_list = stopwords.words('english')    
    if exclude_words:        
        stopword_list = stopword_list + exclude_words #add words to be removed
        
    if extra_words:        
        for word in extra_words:            
            stopword_list.remove(word) #remove words from list of stopwords
            
    words = string.split()    
    filtered_words = [word for word in words if word not in stopword_list]  #filter each word through the stoplist    
    filtered_string = ' '.join(filtered_words)  #join words back together in a string, separated by a space 
    return filtered_string

def prepare_df(df):
    df = missing_rename(df)
    df['clean'] = df['readme_contents'].apply(basic_clean).apply(tokenize).apply(remove_stopwords) #apply functions above
    df['lemmatized'] = df['clean'].apply(lemmatize) #used lemmatize instead of stemmed   
    return df

from sklearn.model_selection import train_test_split

def split_data_for_explore(df): #split data
    train_validate, test = train_test_split(df,test_size=0.2, random_state=123) #spicify random state so we get the same split everytime
    train, validate = train_test_split(train_validate,test_size=0.3, random_state=123) #spicify random state so we get the same split everytime
    
    return train, validate, test

ADDITIONAL_STOPWORDS = ['1','2','3','4','5','u'] #added stopwords we wanted removed from teh data

def clean_for_explore(text): #combination of above functions AND removes the ADDITONAL_STOPWORDS
    'A simple function to cleanup data'
    wnl = nltk.stem.WordNetLemmatizer()
    stopwords = nltk.corpus.stopwords.words('english') + ADDITIONAL_STOPWORDS
    text = (unicodedata.normalize('NFKD', text)
             .encode('ascii', 'ignore')
             .decode('utf-8', 'ignore')
             .lower())
    words = re.sub(r'[^\w\s]', '', text).split()
    return [wnl.lemmatize(word) for word in words if word not in stopwords]

def data_split_for_modeling(x_data, y_data): #data split
    ''' splitting for x & y train,validate,test'''
    x_train_validate, x_test, y_train_validate, y_test = train_test_split(x_data, y_data, 
                                                                          stratify = y_data, 
                                                                          test_size=.2, random_state=123) #spicify random state so we get the same split everytime
    
    x_train, x_validate, y_train, y_validate = train_test_split(x_train_validate, y_train_validate, 
                                                                stratify = y_train_validate, 
                                                                test_size=.3, 
                                                                random_state=123) #spicify random state so we get the same split everytime
    
    return x_train, y_train, x_validate, y_validate, x_test, y_test