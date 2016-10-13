import nltk
from nltk import FreqDist
import argparse

def arguments():
  parser = argparse.ArgumentParser(description="generate a word frequency table from a text")
  parser.add_argument('--input', required=True, action="store", type=str, help="input text file")
  parser.add_argument('--output', required=True,  action="store", type=str, help="output file path")
  args = parser.parse_args()
  return args


def frequency(in_file, out_file):
    """Input: a text file
    Output: a table of word frequency with three columns for Word, Count and Percent frequency
    """
    text = unicode(open(in_file, 'r').read(), errors='ignore')
    words = nltk.word_tokenize(text)
    frequency = FreqDist(words)
    total = float(frequency.N())
    output = open(out_file, 'w')
    output.write("Word\tCount\tPercent\n")
    for pair in frequency.items():
        output.write("{pair[0]}\t{pair[1]}\t{pc:.2f}\n".format(pair=pair, pc=100*pair[1]/total))
    output.close()


if __name__ == '__main__':
    args = arguments()
    frequency(args.input, args.output)
