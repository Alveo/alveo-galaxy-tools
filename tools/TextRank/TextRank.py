'''
Created on 13Dec.,2016

@author: ruiwang
'''
import sys
import optparse
import nltk
from GraphBuilder import GraphBuilder
import networkx as netx
from operator import itemgetter

def stop_err( msg ):
    sys.stderr.write( msg )
    sys.exit()



def get_candidates(sents):


    text = []
    for s in sents:
        sent = []
        for np in s:
            if np:
                sent.append(np)
        text.append(sent)
    return text

def get_ranking_results(stem_text):
        
    extractedkeyword = [] 
    graph = GraphBuilder()
    g = graph.build_unweight_graph(stem_text)

    try:
        x = netx.pagerank(g, max_iter=30,tol=1.0e-4)
        result = sorted(x.iteritems(), key=itemgetter(1), reverse=True)
        for r in result:
            extractedkeyword.append(r[0])
        return extractedkeyword, result
    except:
        return None, None

def run_Textrank(doc_sents, toprank):
    text = get_candidates(doc_sents)
    extractedkeyword, result = get_ranking_results(text)
    i = 0
    for r in result:
        if i < toprank:
            i += 1
            print r[0] + "|" + str(r[1])

 
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
        doc_sents = []
        for line in infile:
            line = line.rstrip( '\r\n' )
            if exclude_line and line.startswith(exclude_line): 
                if doc_sents:
                    run_Textrank(doc_sents, toprank)
                    doc_sents = []
                print line + "\n"
            else:
                phrases = []
                if options.delimiter == 32:
                    phrases = nltk.word_tokenize(line)
                else:
                    phrases = line.split(delimiter)
                doc_sents.append(phrases)   
                   
        if doc_sents:  
            run_Textrank(doc_sents, toprank)
   
                
            
                

if __name__ == "__main__": main()
















