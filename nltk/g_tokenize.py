import nltk
import string
import argparse

def arguments():
    parser = argparse.ArgumentParser(description="tokenize a text")
    parser.add_argument('--input', required=True, action="store", type=str, help="input text file")
    parser.add_argument('--output', required=True,  action="store", type=str, help="output file path")
    parser.add_argument('--lower', required=False, action="store_true", help="lowercase all words")
    parser.add_argument('--nopunct', required=False, action="store_true", help="remove all punctuation characters")
    args = parser.parse_args()
    return args


def strip_punct(text):
  table = string.maketrans("","")
  return text.translate(table, string.punctuation)


def tokenize(in_file, out_file, lower=False, nopunct=False):
    text = open(in_file, 'r').read()
    if lower:
        text = text.lower()
    if nopunct:
        text = strip_punct(text)
    result = []
    text = unicode(text, errors='ignore')
    sentences = nltk.sent_tokenize(text)
    for sentence in sentences:
        tokens = nltk.word_tokenize(sentence)
        result.append(tokens)
    output = open(out_file, 'w')
    # write one token per line
    for sentence in result:
        for token in sentence:
            output.write(token + "\n")
    output.close()


if __name__ == '__main__':
    args = arguments()
    tokenize(args.input, args.output, lower=args.lower, nopunct=args.nopunct)
