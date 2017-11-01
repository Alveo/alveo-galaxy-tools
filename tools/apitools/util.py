"""
Utility functions and settings for API tools
"""
import pyalveo
import csv

# this should be in a config file
API_URL = 'https://app.alveo.edu.au'


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


def get_item_lists(api_key):
    client = pyalveo.Client(api_key=api_key, api_url=API_URL, use_cache=False)
    return client.get_item_lists()


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
