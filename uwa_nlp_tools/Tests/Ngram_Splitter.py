'''
Created on 13 Jun 2016

@author: rui
'''
import nltk
import optparse
import sys


class Counter(dict):
    
    def add(self, other):
        for ngram in other.iterkeys():
            self[ngram] = self.get(ngram, 0) + other[ngram]   
            
            
class Ngrams():
    
    def split_into_unigrams(self, text):
        unigrams = []
        for token in nltk.word_tokenize(text):
            unigram = token
            if unigram:
                unigrams.append(unigram)
        return len(unigrams), unigrams
    
    
    def find_ngrams(self, text, length):
        counter = Counter()
        num_unigrams, unigrams = self.split_into_unigrams(text.lower())
        for i in xrange(num_unigrams):
            if (num_unigrams <= i + length - 1):
                break
            unigram_group = unigrams[i:i + length]
            #if not self.ngram_is_filtered(unigram_group):
            ngram = " ".join(unigram_group)
            counter[ngram] = counter.get(ngram, 0) + 1
        return counter
    
    def generate_ngram_word(self, min_num, n, text):
    
        ngram = []
        counter = Counter()
       
        
        for i in range(min_num, n):
            counter.add(self.find_ngrams(text, i))
        
        for n_gram, count in sorted(counter.items(), key=lambda x:x[1]):
            if count > 0:
                #print n_gram #, count
                ngram.append(n_gram.strip())
        return ngram
                    
    def get_grams(self, ngrams, n):
        grams = []
        for gram in ngrams:
            tokens = nltk.word_tokenize(gram)
            if len(tokens) == n:
                grams.append(gram)
        return grams
    

def stop_err( msg ):
    sys.stderr.write( msg )
    sys.exit()

   
if __name__ == "__main__":    
    
    usage = """%prog [options]
    
options (listed below) default to 'None' if omitted
    """
    parser = optparse.OptionParser(usage=usage)
    
    parser.add_option(
    '-f','--file',
    dest='input_txt',
    default = False,
    help='Name of file to be chopped. STDIN is default')
        
    options, args = parser.parse_args()
    invalid_starts = []

    if options.input_txt:
        infile = open ( options.input_txt, 'r')
    else:
        infile = sys.stdin
        


 
    for i, line in enumerate( infile ):
        line = line.rstrip( '\r\n' )
        if line:
                
            print line   
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    