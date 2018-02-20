'''
Created on Jun 25, 2017

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
import Helper as utility

def stop_err( msg ):
    sys.stderr.write( msg )
    sys.exit()


    
def main():
    


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
        '-e','--exclude_line',
        dest='exclude_line',
        default = False,
        help='')

    parser.add_option(
        '-d','--delimiter',
        dest='delimiter',
        default = False,
        help='')
    
    parser.add_option(
        '-t','--toprank',
        dest='toprank',
        default = False,
        help='')
    
    parser.add_option(
        '-o','--output',
        dest='output',
        default = False,
        help='')
    
    options, args = parser.parse_args()
        
    exclude_line = str(options.exclude_line).strip()
    
    delimiter = chr( int( options.delimiter ) )

    toprank = int( options.toprank ) 
    
    output = str(options.output).strip()
    
    if options.input_txt:
        infile = open ( options.input_txt, 'r')
        documents = []
        current_doc = []
        for line in infile:
            line = line.rstrip( '\r\n' )
            if exclude_line and line.startswith(exclude_line): 
                if current_doc:
                    documents.append(current_doc)
                    current_doc = []
                    continue
            else:
                sentence = []
                if options.delimiter == 32:
                    sentence = nltk.word_tokenize(line)
                else:
                    sentence = line.split(delimiter)
                current_doc += sentence
        if current_doc:
            documents.append(current_doc)

        dictionary = corpora.Dictionary(documents)      
        corpus = [dictionary.doc2bow(text) for text in documents]
        tfidf_model = gensim.models.TfidfModel(corpus, id2word=dictionary)
        #tfidf_model.save(output)
        dict_f = open(output, 'a')  
        for doc in documents:
            #print doc
            dict_f.write(exclude_line + "\n")
            doc_text = utility.tokens_to_text(doc)
            dict_f.write("document nouns & noun phrases" + '\n')
            dict_f.write(doc_text + '\n')
            #dict_f.write(doc + '\n')
            test_doc_vec = dictionary.doc2bow(doc) 
            
            tfidf_score = tfidf_model[test_doc_vec]   
            print tfidf_score
            result = sorted(tfidf_score, key=lambda x: x[1], reverse=True)
            i = 0
            for id, score in result:
                if i < toprank:
                    dict_f.write(dictionary.get(id) + "|" + str(score) + "\n")
                    i += 1
        dict_f.close()
    
                

if __name__ == "__main__": main()


