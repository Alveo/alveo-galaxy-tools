from __future__ import print_function
import argparse
from zipfile import ZipFile

def parser():
    parser = argparse.ArgumentParser(description="Find matching segments in a TextGrid")
    parser.add_argument('--dataset', required=True, action="store", type=str, help="TextGrid files (comma separated)")
    parser.add_argument('--identifier', required=True, action="store", type=str, help="Dataset identifiers (comma separated)")
    parser.add_argument('--output', required=True, action="store", type=str, help="Path to output file")
    return parser.parse_args()


def main():
    args = parser()

    datasets = args.dataset.split(',')
    identifiers = args.identifier.split(',')
    assert len(datasets) == len(identifiers), "number of datasets must match number of identifiers"

    pairs = zip(datasets, identifiers)

    with ZipFile(args.output, 'w') as zipfile:
        for dataset, identifier in pairs:
            zipfile.write(dataset, identifier)


if __name__ == '__main__':
    main()
