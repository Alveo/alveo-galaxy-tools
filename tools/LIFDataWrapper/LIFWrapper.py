'''
Created on 2 Apr. 2018

@author: rui
'''
import sys
#sys.path.append('../LAPPSPythonWrapper/')

import argparse
import os
import LIF_Format_Encoder as lif_encoder
import json
import optparse
import nltk

def main():
    usage = """%prog [options]
    
options (listed below) default to 'None' if omitted
    """
    parser = optparse.OptionParser(usage=usage)
    
    parser.add_option(
        '--input','--file',
        dest='input_txt',
        default = False,
        help='Name of file to be chopped. STDIN is default')
    
    parser.add_option(
        '-t','--is_tok',
        dest='is_tok',
        default = False,
        help='')
    
    
    parser.add_option(
        '-s','--is_sent',
        dest='is_sent',
        default = False,
        help='Name of file to be chopped. STDIN is default')
            

    options, args = parser.parse_args()

    
    if options.input_txt:
        #read the document
        doc_text = open(options.input_txt, "r").read()
        views = []
        
        if options.is_tok == 'true':
            doc_tokens = lif_encoder.get_word_position(doc_text)

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
                        tok_annotation = lif_encoder.Annotation(id, start, end, type, features)
                        annotations.append(tok_annotation.annotation)
                        sent_tok_id += 1
                    tok_id += 1
                sent_id += 1

            view_obj = lif_encoder.ViewObj(lif_encoder.TOKEN_FORMAT,
                            "UWA",
                            "splitter:nltk",
                            annotations
                            )
            views.append(view_obj.viewObj)
        
        if options.is_sent == 'true':
            doc_tokens = lif_encoder.get_word_position(doc_text)
            annotations = []
            sentences = nltk.sent_tokenize(doc_text)  

            start_tok_number = 0
            sent_id = 0
            for sent in sentences:
                id = 's' + str(sent_id)
                s_toks = nltk.word_tokenize(sent)
                
                start_tok_pos = doc_tokens[start_tok_number]
                end_tok_pos = doc_tokens[start_tok_number + len(s_toks)-1]
                type = "http://vocab.lappsgrid.org/Sentence"
                features = {}
                features["sentence"] = sent
                
                tok_annotation = lif_encoder.Annotation(id, start_tok_pos[1], end_tok_pos[2], type, features)
                annotations.append(tok_annotation.annotation)
                start_tok_number += len(s_toks)
                sent_id += 1
        
            view_obj = lif_encoder.ViewObj(lif_encoder.SENTENCE_FORMAT,
                            "UWA",
                            "splitter:nltk",
                            annotations
                            )
            views.append(view_obj.viewObj)
        
        lif = lif_encoder.LIF(doc_text)
        if views:
            lif.addViews(views)
        
        dict_obj = lif.dict
        json_objs = json.dumps(dict_obj)

        print (json_objs)

    

if __name__ == '__main__':
    main()

        
        
        
         
    
    
    
    
    

