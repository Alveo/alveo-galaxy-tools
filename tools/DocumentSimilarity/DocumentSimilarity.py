'''
Created on Jul 1, 2017

@author: ruiwang
'''
import sys
from gensim import corpora, models, similarities
import argparse



def stop_err( msg ):
    sys.stderr.write( msg )
    sys.exit()


def arguments():
    parser = argparse.ArgumentParser(description="")
    parser.add_argument('--doc', required=True, action="store", type=str)
    parser.add_argument('--dataset', required=True, action="store", type=str)
    parser.add_argument('--dict', required=True, action="store", type=str)
    parser.add_argument('--corpus', required=True, action="store", type=str)
    parser.add_argument('--modelname', required=True, action="store", type=str)
    parser.add_argument('--model', required=True, action="store", type=str)
    parser.add_argument('--output', required=True, action="store", type=str)
    args = parser.parse_args()
    return args


               
def process(file, dict, dataset, corpus_name, model_name, input_model, output):

    dictionary = corpora.Dictionary.load(dict) 
    corpus = corpora.MmCorpus(corpus_name)
    
    if model_name == "lda":
        model = models.LdaModel.load(input_model)
    elif  model_name == "lsi":
        model = models.LsiModel.load(input_model)

    doc = open(file, 'r').read()
    vec_bow = dictionary.doc2bow(doc.lower().split())
    doc_vec_rep = model[vec_bow]

    
    index = similarities.MatrixSimilarity(model[corpus])

    sims = index[doc_vec_rep]
    sims = sorted(enumerate(sims), key=lambda item: -item[1])

    for i in sims:
        print i
            

    
    

if __name__ == "__main__":

    args = arguments()
    #the name of args.param has to be the same as the --arg_name, not after $
    process(args.doc, args.dict, args.dataset, args.corpus, args.modelname, args.model, args.output)
