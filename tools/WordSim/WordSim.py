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
from gensim.models.keyedvectors import KeyedVectors


def stop_err( msg ):
    sys.stderr.write( msg )
    sys.exit()



class MySentences(object):
    def __init__(self, filenames):
        self.filenames = filenames
 
    def __iter__(self):
        for fname in self.filenames:
            for line in open(fname):
                yield line.split()


def process():
    usage = """%prog [options]
    
options (listed below) default to 'None' if omitted
    """
    parser = optparse.OptionParser(usage=usage)
    
    parser.add_option(
        '-f','--input1',
        dest='input_txt',
        default = False,
        help='Name of file to be chopped. STDIN is default')
    
    parser.add_option(
        '-e','--equ',
        dest='equ',
        default = False,
        help='')

    
    options, args = parser.parse_args()
    
    input = options.input_txt
    #print input
    equation = options.equ
    
    model =  gensim.models.Word2Vec.load(input) 

    #print  model.wv['patient'] 
    print model.wv.most_similar(positive=['lady', 'eye'], negative=['man'])
    #word_vectors.similarity('lady', 'patient')

if __name__ == "__main__":
    process()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    