import sys
import nltk
import argparse


def arguments():
    parser = argparse.ArgumentParser(description="run NER on a text")
    parser.add_argument('--input', required=True, action="store", type=str, help="input text file")
    parser.add_argument('--grammar', required=True, action="store", type=str, help="grammar file")
    parser.add_argument('--output', required=True, action="store", type=str, help="output file path")
    return parser.parse_args()


def chart_parse(in_file, grammar_file, out_file):
    with open(in_file, 'r') as fd:
        text = fd.read()

    with open(grammar_file, 'r') as fd:
        grammar_string = fd.read()

    try:
        grammar = nltk.CFG.fromstring(grammar_string)
        parser = nltk.ChartParser(grammar)
        sentences = nltk.sent_tokenize(text)
        with open(out_file, 'w') as output:
            for sentence in sentences:
                words = nltk.word_tokenize(sentence)
                trees = parser.parse(words)
                for t in trees:
                    output.write(t.pformat())
                    output.write('\n')

    except Exception as e:
        message = """Error with parsing. Check the input files are correct
and the grammar contains every word in the input sequence. \n----\n""" + str(e) + "\n"
        sys.stderr.write(message)
        sys.exit()
    output.close()


if __name__ == '__main__':
    args = arguments()
    chart_parse(args.input, args.grammar, args.output)
