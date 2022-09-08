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

Clone the repo to get final_notebook, acquire.py, prepare.py

    Run the acquire.py and prepare.py notebooks. This will acquire, prepare, and save a .csv
    OR
    Use the inflation_readme.csv already saved in the repo.


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
'Other' with an accuracy on train of 42.12%

#### Best Model: 
Random Forest TD-IDF with max depth of 4 and an accuracty on validate of 59.53 

#### Test:
Random Forest TD-IDF with max depth of 4 and an accuracty on test of 51.43%



#  Recommendations and Future Work

- adjust stop words to remove the words 'data' and 'inflation' to try and get more specific and unique wording for each language
- try different classification models such as KNN
- try unsupervised learning to see if there are any new insights into the different groupings of data



# Detailed Project Plan

- Friday
    - finish acquiring data
    
- Tuesday
    - prepare and explore data
    
Wednesday
    - modeling, readme, slides

Thursday
    - add comments and practice presentation
    - turn in by 14:30


