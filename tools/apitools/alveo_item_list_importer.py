from __future__ import print_function
import argparse
import sys
from util import get_item_lists


def parser():
    p = argparse.ArgumentParser(description="Retrieves Alveo Item Lists")
    p.add_argument('--api_key', required=True, action="store", type=str, help="Alveo API key")
    p.add_argument('--output', required=True, action="store", type=str, help="Path to output file")
    return p.parse_args()


def write_table(item_lists, filename):
    with open(filename, 'w') as outfile:
        for list_set in item_lists.values():
            for item_list in list_set:
                outfile.write("%s (%d)\t%s\n" % (item_list['name'], item_list['num_items'], item_list['item_list_url']))


def main():
    args = parser()
    try:
        api_key = open(args.api_key, 'r').read().strip()
        item_lists = get_item_lists(api_key)
        if item_lists:
            write_table(item_lists, args.output)
    except Exception as e:
        print("ERROR: " + str(e), file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
