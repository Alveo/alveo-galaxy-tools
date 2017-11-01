from __future__ import print_function
import argparse
import pyalveo
import sys
from util import API_URL, write_key


def parser():
    p = argparse.ArgumentParser(description="Downloads documents in an Alveo Item List")
    p.add_argument('--api_key', required=True, action="store", type=str, help="Alveo API key")
    p.add_argument('--item_list_url', required=True, action="store", type=str, help="Item List to download")
    p.add_argument('--output', required=True, action="store", type=str, help="output file name")
    p.add_argument('--outputkey', required=True, action="store", type=str, help="output file name for API Key")
    return p.parse_args()


def main():
    args = parser()
    try:
        write_key(args.api_key, args.outputkey)

        client = pyalveo.Client(api_key=args.api_key, api_url=API_URL, use_cache=False)
        item_list = client.get_item_list(args.item_list_url)

        with open(args.output, 'w') as out:
            out.write("ItemURL\n")
            for item in item_list:
                out.write(item + "\n")
                print(item)

    except pyalveo.APIError as e:
        print("ERROR: " + str(e), file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
