'''
Created on 06/03/2014

@author: rui
'''
import nltk
import re
import string
import os
import unicodedata
import codecs

def read_file_line_by_line(filePath):
    f = open(filePath, "r")
    lines = f.readlines()
    lowerLines = []
    for line in lines:
        line = line.decode('utf-8', 'ignore')
        lowerLines.append(line.lower())
    return lowerLines

def readFileLineByLineKeepOrginal(filePath):
    f = open(filePath, "r")
    lines = f.readlines()
    file_lines = []
    for line in lines:
        file_lines.append(line.strip())
    return file_lines

def read_file_to_string(filePath):
    f = open(filePath, 'r')
    rawText = f.read()
    rawText = rawText.decode('utf-8', 'ignore')
    return rawText.lower()

def read_french_file_to_string_NFD(filePath):
    f = codecs.open(filePath, encoding='ISO-8859-1').read()
    #rawText = f.read()
    #rawText = rawText.decode('utf-8-sig')

    rawText = f.lower()
    
    rawText = rawText.encode("utf-8")
    rawText = rawText.decode("utf-8")
    
    
    #rawText = unicodedata.normalize('NFD', rawText)
    return rawText


def read_french_file_to_string_Uni(filePath):
    
    f = open(filePath, 'r')
    rawText = f.read()
    rawText = rawText.lower()
    rawText = rawText.decode('utf-8', 'ignore')
    rawText = rawText.replace(u'\ufeff', '')

    #rawText = unicodedata.normalize('NFD', rawText)
    return rawText

def read_french_file_to_line_Uni(filePath):
    
    f = open(filePath, 'r')
    rawText = f.readlines()
    lines = []
    for l in rawText:
        l = l.lower()
        l = l.decode('utf-8', 'ignore')
        l = l.replace(u'\ufeff', '')
        lines.append(l)

    #rawText = unicodedata.normalize('NFD', rawText)
    return lines

def read_file_line_by_line_french(filePath):
    f = codecs.open(filePath, encoding='ISO-8859-1').readlines()
    #rawText = f.read()
    #rawText = rawText.decode('utf-8-sig')
    text = ''
    for rawText in f:
        rawText = rawText.lower()
        
        #rawText = rawText.encode("utf-8")
        rawText = rawText.decode("utf-8")
        text += rawText.replace('\r\n', '') + " "
    
    #rawText = unicodedata.normalize('NFD', rawText)
    return text

def stemming_tokens_with_wordNetLemmatizer(tokens):
    stemmed = []
    lemmatizer = nltk.stem.WordNetLemmatizer()
    #lemmatizer = nltk.stem.PorterStemmer()
    for token in tokens:
        w= lemmatizer.lemmatize(token)
        #w= lemmatizer.stem(token)
        stemmed.append(w)
    return stemmed

def stemming_tokens_with_porter(tokens):
    stemmed = []
    #lemmatizer = nltk.stem.WordNetLemmatizer()
    lemmatizer = nltk.stem.PorterStemmer()
    for token in tokens:
        #w= lemmatizer.lemmatize(token)
        w= lemmatizer.stem(token)
        stemmed.append(w.strip())
    return stemmed

def stemming_tokens_french(tokens):
    stemmed = []
    #lemmatizer = nltk.stem.WordNetLemmatizer()
    lemmatizer = nltk.stem.snowball.FrenchStemmer()
    for token in tokens:
        #w= lemmatizer.lemmatize(token)
        w= lemmatizer.stem(token)
        stemmed.append(w)
    return stemmed

def stemming_text_with_porter(text):
    tokens = nltk.word_tokenize(text)
    tokens = stemming_tokens_with_porter(tokens)
    return tokens_to_text(tokens)

def stemming_text_french(text):
    tokens = nltk.WhitespaceTokenizer().tokenize(text)
    tokens = stemming_tokens_french(tokens)
    return tokens_to_text(tokens)

def stemming_candidate_phrase_porter(lists):
    returnList = []
    for l in lists:
        phrase_list = []
        for phrase in l:
            phrase_list.append(stemming_text_with_porter(phrase))
        returnList.append(phrase_list)
    return returnList

def stemming_candidate_phrase_french(lists):
    returnList = []
    for l in lists:
        phrase_list = []
        for phrase in l:
            phrase_list.append(stemming_text_french(phrase))
        returnList.append(phrase_list)
    return returnList

lemmatizer = nltk.stem.WordNetLemmatizer()
def lemmatize_tokens(tokens):
    stemmed = []

    for token in tokens:
        w= lemmatizer.lemmatize(token)
        stemmed.append(w.strip())
    return stemmed


def lemmatize_text(text):
    tokens = nltk.word_tokenize(text)
    tokens = lemmatize_tokens(tokens)
    return tokens_to_text(tokens)



def lemmatize_candidate_phrase(lists):
    returnList = []
    for l in lists:
        phrase_list = []
        for phrase in l:
            phrase_list.append(lemmatize_text(phrase))
        returnList.append(phrase_list)
    return returnList

def tokens_to_text(tokens):
    text = ""
    for token in tokens:
        text += " " + token
    return text.strip()

def is_punct(word):
    return len(word) == 1 and word in string.punctuation

def get_punct():
    return string.punctuation
           
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def customized_punct_marks():
    chars = []
    for p in get_punct():
        if not p == '-':
            chars.append(p)
    chars.append("\''")
    return chars

def stop_words():
    return nltk.corpus.stopwords.words('english')


def sentences_to_text(sentences):
    text_list = []
    for text in sentences:
        none_space_char = [w for w in text if w]
        text_list += none_space_char
    return text_list

def strip_list_of_string(list_string):
    returnList = []
    for l in list_string:
        returnList.append(l.strip())
    return returnList