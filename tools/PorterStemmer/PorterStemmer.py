'''
Created on 13Dec.,2016

@author: ruiwang
'''
'''
Created on 27 Oct 2016

@author: rui
'''
import sys
import optparse
import os
import numpy
import time 
import nltk
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
        '-f','--file',
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
        '-s','--stemmer',
        dest='stemmer',
        default = False,
        help='')
    
    
    options, args = parser.parse_args()
    
    exclude_line = str(options.exclude_line)

    delimiter = chr( int( options.delimiter ) )
    
    stemmer =  str(options.stemmer)

    if options.input_txt:

        infile = open ( options.input_txt, 'r')

        for line in infile:
            line = line.rstrip( '\r\n' )
            if line.startswith(exclude_line): 
                print line + "\n"
                continue    
            phrases = []
            if options.delimiter == 32:
                phrases = nltk.word_tokenize(line)
            else:
                phrases = line.split(delimiter)
            
            stemm_line = ""
            for p in phrases:
                stemmed = ''
                if stemmer == "porter":
                    stemmed = utility.stemming_text_with_porter(p)    
                elif stemmer == "lem":
                    stemmed = utility.lemmatize_text(p)
                if stemmed:
                    stemm_line += stemmed + delimiter
            print stemm_line + '\n'  
                
            

if __name__ == "__main__": main()







