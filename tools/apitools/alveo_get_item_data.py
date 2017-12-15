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
    p.add_argument('--patterns', required=False, action="store", type=str, help="File patterns to download")
    p.add_argument('--primarytext', required=False, action="store_true", help="Download only primary text")
    p.add_argument('--output_path', required=True, action="store", type=str, help="Path to output file")
    return p.parse_args()


# this file name pattern allows galaxy to discover the dataset designation and type
FNPAT = "%(designation)s#%(ext)s"


def galaxy_name(fname, ext):
    """construct a filename suitable for Galaxy dataset discovery"""

    fname = FNPAT % {'designation': fname, 'ext': ext}

    return fname


def download_documents(item_list, output_path, patterns=None):
    """
    Downloads a list of documents to the directory specified by output_path.

    :type documents: list of pyalveo.Document
    :param documents: Documents to download

    :type patterns: string
    :param patterns: Glob pattern for files to download, may include the special
    pattern PRIMARYTEXT which returns the primary text of each item as ITEMNAME.txt

    :type output_path: String
    :param output_path: directory to download to the documents to
    """
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    items = item_list.get_all()
    for item in items:
        md = item.metadata()
        ident = md['alveo:metadata']['dcterms:identifier']

        documents = item.get_documents()
        for doc in documents:
            for pattern in patterns:
                if pattern == 'PRIMARYTEXT':
                    fname = os.path.join(output_path, galaxy_name(ident, 'txt'))
                    content = item.get_primary_text()
                    if content is not None:
                        with open(fname, 'w') as out:
                            out.write(content.decode('utf-8'))

                elif not pattern == '' and fnmatch(doc.get_filename(), pattern):
                    root, ext = os.path.splitext(doc.get_filename())
                    ext = ext[1:]  # remove initial .
                    fname = galaxy_name(root, ext)
                    try:
                        doc.download_content(dir_path=output_path, filename=fname)

                    except pyalveo.APIError as e:
                        print("ERROR: " + str(e), file=sys.stderr)
                        sys.exit(1)


def main():
    args = parser()
    try:
        api_key = open(args.api_key, 'r').read().strip()

        client = pyalveo.Client(api_url=API_URL, api_key=api_key, use_cache=False)

        item_list = read_item_list(args.item_list, client)

        patterns = args.patterns.split(',')
        download_documents(item_list, args.output_path, patterns=patterns)

    except pyalveo.APIError as e:
        print("ERROR: " + str(e), file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
