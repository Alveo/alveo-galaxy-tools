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
import HTMLParser


def stop_err( msg ):
    sys.stderr.write( msg )
    sys.exit()

class NPChunker():

        
    def init(self, raw_text, wordtag_delimiter):
        self.Text = raw_text
        self.punct = utility.customized_punct_marks()
        self.wordtag_delimiter = wordtag_delimiter
        
    def tree(self, text_segment):
        grammar = "NP: {<JJ>*<NN.*>+}"

        
        chunker = nltk.RegexpParser(grammar)
        tagged_token = [ ]
        tokens = nltk.word_tokenize(text_segment)
        for t in tokens:
            t = t.split(self.wordtag_delimiter)
            if (len(t) == 2):
                if str(t[1]):
                    tagged_token.append((str(t[0]), str(t[1].upper())))
        
        tree = chunker.parse(tagged_token)
        return tree 

    
    
 
    def leaves(self, tree):
        for subtree in tree.subtrees(filter = lambda t: t.label()=='NP'):
            yield subtree.leaves()
     
     
    def acceptable_word(self, word):
        accepted = bool(2 <= len(word) <= 40
        and word not in utility.stop_words())
        return accepted
     

    def get_np_terms(self, text_segment):
        if text_segment:
            for leaf in self.leaves(self.tree(text_segment)):
                term = [ w for w, t in leaf if self.acceptable_word(w) ]
                yield term
 

    def get_candidates(self):
        np = []
        unstemmed = []

        for sent in self.Text: 
            sent_terms = []
            se = ""
            sent = sent.split(" ")
            for s in sent:
                sub = s.split(self.wordtag_delimiter)
                if len(sub) == 2:
                    if sub[1] in self.punct:
                        se += sub[0]+self.wordtag_delimiter+"PUNCT" + " "
                    else: se += s + " "
                    
            terms = self.get_np_terms(se.strip()) 
            for term in terms:
                sent_terms.append(utility.tokens_to_text(term))
            np.append(sent_terms)
            unstemmed.append(sent_terms)
        #self.Text.STEMMED_CANDIDATED_SENTENCES = utility.stemming_candidate_phrase_porter(np)

        return np
    
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
        '-r','--reg_exp',
        dest='reg_exp',
        default = False,
        help='')
    
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

    parser.add_option(
        '-p','--phrase_delimiter',
        dest='phrase_delimiter',
        default = False,
        help='')
    
    options, args = parser.parse_args()
    
    exclude_line = str(options.exclude_line)
    wordtag_delimiter = chr( int( options.wordtag_delimiter ) )
    phrase_delimiter  = chr( int( options.phrase_delimiter ) )
    
    if options.input_txt:


        infile = open ( options.input_txt, 'r')
        raw_text = []
        
        for line in infile:
            line = line.rstrip( '\r\n' )
            if line.startswith(exclude_line): 
                print line + "\n"
                continue    

            raw_text.append(line)

            chunker = NPChunker()
            chunker.init(raw_text, wordtag_delimiter)
            nps_sent = chunker.get_candidates()
            for nps in nps_sent:
                if nps:
                    sent = ""
                    for np in nps:
                        sent += np + phrase_delimiter
                    print sent.strip(phrase_delimiter)
            raw_text = []
            

if __name__ == "__main__": main()



























