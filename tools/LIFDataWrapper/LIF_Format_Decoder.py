'''
Created on 30 Mar. 2018

@author: rui
'''
import json
import collections
from LIF_Format_Encoder import TOKEN_FORMAT
from LIF_Format_Encoder import SENTENCE_FORMAT


        
def read_LIF(lif_string):
    
    lif_obj = json.loads(lif_string)
    return lif_obj
    
def get_text(lif_obj):
    text = lif_obj["payload"]["text"]["@value"]
    return text

def get_tokens(lif_obj):
    views = lif_obj["payload"]["views"]
    token_annotation = []
    tokens = []
    for element in views:
        for sub_ele in element["metadata"]["contains"]:
            if sub_ele == TOKEN_FORMAT:
                token_annotation = element["annotations"]
    
    for element in token_annotation:
        tokens.append(element)
    
    return tokens
    
def get_sentences(lif_obj):
    views = lif_obj["payload"]["views"]
    token_annotation = []
    tokens = []
    for element in views:
        for sub_ele in element["metadata"]["contains"]:
            if sub_ele == SENTENCE_FORMAT:
                token_annotation = element["annotations"]
    
    for element in token_annotation:
        tokens.append(element["features"]["sentence"])
            
    return tokens
    



def test():
    filename = "/Users/rui/Dropbox/Projects/Galaxy/LAPPSTest/MyGen1.lif"
    lif_string = open(filename, "r").read()
    lif_obj = read_LIF(lif_string)
    views =  lif_obj["payload"]["views"]
    
    #print lif_obj["payload"]["text"]["@value"]

    token_annotation = []
    for element in views:
        for sub_ele in element["metadata"]["contains"]:
            if sub_ele == SENTENCE_FORMAT:
                token_annotation = element["annotations"]
    
    #for element in token_annotation:
        #print element["features"]["word"]
                
                
if __name__ == "__main__": 
    test()

