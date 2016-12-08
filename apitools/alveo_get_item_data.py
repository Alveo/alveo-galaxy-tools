from __future__ import print_function
import json
import argparse
import pyalveo
import sys
import os
from fnmatch import fnmatch
import csv

API_URL = 'https://app.alveo.edu.au' # TODO: export constants to a separate module

def parser():
    parser = argparse.ArgumentParser(description="Downloads documents in an Alveo Item List")
    parser.add_argument('--api_key', required=True, action="store", type=str, help="Alveo API key")
    parser.add_argument('--item_list', required=True, action="store", type=str, help="File containing list of item URLs")
    parser.add_argument('--patterns', required=True, action="store", type=str, help="File patterns to download")
    parser.add_argument('--output_path', required=True, action="store", type=str, help="Path to output file")
    return parser.parse_args()

def read_item_list(filename, client):
    """Read an item list from a file
    which should be a tabular formatted file
    with one column header ItemURL.
    Return an instance of ItemGroup"""

    with open(filename) as fd:
        csvreader = csv.DictReader(fd, dialect='excel-tab')
        if 'ItemURL' not in csvreader.fieldnames:
            return None
        itemurls = []
        for row in csvreader:
            itemurls.append(row['ItemURL'])

    itemlist = pyalveo.ItemGroup(itemurls, client)

    return itemlist

# this file name pattern allows galaxy to discover the dataset designation and type
FNPAT = "%(designation)s#%(ext)s"

def galaxy_name(itemname, fname):
    """construct a filename suitable for Galaxy dataset discovery
    designation - (dataset identifier) is the file basename
    ext - defines the dataset type and is the file extension
    """

    root, ext = os.path.splitext(fname)
    ext = ext[1:] # remove initial .
    fname = FNPAT % {'designation': fname, 'ext': ext}

    return fname

def download_documents(item_list, patterns, output_path):
    """
    Downloads a list of documents to the directory specificed by output_path.

    :type documents: list of pyalveo.Document
    :param documents: Documents to download

    :type output_path: String
    :param output_path: directory to download to the documents to
    """
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    downloaded = []

    items = item_list.get_all()
    filtered_documents = []
    for item in items:
        documents = item.get_documents()
        for doc in documents:
            for pattern in patterns:
                if not pattern == '' and fnmatch(doc.get_filename(), pattern):
                    fname = galaxy_name(item.metadata()['alveo:metadata']['dc:identifier'], doc.get_filename())
                    try:
                        doc.download_content(dir_path=output_path, filename=fname)
                        downloaded.append(doc.get_filename())
                    except:
                        # maybe it doesn't exist or we have no access
                        # TODO: report this
                        pass
    return downloaded

def main():
    args = parser()
    try:
        api_key = open(args.api_key, 'r').read().strip()

        client = pyalveo.Client(api_url=API_URL, api_key=api_key, use_cache=False)

        item_list = read_item_list(args.item_list, client)
        patterns = args.patterns.split(',')
        downloaded = download_documents(item_list, patterns, args.output_path)
    except pyalveo.APIError as e:
        print("ERROR: " + str(e), file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
