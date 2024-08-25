import hazm as hz
import pandas as pd
import numpy as np
import math
from nltk.corpus import stopwords
from hazm.utils import stopwords_list
import string

punctuations = ['۱','۲','۳','۴','۵','۶','۷','۸','۹','۰', ',', '.', ')', '(', ':', '«', '،', '»' , '؟' , '،' , '؛' , '-' , 'ـ' , '٪' , '!' , '٬', '<', '>', '{', '}', '[', ']', '?', '|', '#', '/', '^', '\'', '\"']
stopwords =[]
df_train = pd.read_csv('books_train.csv')
df_test = pd.read_csv('books_test.csv')

data_of_books =['title', 'description', 'categories']

bag_of_words = [[],[],[],[],[],[]]
category1= "کلیات اسلام"
category2= "مدیریت کسب و کار"
category3 = "داستان کودک و نوجوانان"
category4 ="رمان"
category5 = "داستان کوتاه"
category6 = "جامه شناسی"

normalizer = hz.Normalizer()
stopwords = hz.stopwords_list()
lemmeatizer = hz.Lemmatizer()
tokennizer = hz.WordTokenizer()
tokenized_list =[]

def index_category(cat):
    if cat == "مدیریت و کسب و کار": return 0
    elif cat == "رمان": return 1
    elif cat == "کلیات اسلام": return 2 
    elif cat == "داستان کودک و نوجوانان": return 3
    elif cat == "جامعه‌شناسی": return 4
    elif cat == "داستان کوتاه": return 5 

final_text = []
remove_puncs_and_nums = ""
for i in range(len(df_train)): 
    normalized_string = normalizer.normalize(df_train.loc[i]["description"])
    lemmatizer_string = lemmeatizer.lemmatize(normalized_string)
    '''for char in lemmatizer_string:
        if char not in punctuations: remove_puncs_and_nums += char'''
    tokenized_list = tokennizer.tokenize(lemmatizer_string)
    '''for word in tokenized_list:
        if word not in stopwords: final_text.append(word)'''
    category_book = df_train.loc[i]["categories"]
    bag_of_words[index_category(category_book)].extend(tokenized_list)
    #print("a")


def function(description): 
    final_text_test = []
    #remove_puncs_and_nums_test = ""
    normalized_string_test = normalizer.normalize(description)
    lemmatizer_string_test = lemmeatizer.lemmatize(normalized_string_test)
    '''for char in lemmatizer_string_test:
        if char not in punctuations: remove_puncs_and_nums_test += char'''
    tokenized_list_test = tokennizer.tokenize(lemmatizer_string_test)
    '''for word in tokenized_list_test:
        if word not in stopwords: final_text_test.append(word)'''
    return tokenized_list_test

def choose_category(cat):
    if cat == 0: return "مدیریت و کسب و کار"
    elif cat == 1: return "رمان"
    elif cat == 2: return "کلیات اسلام"
    elif cat == 3: return "داستان کودک و نوجوانان"
    elif cat == 4: return "جامعه‌شناسی"
    elif cat == 5: return "داستان کوتاه"

categories_list = []
for row in range(len(df_test)):
    max = -12345678999
    category = ""
    for cat in range(len(bag_of_words)):
        prob = 0
        for word in function(df_test.loc[row]["description"]):
            if word in bag_of_words[cat]:
                result = bag_of_words[cat].count(word)
                prob += math.log10((result) / len(bag_of_words[cat]))
            else :
                prob += math.log10(0.1 / len(bag_of_words[cat]))
        if (prob > max):
            max = prob
            category = choose_category(cat)
    categories_list.append(category)
    print(category)


sum = 0
for i in range(len(df_test)):
    if df_test.loc[i]["categories"] == categories_list[i]:
        sum += 1
print((sum / 4.5))










