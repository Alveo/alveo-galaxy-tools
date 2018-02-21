'''
Created on 12 Oct 2016

@author: rui
'''
import sys
import optparse
import nltk
import string
import Helper as utility
import argparse


#--input $input1 --stopword $input2 --number $input3 --symbol $input4 --line $input5

def stop_err( msg ):
    sys.stderr.write( msg )
    sys.exit()

    
def main():
    
#-f $input1 -e '$exclude_line' -s $stopword -n $number -q $symbol
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
        '-s','--stopword',
        dest='stopword',
        default = False,
        help='')
    
    parser.add_option(
        '-n','--number',
        dest='number',
        default = False,
        help='')
    
    parser.add_option(
        '-q','--symbol',
        dest='symbol',
        default = False,
        help='')
    
        
    options, args = parser.parse_args()
    
    exclude_line = str(options.exclude_line)

    ex_stopword = options.stopword
    ex_num = options.number
    ex_symb = options.symbol

    stopwords = nltk.corpus.stopwords.words('english')

    if options.input_txt:

        infile = open ( options.input_txt, 'r')

        for line in infile:

            line = line.rstrip( '\r\n' )
            if line.startswith(exclude_line): 
                print line
            else:
                sent = nltk.sent_tokenize(line)
                for s in sent:
                    
                    words = nltk.word_tokenize(s.lower())
        
                    if ex_stopword:
                        words = [w for w in words if w not in stopwords]
                    if ex_num:
                        words = [w for w in words if not w.isdigit()]
                    if ex_symb:
                        words = [w for w in words if w not in string.punctuation]
                    
                    sent_txt = utility.tokens_to_text(words) + " ."
                    print sent_txt + "\n"    
    
    

if __name__ == '__main__':main()





























