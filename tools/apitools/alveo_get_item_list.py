from __future__ import print_function
import argparse
import pyalveo
import sys

API_URL = 'https://app.alveo.edu.au'  # TODO: export constants to a separate module


def parser():
    parser = argparse.ArgumentParser(description="Downloads documents in an Alveo Item List")
    parser.add_argument('--api_key', required=True, action="store", type=str, help="Alveo API key")
    parser.add_argument('--item_list_url', required=True, action="store", type=str, help="Item List to download")
    parser.add_argument('--output', required=True, action="store", type=str, help="output file name")
    return parser.parse_args()


def main():
    args = parser()
    try:
        api_key = open(args.api_key, 'r').read().strip()

        client = pyalveo.Client(api_key=api_key, api_url=API_URL, use_cache=False)
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
