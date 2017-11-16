from __future__ import print_function
import argparse
import pyalveo
import sys
import os

from util import API_URL, read_item_list


def parser():
    parser = argparse.ArgumentParser(description="Downloads documents in an Alveo Item List")
    parser.add_argument('--api_key', required=True, action="store", type=str, help="Alveo API key")
    parser.add_argument('--item_list', required=True, action="store", type=str, help="File containing list of item URLs")
    parser.add_argument('--output_path', required=True, action="store", type=str, help="Path to output file")
    return parser.parse_args()


# this file name pattern allows galaxy to discover the dataset designation and type
FNPAT = "%(designation)s_%(ext)s"


def galaxy_name(fname, ext):
    """construct a filename suitable for Galaxy dataset discovery"""

    fname = FNPAT % {'designation': fname, 'ext': ext}

    return fname


def download_text(item_list, output_path):
    """
    Downloads primary text from a list of items to the directory specified by output_path.

    :type item_list: ItemGroup
    :param item_list: item list to download

    :type output_path: String
    :param output_path: directory to download to the documents to
    """
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    downloaded = []

    items = item_list.get_all()
    for item in items:
        md = item.metadata()
        fname = os.path.join(output_path, galaxy_name(md['alveo:metadata']['dcterms:identifier'], 'txt'))
        content = item.get_primary_text()
        if content is not None:
            with open(fname, 'w') as out:
                out.write(content.decode('utf-8'))

    return downloaded


def main():
    args = parser()
    try:
        api_key = open(args.api_key, 'r').read().strip()
        client = pyalveo.Client(api_url=API_URL, api_key=api_key, use_cache=False)
        item_list = read_item_list(args.item_list, client)
        download_text(item_list, args.output_path)
    except pyalveo.APIError as e:
        print("ERROR: " + str(e), file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
