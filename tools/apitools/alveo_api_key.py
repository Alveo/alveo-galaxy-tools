from __future__ import print_function
import argparse
import pyalveo
import sys

API_URL = 'https://app.alveo.edu.au'


def parser():
    parser = argparse.ArgumentParser(description="Retrieves Alveo Item Lists")
    parser.add_argument('--api_key', required=True, action="store", type=str, help="Alveo API key")
    parser.add_argument('--output_path', required=True, action="store", type=str, help="File to store the API key in")
    return parser.parse_args()


def write_key(api_key, output_path, client_module=pyalveo):
    """Tests whether an API key is valid and writes it to a file.

    :type api_key: String
    :param api_key: Alveo API key

    :type output_path: String
    :param output_path: Path to the file to store the API key in

    :type client_module: pyalveo.Client
    :param client_module: Module providing the client (used for testing purposes),
        defaults to pyalveo

    :raises: pyalveo.APIError if the API request is not successful

    """
    # validate the client key, raises an exception if it is not valid
    client_module.Client(api_key, API_URL, use_cache=False)
    outfile = open(output_path, 'w')
    outfile.write(api_key)
    outfile.close()


def main():
    args = parser()
    try:
        write_key(args.api_key, args.output_path)
    except Exception as e:
        print("ERROR: " + str(e), file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
