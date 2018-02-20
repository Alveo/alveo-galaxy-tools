'''
Created on 13Dec.,2016

@author: ruiwang
'''
import sys
import optparse
import os
import numpy
import time 
import nltk
import Helper as utility
import CValue as cvalue
from operator import itemgetter


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
        '-t','--toprank',
        dest='toprank',
        default = False,
        help='')
    

    options, args = parser.parse_args()
    exclude_line = str(options.exclude_line).strip()
    delimiter = chr( int( options.delimiter ) )
    toprank = int( options.toprank ) 
    
    if options.input_txt:

        infile = open ( options.input_txt, 'r')

        dict = {}
        for line in infile:
            line = line.rstrip( '\r\n' )
            if exclude_line and line.startswith(exclude_line): 
                continue
            nps = []
            if options.delimiter == 32:
                nps = nltk.word_tokenize(line)
            else:
                nps = line.split(delimiter)
                    
            for np in nps:
                if np:
                    if np in dict:
                        dict[np] += 1
                    else:
                        dict[np] = 1
        phrases = []           
        for d in dict:
            phrases.append((d, dict[d]))
        
        cv = cvalue.CValue_Processor()
        values = cv.compute_cvalue(phrases)
        result = sorted(values.iteritems(), key=itemgetter(1), reverse=True)
        i = 0
        for v in result:
            if i < toprank:
                print v[0] + "|" + str(v[1])
                i += 1
#this is the latest change
                
if __name__ == "__main__": main()


































