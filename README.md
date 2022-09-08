# inflation_nlp_classification

# Data Dictionary

                  
| Column Name      | Definition                                                                           |
| -------------    |------------------------------------------------------------------------------------: |
| repo             | name of repo on git hub                                                              |
| language         | language of repo from git hub                                                        |
| readme contents  | readme contents from github                                                          |
| clean            | lowercase, unicoded, nonalphnumeric or spaces removed, tokenized, removed stopwords  |
| lemmatized       | lemmatized                                                                           |
| stem             | stemmed                                                                              |
| all              | all readmes regardless of langauge                                                   |
| python           | all readmes labeled 'Python' by github                                               |
| javascript       | all readmes labeled 'javascript' by github                                           |    
| r                | all readmes labeled 'R' by github                                                    |
| other            | readmes labeled by github as any other language than Python, JavaScript, or R        |
| max_depth        | depth of tree(s)                                                                     |
| train_accuracy   | accuracy of model on trianing set                                                    |
| validate_accuracy| accuracy of model on validate set                                                    |
| difference       | difference between train_accuracy and validate_accuracy                              |  



# Steps to reproduce

You will need a Github personal access token.

1. Go here and generate a personal access token: https://github.com/settings/tokens
   You do _not_ need select any scopes, i.e. leave all the checkboxes unchecked
2. Save it in your env.py file under the variable `github_token`
   Add your github username to your env.py file under the variable `github_username`

Clone the repo

Libraries used are pandas, numpy, nlt, sklearn, wordcloud, matplotlib, and seaborn..


# Project Goals

Under inflation topic, determine the programming language used in the code of online github repos based on the contents of the README.md.

# Project Desciption

Inflation is an ongoing concern for many. We looked at github to see there are over 1,000 publicly available repos addressing inflation. We took a sample and after filtering out repos that do not have a readme, we ended up with a little over 500 repos to analyze. 


# Initial Testing and Hypothesis
1. What are the most common words in all READMEs related to the inflation topic?
2. Does the length of the README vary by programming language?
3. What are the most common words in python, javascript and R besides the keyword inflation?
4. Are there any words that uniquely identify a programming language?

# Report Findings 

### Initial Testing and Hypothesis
1. The word choice in the Readme will vary by program language.
    - True to an extent. When we look at the most common 20 words, they are fairly well distributed throughout the languages. If we look at the least common words, we see more stratrification. For instance, 'librarydpylr' is only referenced in R languge readmes becuase it imports an R statistics library. 

2. The Readme will vary in length based on program language.
    - Not true. Due to the large variance betweein readme's of the same language, the length alone is not an ideal variable to feed into the models.  
    
3. What are the most common words in python, javascript and R besides the key word inflation?
   - Python: data, using, price, model
    - R: data, file, project, inflation rate
    - JavaScript: map, text, data, file
    - Other: file, model, value, code
    - All: file, data, project, code

### Modeling
#### Baseline: 
'Other' with an accuracy on validate of 42.12%

#### Best Model: 
Bag of Words Random Forest with a max depth of 11 and an accuracy on validate of 72.95% 

#### Test:
Bag of Words Random Forest with a max depth of 11 and an accuracy of %



#  Recommendations and Future Work

- combine model with models that predict changes in temperature and rainfall to get a more accurate predictions

- regulate water usage to minimize use of limited water resources

- invest in salt-water conversion to fresh water


# Detailed Project Plan-do we need this?

