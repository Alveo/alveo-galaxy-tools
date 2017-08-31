import nltk
from nltk.collocations import BigramCollocationFinder, BigramAssocMeasures
from nltk.collocations import TrigramCollocationFinder, TrigramAssocMeasures
import argparse


def Parser():
    the_parser = argparse.ArgumentParser(description="Parse the sentence using Chart Parser and a supplied grammar")
    the_parser.add_argument('--input', required=True, action="store", type=str, help="input text file")
    the_parser.add_argument('--output', required=True, action="store", type=str, help="output file path")
    the_parser.add_argument('--freq_filter', required=True, action="store", type=str, help="The minimum number of required occurrences in the corpus")
    the_parser.add_argument('--results', required=True, action="store", type=str, help="The maximum number of collocations to show in the results")
    the_parser.add_argument('--coll_type', required=True, action="store", type=str, help="Type of collocations to find")
    the_parser.add_argument('--pos', required=True, action="store", type=str, help="Data input is a set of POS tags")

    return the_parser.parse_args()


def collocation(inp, outp, freq_filter, results, coll_type, pos):
    pos = bool(pos == 'true')
    with open(inp, 'r') as fd:
        i = fd.read()

    all_words = []
    if pos:
        text = i.split(' ')[:-1]
        all_words = [x[0:x.index('/')] if x != '\n' else x for x in text]
        all_words = [x.strip(' ').strip('\n') for x in all_words]
    else:
        sents = nltk.sent_tokenize(i)
        for sent in sents:
            all_words += nltk.word_tokenize(sent)
    if coll_type == 'bigram':
        measures = BigramAssocMeasures()
        finder = BigramCollocationFinder.from_words(all_words)
    else:
        measures = TrigramAssocMeasures()
        finder = TrigramCollocationFinder.from_words(all_words)
    finder.apply_freq_filter(int(freq_filter))
    colls = finder.nbest(measures.pmi, int(results))
    with open(outp, 'w') as output:
        for coll in colls:
            output.write("%s\t%s" % coll)
            output.write('\n')


if __name__ == '__main__':
    args = Parser()

    collocation(args.input, args.output, args.freq_filter, args.results, args.coll_type, args.pos)
