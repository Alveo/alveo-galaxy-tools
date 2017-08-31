from __future__ import print_function
import argparse
import pyalveo
import sys

API_URL = 'https://app.alveo.edu.au/'
PREFIXES = """
PREFIX dc:<http://purl.org/dc/terms/>
PREFIX austalk:<http://ns.austalk.edu.au/>
PREFIX olac:<http://www.language-archives.org/OLAC/1.1/>
PREFIX ausnc:<http://ns.ausnc.org.au/schemas/ausnc_md_model/>
PREFIX foaf:<http://xmlns.com/foaf/0.1/>
PREFIX dbpedia:<http://dbpedia.org/ontology/>
PREFIX rdf:<http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs:<http://www.w3.org/2000/01/rdf-schema#>
PREFIX geo:<http://www.w3.org/2003/01/geo/wgs84_pos#>
PREFIX iso639schema:<http://downlode.org/rdf/iso-639/schema#>
PREFIX austalkid:<http://id.austalk.edu.au/>
PREFIX iso639:<http://downlode.org/rdf/iso-639/languages#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX is: <http://purl.org/ontology/is/core#>
PREFIX iso: <http://purl.org/iso25964/skos-thes#>
PREFIX dada: <http://purl.org/dada/schema/0.2#>"""


def parser():
    parser = argparse.ArgumentParser(description="Retrieves Alveo Item Lists")
    parser.add_argument('--api_key', required=True, action="store", type=str, help="Alveo API key")
    parser.add_argument('--speaker', required=True, action="store", type=str, help="Speaker identifier")
    parser.add_argument('--words', required=False, default='all', action="store", type=str,
                        help="Word group (all, monopthongs, dipthongs)")
    parser.add_argument('--output', required=True, action="store", type=str, help="output file name")
    return parser.parse_args()


def find_hVd_words(api_key, speakerid, output, words='all'):
    """Find words in the Austalk corpus
    """

    client = pyalveo.Client(api_key, API_URL, use_cache=False)

    query = PREFIXES + """
SELECT distinct ?item ?prompt ?compname
WHERE {
  ?item a ausnc:AusNCObject .
  ?item olac:speaker ?speaker .
  ?speaker austalk:id "%s" .
  ?item austalk:prompt ?prompt .
  ?item austalk:componentName ?compname .
 """ % speakerid

    hVdWords = dict(monopthongs=['head', 'had', 'hud', 'heed', 'hid', 'hood', 'hod',
                                 'whod', 'herd', 'haired', 'hard', 'horde'],
                    dipthongs=['howd', 'hoyd', 'hide', 'hode', 'hade', 'heared'])

    if words == 'all':
        words = hVdWords['monopthongs'] + hVdWords['dipthongs']
    else:
        words = hVdWords[words]

    filterclause = 'FILTER regex(?prompt, "^'
    filterclause += '$|^'.join(words)
    filterclause += '$", "i")\n'

    query += filterclause + "}"

    result = client.sparql_query('austalk', query)

    items = []
    for b in result['results']['bindings']:
        items.append((b['prompt']['value'], b['item']['value']))

    with open(output, 'w') as out:
        out.write("Speaker\tPrompt\tItemURL\n")
        for item in items:
            # TODO: fix this once the RDF data is fixed in alveo
            # need to modify the item URL
            itemurl = item[1].replace('http://id.austalk.edu.au/item/', 'https://app.alveo.edu.au/catalog/austalk/')

            out.write(speakerid + "\t" + item[0] + "\t" + itemurl + "\n")


def main():
    args = parser()
    try:
        api_key = open(args.api_key, 'r').read().strip()
        find_hVd_words(api_key, args.speaker, args.output, args.words)
    except Exception as e:
        print("ERROR: " + str(e), file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
