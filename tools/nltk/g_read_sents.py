
import os
import nltk
from nltk.corpus import PlaintextCorpusReader
import argparse

nltk.download('punkt', quiet=True)


def Parser():
    the_parser = argparse.ArgumentParser(description="Segments the text input into separate sentences")
    the_parser.add_argument('--input', required=True, action="store", type=str, help="input text file")
    the_parser.add_argument('--output', required=True, action="store", type=str, help="output file path")

    args = the_parser.parse_args()
    return args


def print_out(outp, sentences):
    with open(outp, 'w') as output:
        for sent in sentences:
            for tok in sent:
                output.write(tok)
                output.write(' ')
            output.write('\n')


def find_nth(string, sub, n, offset):
    start = string.find(sub, offset)
    while start >= 0 and n > 1:
        start = string.find(sub, start + len(sub))
        n -= 1
    return start


def count_occurences(lst, string):
    count = 0
    for item in lst:
        if string in item:
            count += 1
    return count


def read_sents(inp, outp):

    corpus = PlaintextCorpusReader(os.path.dirname(inp), os.path.basename(inp))
    sents = corpus.sents()
    print_out(outp, sents)


if __name__ == '__main__':
    args = Parser()
    read_sents(args.input, args.output)
