'''
Created on Jun 26, 2017

@author: ruiwang
'''
import sys
import optparse
import nltk
import gensim
from nltk.tokenize import RegexpTokenizer

def stop_err( msg ):
    sys.stderr.write( msg )
    sys.exit()



class MySentences(object):
    def __init__(self, filenames):
        self.filenames = filenames
 
    def __iter__(self):
        for fname in self.filenames:
            for line in open(fname):
                yield nltk.word_tokenize(line)


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
        '-s','--size',
        dest='size',
        default = False,
        help='')

    parser.add_option(
        '-w','--window',
        dest='window',
        default = False,
        help='')

    parser.add_option(
        '-m','--min',
        dest='min',
        default = False,
        help='')
    
    parser.add_option(
        '-o','--output',
        dest='output',
        default = False,
        help='')
    
    options, args = parser.parse_args()
    
    input = options.input_txt
   
    size = int(options.size)
    window = int(options.window)
    min = int(options.min)

    out_file = options.output    

    sentences = MySentences(input.split(","))

    model = gensim.models.Word2Vec(sentences, size=size, window=window, min_count=min)
    model.save(out_file)
    
    
    #s = model['eye'] 
    #print s

if __name__ == "__main__":

    process()
    
    
    