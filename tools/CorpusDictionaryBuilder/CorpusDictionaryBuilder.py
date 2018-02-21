'''
Created on Jun 26, 2017

@author: ruiwang
'''
import sys
import optparse
import os
import nltk
from gensim import corpora, models, similarities
import gensim
from operator import itemgetter
import argparse
from nltk.tokenize import RegexpTokenizer


def stop_err( msg ):
    sys.stderr.write( msg )
    sys.exit()


def arguments():
    parser = argparse.ArgumentParser(description="Document summarisation using TextRank")
    parser.add_argument('--input', required=True, action="store", type=str, help="input text file")
    parser.add_argument('--output', required=True, action="store", type=str, help="output file path")
    args = parser.parse_args()
    return args


def process(input, output):


    infile = open ( input, 'r')
    sents = []
    for line in infile:
        line = line.rstrip( '\r\n' )
        sents.append(line)
    
    
    tokenizer = RegexpTokenizer(r'\w+')    
    texts = []    
    for i in sents:
        raw = i.lower()
        tokens = tokenizer.tokenize(raw)
        texts.append(tokens)           
        
    dictionary = corpora.Dictionary(texts)  
    dictionary.save(output)
    

if __name__ == "__main__":

    args = arguments()
    #the name of args.param has to be the same as the --arg_name, not after $
    process(args.input, args.output)
