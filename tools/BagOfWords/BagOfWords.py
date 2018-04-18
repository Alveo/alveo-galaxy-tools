'''
Created on 12 Oct 2016

@author: rui
'''
import sys
import optparse
import nltk
import string
import Helper as utility
import LIF_Format_Encoder as lif_encoder
import LIF_Format_Decoder as lif_decoder
import json
from nltk.tag.stanford import StanfordPOSTagger
import os

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
    
    #   LowerCase_Casting.py -f $input1 -s $stopword -n $number -q $symbol 
    #   -lem $lemmatisation -stem $stemming -pos $pos$> $out_file1

    parser.add_option(
        '-f','--file',
        dest='input_txt',
        default = False,
        help='Name of file to be chopped. STDIN is default')

    parser.add_option(
        '--low','--low',
        dest='low',
        default = False,
        help='')
    
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
        '-c','--customised_stopwords',
        dest='customised_stopwords',
        default = False,
        help='')    
    parser.add_option(
        '-n','--number',
        dest='number',
        default = False,
        help='')
    
    parser.add_option(
        '-q','--punct',
        dest='punct',
        default = False,
        help='')

    parser.add_option(
        '--lem','--lemmatisation',
        dest='lemmatisation',
        default = False,
        help='')
    
    parser.add_option(
        '--stem','--stemming',
        dest='stemming',
        default = False,
        help='')
    
    parser.add_option(
        '--pos','--pos',
        dest='pos',
        default = False,
        help='')
    
    ########################################
        
    options, args = parser.parse_args()
    

    low = options.low
    ex_stopword = options.stopword
    ex_num = options.number
    ex_punct = options.punct
    
    is_lem = options.lemmatisation
    is_stem = options.stemming
    is_pos = options.pos
    customised_stopwords = options.customised_stopwords

    stopwords = nltk.corpus.stopwords.words('english') + customised_stopwords.strip().split(',')

    if options.input_txt:

        infile = open ( options.input_txt, 'r').read()
        lif_obj = lif_decoder.read_LIF(infile)
        tokens = lif_decoder.get_tokens(lif_obj)
        
        if low == 'true':
            for t in tokens:
                t['features']['word'] = t['features']['word'].lower()   
                t['features']['tokenType'] = 'word'         
        
        if ex_stopword == 'true':
            for t in tokens:
                if t['features']['word'] in stopwords:
                    t['features']['tokenType'] = "stopword"
        if ex_num == 'true':
            for t in tokens:
                if t['features']['word'].isdigit():
                    t['features']['tokenType'] = "number"
        if ex_punct == 'true':
            for t in tokens:
                if t['features']['word'] in string.punctuation:
                    t['features']['tokenType'] = "punctuation"
        
        if is_lem == 'true':
            lemmatizer = nltk.stem.WordNetLemmatizer()
            for t in tokens:
                t['features']['lemma'] = lemmatizer.lemmatize( t['features']['word'])
        if is_stem == 'true':
            stemmer = nltk.stem.PorterStemmer()
            for t in tokens:
                t['features']['stem'] = stemmer.stem( t['features']['word'])
        if is_pos == 'true':

            os.environ['JAVAHOME'] = '/usr/bin/java'
            st = StanfordPOSTagger('/Users/rui/Lib/english-left3words-distsim.tagger', '/Users/rui/Lib/stanford-postagger.jar')
            current_sent_id = 0
            current_sent_toks = []
            for i in range(len(tokens)):
                sent_id = int(tokens[i]['id'].split('_')[1])
                if current_sent_id == sent_id:
                    current_sent_toks.append(tokens[i])
                if ((i+1) == len(tokens) or current_sent_id != sent_id):
                    sent_tok = [x['features']['word'] for x in current_sent_toks]
                    postoks = st.tag(sent_tok) 
                    for j in range(len(current_sent_toks)):
                        current_sent_toks[j]['features']['pos'] = postoks[j][1]
                    current_sent_id += 1
                    current_sent_toks = []
                    current_sent_toks.append(tokens[i])
            
        print (json.dumps(lif_obj))           
    
'''
def test():
    filename = "/Users/rui/Dropbox/Projects/Galaxy/LAPPSTest/a.txt"
    lif_string = open(filename, "r").read()
    lif_obj = lif_decoder.read_LIF(lif_string)
    views =  lif_obj["payload"]["views"]
    
    tokens = lif_decoder.get_tokens(lif_obj)

    os.environ['JAVAHOME'] = '/usr/bin/java'
    st = StanfordPOSTagger('/Users/rui/Lib/english-left3words-distsim.tagger', '/Users/rui/Lib/stanford-postagger.jar')
    current_sent_id = 0
    current_sent_toks = []
    print len(tokens)
    for i in range(len(tokens)):
        print i
        print tokens[i]
        sent_id = int(tokens[i]['id'].split('_')[1])
        if current_sent_id == sent_id:
            current_sent_toks.append(tokens[i])
        if ((i+1) == len(tokens) or current_sent_id != sent_id):
            print current_sent_toks
            sent_tok = [x['features']['word'] for x in current_sent_toks]
            postoks = st.tag(sent_tok) 
            for j in range(len(current_sent_toks)):
                current_sent_toks[j]['features']['pos'] = postoks[j][1]
            current_sent_id += 1
            current_sent_toks = []
            current_sent_toks.append(tokens[i])
        
    
    print json.dumps(lif_obj)
'''
if __name__ == '__main__':main()





























