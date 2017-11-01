import nltk
import string
import argparse

nltk.download('punkt', quiet=True)


def arguments():
    parser = argparse.ArgumentParser(description="tokenize a text")
    parser.add_argument('--input', required=True, action="store", type=str, help="input text file")
    parser.add_argument('--output', required=True, action="store", type=str, help="output file path")
    parser.add_argument('--lower', required=False, action="store_true", help="lowercase all words")
    parser.add_argument('--nopunct', required=False, action="store_true", help="remove all punctuation characters")
    return parser.parse_args()


def strip_punct(text):
    table = text.maketrans("", "")
    return text.translate(table, string.punctuation)


def tokenize(in_file, out_file, lower=False, nopunct=False):
    with open(in_file, 'r') as fd:
        text = fd.read()

    if lower:
        text = text.lower()
    result = []
    # text = unicode(text, errors='ignore')
    sentences = nltk.sent_tokenize(text)
    for sentence in sentences:
        tokens = nltk.word_tokenize(sentence)
        if nopunct:
            tokens = filter(lambda w: w not in string.punctuation, tokens)
        result.append(tokens)

    with open(out_file, 'w') as output:
        # write one token per line
        for sentence in result:
            for token in sentence:
                output.write(token + "\n")


if __name__ == '__main__':
    args = arguments()
    tokenize(args.input, args.output, lower=args.lower, nopunct=args.nopunct)
