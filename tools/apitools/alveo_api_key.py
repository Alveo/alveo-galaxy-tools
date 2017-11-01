from __future__ import print_function
import argparse
import sys
from util import write_key


def parser():
    p = argparse.ArgumentParser(description="Retrieves Alveo Item Lists")
    p.add_argument('--api_key', required=True, action="store", type=str, help="Alveo API key")
    p.add_argument('--output_path', required=True, action="store", type=str, help="File to store the API key in")
    return p.parse_args()


def main():
    args = parser()
    try:
        write_key(args.api_key, args.output_path)
    except Exception as e:
        print("ERROR: " + str(e), file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
