'''
Created on Jun 26, 2017

@author: ruiwang
'''

import sys
import optparse
import nltk
import gensim 
from nltk.tokenize import RegexpTokenizer
import Helper as utility

def stop_err( msg ):
    sys.stderr.write( msg )
    sys.exit()



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
        '-t','--topnum',
        dest='topnum',
        default = False,
        help='')
    
    parser.add_option(
        '-l','--tab_file',
        dest='tab_file',
        default = False,
        help='')
    
    parser.add_option(
        '-m','--tab_file2',
        dest='tab_file2',
        default = False,
        help='')
    
    parser.add_option(
        '-o','--tab_file3',
        dest='tab_file3',
        default = False,
        help='')
    
    options, args = parser.parse_args()
    
    input = options.input_txt
    exclude_line = str(options.exclude_line).strip()
    topics = int(options.topnum)
    delimiter = chr( int( options.delimiter ) )
    lda_out = options.tab_file
    matrix_out = options.tab_file2
    out_file = options.tab_file3
    
    
    if topics > 0:
        infile = open ( input, 'r')
        documents = []
        current_doc = []
        for line in infile:
            line = line.rstrip( '\r\n' )
            if exclude_line and line.startswith(exclude_line): 
                if current_doc:
                    documents.append(current_doc)
                    current_doc = []
                    continue
            else:
                sentence = []
                if options.delimiter == 32:
                    sentence = nltk.word_tokenize(line)
                else:
                    sentence = line.split(delimiter)
                current_doc += sentence
        if current_doc:
            documents.append(current_doc)
        
        dictionary = gensim.corpora.Dictionary(documents)      
        corpus = [dictionary.doc2bow(text) for text in documents]
        
        gensim.corpora.MmCorpus.serialize(matrix_out, corpus)    
        
        mm_corpus = gensim.corpora.MmCorpus(matrix_out)
        
        ldamodel = gensim.models.ldamodel.LdaModel(mm_corpus, num_topics=topics, 
                                                   id2word = dictionary, update_every=1, chunksize=2, passes=1)      
        ldamodel.save(lda_out)
        
        dict_f = open(out_file, 'a')
        
        topics_matrix = ldamodel.show_topics(formatted=False, num_words=20)
        
        topic_id = 0
        for t in topics_matrix:
            topic_id += 1
            
            tps = t
            #print tps
            dict_f.write("topic -- " + str(topic_id) + ' top 20 topical words \n')
            for wd in tps:
                print"-----"
                print wd
                dict_f.write( wd[1] )
                dict_f.write( " ; " )
            dict_f.write('\n')
            
        #for t in topics_matrix:
        #    topic_id = t[0]
        #    tps = t[1]
        #    dict_f.write("topic -- " + str(topic_id) + 'top 20 topical words \n')
        #    for wd in tps:
        #        dict_f.write( wd[0] + " ")
        #    dict_f.write('\n')

    
        for doc in documents:
            dict_f.write(exclude_line + '\n')
            doc_text = utility.tokens_to_text(doc)
            sents = nltk.sent_tokenize(doc_text)
            for s in sents:
                dict_f.write(s + '\n')
            test_doc_vec = dictionary.doc2bow(doc) 
            topics_list = ldamodel[test_doc_vec]
            for t in topics_list:
                dict_f.write('topic number: ' + str(t[0]) + "    probability: " + str(t[1]) + '\n')
            

        dict_f.close()
    else:
        raise ValueError('Invalid number of topics')
       

if __name__ == "__main__":
    process()
    
    
    
    
    
    
    
    