import nltk
from nltk import FreqDist
import argparse

nltk.download('punkt', quiet=True)


def arguments():
    parser = argparse.ArgumentParser(description="generate a word frequency table from a text")
    parser.add_argument('--input', required=True, action="store", type=str, help="input text file")
    parser.add_argument('--output', required=True, action="store", type=str, help="output file path")
    return parser.parse_args()


def frequency(in_file, out_file):
    """Input: a text file
    Output: a table of word frequency with three columns for Word, Count and Percent frequency
    """
    with open(in_file, 'r') as fd:
        text = fd.read()

    words = nltk.word_tokenize(text)
    fdist = FreqDist(words)
    total = float(fdist.N())

    with open(out_file, 'w') as output:
        output.write("Word\tCount\tPercent\n")
        for pair in fdist.items():
            output.write("{pair[0]}\t{pair[1]}\t{pc:.2f}\n".format(pair=pair, pc=100 * pair[1] / total))


if __name__ == '__main__':
    args = arguments()
    frequency(args.input, args.output)
