from __future__ import print_function
import argparse
import pyalveo
import sys
import os
from fnmatch import fnmatch
from util import API_URL, read_item_list


def parser():
    p = argparse.ArgumentParser(description="Downloads documents in an Alveo Item List")
    p.add_argument('--api_key', required=True, action="store", type=str, help="Alveo API key")
    p.add_argument('--item_list', required=True, action="store", type=str, help="File containing list of item URLs")
    p.add_argument('--patterns', required=True, action="store", type=str, help="File patterns to download")
    p.add_argument('--output_path', required=True, action="store", type=str, help="Path to output file")
    return p.parse_args()


# this file name pattern allows galaxy to discover the dataset designation and type
FNPAT = "%(designation)s#%(ext)s"


def galaxy_name(itemname, fname):
    """construct a filename suitable for Galaxy dataset discovery
    designation - (dataset identifier) is the file basename
    ext - defines the dataset type and is the file extension
    """

    root, ext = os.path.splitext(fname)
    ext = ext[1:]  # remove initial .
    fname = FNPAT % {'designation': root, 'ext': ext}

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
    for item in items:
        documents = item.get_documents()
        for doc in documents:
            for pattern in patterns:
                if not pattern == '' and fnmatch(doc.get_filename(), pattern):
                    fname = galaxy_name(item.metadata()['alveo:metadata']['dcterms:identifier'], doc.get_filename())
                    try:
                        doc.download_content(dir_path=output_path, filename=fname)
                        downloaded.append(doc.get_filename())
                    except pyalveo.APIError as e:
                        print("ERROR: " + str(e), file=sys.stderr)
                        sys.exit(1)
    return downloaded


def main():
    args = parser()
    try:
        api_key = open(args.api_key, 'r').read().strip()

        client = pyalveo.Client(api_url=API_URL, api_key=api_key, use_cache=False)

        item_list = read_item_list(args.item_list, client)
        patterns = args.patterns.split(',')
        download_documents(item_list, patterns, args.output_path)
    except pyalveo.APIError as e:
        print("ERROR: " + str(e), file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
