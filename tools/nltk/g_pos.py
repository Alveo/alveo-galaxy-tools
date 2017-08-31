import nltk
import argparse


def arguments():
    parser = argparse.ArgumentParser(description="tokenize a text")
    parser.add_argument('--input', required=True, action="store", type=str, help="input text file")
    parser.add_argument('--output', required=True, action="store", type=str, help="output file path")
    return parser.parse_args()


def postag(in_file, out_file):
    """Input: a text file with one token per line
    Output: a version of the text with Part of Speech tags written as word/TAG
    """
    with open(in_file, 'r') as fd:
        text = fd.read()

    sentences = nltk.sent_tokenize(text)

    with open(out_file, 'w') as output:
        for sentence in sentences:
            tokens = nltk.word_tokenize(sentence)
            postags = nltk.pos_tag(tokens)
            for postag in postags:
                # print postag
                output.write("%s/%s " % postag)
        output.write('\n')


if __name__ == '__main__':
    args = arguments()
    postag(args.input, args.output)
