from __future__ import print_function
import json
import argparse
import pyalveo
import sys
import os
from fnmatch import fnmatch

API_URL = 'https://app.alveo.edu.au' # TODO: export constants to a separate module

def parser():
    parser = argparse.ArgumentParser(description="Downloads documents in an Alveo Item List")
    parser.add_argument('--api_key', required=True, action="store", type=str, help="Alveo API key")
    parser.add_argument('--item_list_url', required=True, action="store", type=str, help="Item List to download")
    parser.add_argument('--output_path', required=True, action="store", type=str, help="Path to output file")
    return parser.parse_args()

def get_item_list(api_key, item_list_url):
    client = pyalveo.Client(api_key=api_key, api_url=API_URL, use_cache=False)
    return client.get_item_list(item_list_url)

# this file name pattern allows galaxy to discover the dataset designation and type
FNPAT = "%(designation)s_%(ext)s"

def galaxy_name(fname, ext):
    """construct a filename suitable for Galaxy dataset discovery"""

    fname = FNPAT % {'designation': fname, 'ext': ext}

    return fname
import pprint
def download_documents(item_list, output_path):
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
        md = item.metadata()
        fname = os.path.join(output_path, galaxy_name(md['alveo:metadata']['dc:identifier'], 'txt'))
        content = item.get_primary_text()
        if not content == None:
            with open(fname, 'w') as out:
                out.write(content)

    return downloaded

def main():
    args = parser()
    try:
        api_key = open(args.api_key, 'r').read().strip()
        item_list = get_item_list(api_key, args.item_list_url)
        downloaded = download_documents(item_list, args.output_path)
        # write out a list of downloaded files as a result?
    except pyalveo.APIError as e:
        print("ERROR: " + str(e), file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
