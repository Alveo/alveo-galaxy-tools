'''
Created on Jun 25, 2017

@author: ruiwang
'''

import nltk
import Helper as utility
import numpy as np
from operator import itemgetter

class CValue_Processor():


    def get_longest_length(self, candidate_tupe):
        t = 1
        for c in candidate_tupe:
            tok_length = len(nltk.word_tokenize(c[0]))
            if t < tok_length:
                t = tok_length
        return t
    
    def compute_cvalue(self, candidates):
        local_dict = {}
        longest = self.get_longest_length(candidates)
        for c in candidates:
            toks_length = len(nltk.word_tokenize(c[0])) 
            if toks_length == longest and c[0] not in local_dict:
                local_dict[c[0]] = np.log2(toks_length)*int(c[1])
            elif c[0] not in local_dict:
                fa = int(c[1])
                ta = 0
                pt = 0
                for cc in candidates:
                    if cc[0] != c[0] and c[0] in cc[0]:
                        pt += 1
                        ta += cc[1]
                        fa += cc[1] # all frequency is abs account
                if pt > 0:
                    local_dict[c[0]] = np.log2(toks_length) * (fa - (ta/pt))  
                else:
                    log2_a = np.log2(toks_length)
                    local_dict[c[0]] = log2_a*int(c[1])
  
        return local_dict
    
    def get_phrase(self, phrase):
        new_phrases = []
        if phrase in self.cvalue:
            candidates = self.cvalue[phrase]
            if len(candidates) > 1:
                phrase_dict = self.compute_cvalue(phrase, candidates)
                phrase_sorted = sorted(phrase_dict.iteritems(), key=itemgetter(1), reverse=True)

                for p in phrase_sorted:
                    if p[0] != phrase and p[0] in phrase and phrase_dict[p[0]] > phrase_dict[phrase]:
                        new_phrases.append(p[0])
                        sub_phrases = phrase.split(p[0])
                        
                        for ph in sub_phrases:
                            if ph.strip():
                                #if (len(nltk.word_tokenize(ph)) > 1):
                                    #print "stop"
                                new_phrases += self.get_phrase(ph.strip())
                            
                if new_phrases:    
                    return new_phrases
                else:
                    return [phrase]
            else:
                return [phrase]
        else:
            return [phrase]
            
          
    def process_np(self, sentences):
        new_sents = []
        
        for sent in sentences:
            
            new_sent = []
            for phrase in sent:
                toks = nltk.word_tokenize(phrase)
                
                if len(toks) > 2:
                    p = utility.lemmatize_text(phrase)
                    new_sent += self.get_phrase(p)
                else:
                    new_sent.append(phrase)
            new_sents.append(new_sent)
                
        return new_sents    
        

        
if __name__ == '__main__':  
    dataset = ""
    cvalue = CValue_Processor()
    candidates = [("RECURRENT BASAL CELL CARCINOMA", 5),
                  ("CYSTIC BASAL CELL CARCINOMA", 6),
                  ("ULCERATED BASAL CELL CARCINOMA", 7),
                  ("ADENOID CYSTIC BASAL CELL CARCINOMA", 5),
                  ("CIRCUMSCRIBED BASAL CELL CARCINOMA", 3),
                  ("BASAL CELL CARCINOMA", 958),
                  ]
    values = cvalue.compute_cvalue(candidates)
    for v in values:
        print v + "    " + str(values[v])
    