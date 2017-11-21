import nltk
from nltk import FreqDist
import argparse

nltk.download('punkt', quiet=True)


def arguments():
    parser = argparse.ArgumentParser(description="generate a word frequency table from a text")
    parser.add_argument('--input', required=True, action="store", type=str, help="input text file")
    parser.add_argument('--output', required=True, action="store", type=str, help="output file path")
    return parser.parse_args()


def frequency(textfiles, out_file):
    """Input: a text file
    Output: a table of word frequency with three columns for Word, Count and Percent frequency
    """

    words = []
    for textfile in textfiles:
        with open(textfile, 'r') as fd:
            text = fd.read()

        words.extend(nltk.word_tokenize(text))

    fdist = FreqDist(words)
    total = float(fdist.N())

    with open(out_file, 'w') as output:
        output.write("Word\tCount\tPercent\n")
        for pair in sorted(fdist.items()):
            output.write("{pair[0]}\t{pair[1]}\t{pc:.2f}\n".format(pair=pair, pc=100 * pair[1] / total))


if __name__ == '__main__':
    args = arguments()
    textfiles = args.input.split(',')
    frequency(textfiles, args.output)
