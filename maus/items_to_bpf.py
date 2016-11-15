from __future__ import print_function
import json
import argparse
import pyalveo
import sys
import os
from fnmatch import fnmatch
import csv
import re


def parser():
    parser = argparse.ArgumentParser(description="Generate BPF Orthographic Transcription from Item List")
    parser.add_argument('--item_list', required=True, action="store", type=str, help="File containing list of item URLs")
    parser.add_argument('--lexicon', required=True, action="store", type=str, help="File containing lexicon (tsv)")
    parser.add_argument('--output_path', required=True, action="store", type=str, help="Path to output file")
    return parser.parse_args()

def read_item_list(filename):
    """Read an item list from a file
    which should be a tabular formatted file
    with one column header ItemURL.
    Return an instance of ItemGroup"""

    with open(filename) as fd:
        csvreader = csv.DictReader(fd, dialect='excel-tab')
        print("CSV", csvreader.fieldnames)
        if 'ItemURL' not in csvreader.fieldnames:
            return None
        if 'Prompt' not in csvreader.fieldnames:
            return None
        itemurls = []
        for row in csvreader:
            itemurls.append((row['Prompt'], row['ItemURL']))

    return itemurls

# this file name pattern allows galaxy to discover the dataset designation and type
FNPAT = "%(designation)s#%(ext)s"

def galaxy_name(itemurl, ext):
    """Construct a filename suitable for dataset discovery
    by Galaxy.

    @type itemurl: C{String}
    @param itemurl: the item URL from Alveo

    @type ext: C{String}
    @param ext: the datatype extension for the resulting file
    """

    itemname = itemurl.split('/')[-1]
    fname = FNPAT % {'designation': itemname, 'ext': ext}

    return fname


def build_bpf(ortho_trans, lexicon):
    """ Given an orthographic transcript, generate a BPF-format phonetic
        transcription for passing to MAUS, using the specified lexicon.

        @type ortho_trans: C{String}
        @param ortho_trans: the (space-separated) orthographic transcript
        @type lex: C{Dict}
        @param lex: the lexicon to use to translate words to phonetic sybmols

        @rtype: C{String}
        @returns: the BPF-formatted transcript

        @raises IncompleteLexiconError: if there is a word appearing in the
        orthographic transcript that is not covered by the lexicon

    """

    spl = re.compile(r'[\s.,!?"\-]')
    words = [w.lower() for w in spl.split(ortho_trans) if w]
    ort = []
    kan = []

    for n, word in enumerate(words):
        try:
            ort.append("ORT: %d %s" % (n, word))
            kan.append("KAN: %d %s" % (n, lexicon[word]))
        except KeyError:
            raise IncompleteLexiconError("'" + word +
                                         "' not present in lexicon")

    nl = u"\n"
    return nl.join(ort) + nl + nl.join(kan)


def load_lexicon(lexiconfile):
    """ Load the given file as a lexicon dictionary.
        Should be a tsv file with two columns, first column
        is orthography, second is phonetic transcription.

        @type lexiconfile: C{String}
        @param lexiconfile: the filename of the lexicon file

        @rtype: C{Dict}
        @returns: the lexicon, as a dictionary with orthographic entries as keys

    """
    lex = {}

    with open(lexiconfile) as f:
        for line in f:
            orth, pron = line.split('\t')
            lex[orth] = pron

    return lex


def list_to_bpf(item_list, lexicon, output_path):
    """
    Generate a BPF file for each item in this item list.
    Items consist of (prompt, ItemURL). URL is used to generate output
    file name.

    :type documents: list of pyalveo.Document
    :param documents: Documents to download

    :type output_path: String
    :param output_path: directory to download to the documents to
    """
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    for prompt, itemURL in item_list:

        fname = galaxy_name(itemURL, 'par')
        bpftext = build_bpf(prompt, lexicon)
        with open(os.path.join(output_path, fname), 'w') as out:
            out.write(bpftext)


def main():
    args = parser()
    item_list = read_item_list(args.item_list)
    lexicon = load_lexicon(args.lexicon)
    list_to_bpf(item_list, lexicon, args.output_path)


if __name__ == '__main__':
    main()
