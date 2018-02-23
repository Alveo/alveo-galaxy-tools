'''
Created on 06/03/2014

@author: rui
'''
import nltk


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

