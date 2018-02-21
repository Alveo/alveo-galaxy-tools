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
from nltk.tag.stanford import StanfordPOSTagger


    
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
        '-j','--java_path',
        dest='java_path',
        default = False,
        help='default java path')
       
    
    parser.add_option(
        '-t','--tagger_file',
        dest='tagger_file',
        default = False,
        help='Stanford tagger file')
        
        
    parser.add_option(
        '-s','--jar_file',
        dest='jar_file',
        default = False,
        help='Stanford tagger jar')
    
    parser.add_option(
        '-e','--exclude_line',
        dest='exclude_line',
        default = False,
        help='')
            
    parser.add_option(
        '-w','--wordtag_delimiter',
        dest='wordtag_delimiter',
        default = False,
        help='')
            
    options, args = parser.parse_args()

    java_path = str(options.java_path)
    tagger = str(options.tagger_file)
    postagger = str(options.jar_file)
    exclude_line = str(options.exclude_line)
    wordtag_delimiter = chr( int( options.wordtag_delimiter ) )

    os.environ['JAVAHOME'] = java_path
    st = StanfordPOSTagger(tagger, postagger)
    
    
    if options.input_txt:
        #nltk.download()
        infile = open ( options.input_txt, 'r')

        
        for line in infile:
            line = line.rstrip( '\r\n' )
            
            if line.startswith(exclude_line): 
                print line + "\n"
                continue
            
            toks = nltk.word_tokenize(line)
            postoks = st.tag(toks) 
            str_d = ""
            for w in postoks:
                str_d += w[0]+ wordtag_delimiter + w[1] + " "
            print str_d + "\n"
            
        


if __name__ == "__main__": main()









