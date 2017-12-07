
import json

API_URL = 'https://app.alveo.edu.au'


try:
    from urllib.request import Request, build_opener, HTTPHandler, HTTPError
    from urllib.parse import urlencode, unquote
except ImportError:
    from urllib2 import Request, build_opener, HTTPHandler, HTTPError
    from urllib import urlencode, unquote


def api_request(url, api_key):
    """ Perform an API GET request to the given URL
    """

    headers = {'X-API-KEY': api_key, 'Accept': 'application/json'}

    req = Request(url, headers=headers)

    try:
        opener = build_opener(HTTPHandler())
        response = opener.open(req)
    except HTTPError as err:
        raise APIError(err.code, err.reason, "Error accessing API (url: %s, method: %s)\nData: %s" % (url, req.get_method() or "GET", data or 'None'))

    content = response.read()

    return json.loads(content.decode('utf-8'))


def ds_item_lists_options(api_key):
    """Return options for item lists for this user"""

    fname = api_key.get_file_name()
    with open(fname) as fd:
        key = fd.read().strip()

    url = API_URL + "/item_lists"
    itemlists = api_request(url, key)

    result = [(x['name'], x['item_list_url'], False) for x in itemlists['own']]
    result.extend([(x['name'], x['item_list_url'], False) for x in itemlists['shared']])

    return result


if __name__=='__main__':

    class FakeHistObj:

        def get_file_name(self):
            return "../../test-data/api-key.dat"

    fake = FakeHistObj()

    il = ds_item_lists_options(fake)

    import pprint

    pprint.pprint(il)
