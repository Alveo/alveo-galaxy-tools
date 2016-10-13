import sys
import nltk
import argparse
from nltk.corpus import PlaintextCorpusReader

def arguments():
    parser = argparse.ArgumentParser(description="run NER on a text")
    parser.add_argument('--input', required=True, action="store", type=str, help="input text file")
    parser.add_argument('--grammar', required=True,  action="store", type=str, help="grammar file")
    parser.add_argument('--output', required=True,  action="store", type=str, help="output file path")
    args = parser.parse_args()
    return args


def chart_parse(in_file, grammar_file, out_file):
    text = unicode(open(in_file, 'r').read(), errors='ignore')
    output = open(out_file, 'w')
    grammar_string = unicode(open(grammar_file, 'r').read(), errors='ignore')
    try:
        grammar = nltk.parse_cfg(grammar_string)
        parser = nltk.ChartParser(grammar)
        sentences = nltk.sent_tokenize(text)
        for sentence in sentences:
            words = nltk.word_tokenize(sentence)
            tree = parser.parse(words)
            output.write(tree.pprint())
            output.write('\n')
    except Exception, e:
        message = "Error with parsing. Check the input files are correct and the grammar contains every word in the input sequence. \n----\n" + str(e)
        sys.stderr.write(message)
        sys.exit()
    output.close()

if __name__ == '__main__':
    args = arguments()
    chart_parse(args.input, args.grammar, args.output)


