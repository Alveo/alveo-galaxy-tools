'''
Created on 26 Feb. 2018

@author: rui
'''
import json
import collections
import nltk

TOKEN_FORMAT = "http://vocab.lappsgrid.org/Token"
SENTENCE_FORMAT = "http://vocab.lappsgrid.org/Sentence"

class LIF(object):
    def __init__(self, doc_text, views = None):
        
        self.dict = collections.OrderedDict()
        self.payload = collections.OrderedDict()
        self.payload["@context"] = "http://vocab.lappsgrid.org/context-1.0.0.jsonld"
        self.payload["metadata"] = {}
        
        text = collections.OrderedDict()
        text["@value"] = doc_text
        self.payload["text"] = text
        if views != None:
            self.payload["views"] = views
        
        
        #self.LIF = {}
        self.dict["discriminator"] = "http://vocab.lappsgrid.org/ns/media/jsonld#lif"
        self.dict["payload"] = self.payload
    
    def addViews(self, views):
        if views != None:
            self.payload["views"] = views 
        

class ViewObj(object):
    '''
    annotations is a list of Annotation objects
    '''
    def __init__(self, defination, producer, type, annotations):
        
        contains_properties = collections.OrderedDict()
        contains_properties["producer"] = producer
        contains_properties["type"] = type
        
        dict_contains = collections.OrderedDict()
        dict_contains[defination] = contains_properties
        
        metadata = collections.OrderedDict()
        metadata["contains"] = dict_contains
        
        
        self.viewObj = collections.OrderedDict()
        self.viewObj["metadata"] = metadata
        self.viewObj["annotations"] = annotations
    

class Annotation(object):
    '''
    features is a dictionary that contains annotations
    '''
    def __init__(self, id, start, end, type, features):
        self.annotation = collections.OrderedDict()
        self.annotation["id"] = id
        self.annotation["start"] = start
        self.annotation["end"] = end
        self.annotation["@type"] = type
        self.annotation["features"] = features

def get_word_position(doc_text):
    tok_offset = 0
    doc_tokens = collections.OrderedDict()
    tok_id = 0
    for tok in nltk.word_tokenize(doc_text):
        while doc_text[tok_offset] != tok[0]:
            tok_offset += 1

        length = len(tok)
        #print tok, tok_offset, tok_offset+ length
        doc_tokens[tok_id] = [tok, tok_offset, tok_offset+ length]
        tok_offset += length
        tok_id += 1
    return doc_tokens


def test():
    '''
    filename = "/Users/rui/Dropbox/Projects/Galaxy/LAPPSTest/Test1.txt"
    doc_text = open(filename, "r").read()
    #print doc_text
    doc_tokens = get_word_position(doc_text)
    #for k in doc_tokens.keys():
    #    print str(k) + " :" 
    #    print doc_tokens[k]

    annotations = []
    sentences = nltk.sent_tokenize(doc_text)   
    sent_id = 0
    tok_id = 0
    for sent in sentences:
        sent_toks = nltk.word_tokenize(sent)
        sent_tok_id = 0
        for tok in sent_toks:
            if tok == doc_tokens[tok_id][0]:
                
                id = "tok_" + str(sent_id) + "_" + str(sent_tok_id)
                start = doc_tokens[tok_id][1]
                end = doc_tokens[tok_id][2]
                type = "http://vocab.lappsgrid.org/Token"
                features = {}
                features["word"] = tok
                tok_annotation = Annotation(id, start, end, type, features)
                annotations.append(tok_annotation.annotation)
                sent_tok_id += 1
            tok_id += 1
        sent_tok_id += 1

    views = []
    view_obj = ViewObj("http://vocab.lappsgrid.org/Sentence",
                    "edu.brandeis.cs.lappsgrid.stanford.corenlp.Splitter:2.0.4",
                    "splitter:stanford",
                    annotations
                    )
    views.append(view_obj.viewObj)

    lif = LIF(doc_text)
    lif.addViews(views)
    
    dict_obj = lif.__dict__

    test = json.dumps(dict_obj)
    
    #print test
    '''
if __name__ == "__main__": 
    test()
