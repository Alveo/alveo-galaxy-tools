'''
Created on Jun 26, 2017

@author: ruiwang
'''
import sys
import gensim
import argparse
import Helper as utility


def stop_err( msg ):
    sys.stderr.write( msg )
    sys.exit()


def arguments():
    parser = argparse.ArgumentParser(description="Document summarisation using TextRank")
    parser.add_argument('--input', required=True, action="store", type=str, help="input text file")
    parser.add_argument('--ratio', required=True, action="store", type=str, help="ratio")
    parser.add_argument('--output', required=True, action="store", type=str, help="output file path")
    args = parser.parse_args()
    return args

def get_ratio(input2):
    try:
        return float(input2)
    except:
        return 0

def process(input_file, input_ratio, output):


    infile = open (input_file, 'r')
    rat = get_ratio(input_ratio)

    if rat > 0: 
        sents = ""
    
        for line in infile:
            line = utility.lemmatize_text(line.rstrip( '\r\n' ))
            if line:
                sents += line + ' '
        if sents:
            summ = gensim.summarization.summarize(sents, ratio=rat)  
            dict_f = open(output, 'a')  
            for s in summ:
                dict_f.write(s)       
            dict_f.close()
    else:
        raise ValueError('Invalid ratio, ratio needs to be float value that greater than 0 and less/equal to 1')
    

if __name__ == "__main__":

    args = arguments()
    #the name of args.param has to be the same as the --arg_name, not after $
    process(args.input, args.ratio, args.output)
