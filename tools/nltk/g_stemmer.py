import nltk
from nltk.stem import PorterStemmer, LancasterStemmer, snowball
import argparse


def arguments():
    parser = argparse.ArgumentParser(description="Segments the text input into separate sentences")
    parser.add_argument('--input', required=True, action="store", type=str, help="input text file")
    parser.add_argument('--output', required=True, action="store", type=str, help="output file path")
    parser.add_argument('--stemmer', required=False, action="store", type=str, help="output file path")
    args = parser.parse_args()
    return args


def stem_file(in_file, out_file, stemmer_type):
    with open(in_file, 'r') as fd:
        unsegmented = fd.read()

    with open(out_file, 'w') as output:
        sentences = nltk.sent_tokenize(unsegmented)
        stemmer = get_stemmer(stemmer_type)
        for sentence in sentences:
            words = nltk.word_tokenize(sentence)
            for word in words:
                stemmed_word = stemmer.stem(word)
                output.write(stemmed_word)
                output.write('\n')


def get_stemmer(stemmer_type):
    if stemmer_type == 'lancaster':
        stemmer = LancasterStemmer()
    elif stemmer_type == 'porter':
        stemmer = PorterStemmer()
    else:
        stemmer = snowball.EnglishStemmer()
    return stemmer


if __name__ == '__main__':
    args = arguments()
    stem_file(args.input, args.output, args.stemmer)
