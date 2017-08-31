from __future__ import print_function
import argparse
import tgt


def parser():
    parser = argparse.ArgumentParser(description="Find matching segments in a TextGrid")
    parser.add_argument('--textgrid', required=True, action="store", type=str, help="TextGrid files (comma separated)")
    parser.add_argument('--identifier', required=True, action="store", type=str, help="Dataset identifiers (comma separated)")
    parser.add_argument('--tier', required=True, action="store", type=str, help="TextGrid Tier to search")
    parser.add_argument('--regex', required=True, action="store", type=str, help="Regular expression matching segments")
    parser.add_argument('--output_path', required=True, action="store", type=str, help="Path to output file")
    return parser.parse_args()


def main():
    args = parser()

    tgfiles = args.textgrid.split(',')
    identifiers = args.identifier.split(',')
    assert len(tgfiles) == len(identifiers), "number of textgrids must match number of identifiers"

    pairs = zip(tgfiles, identifiers)

    rows = []
    for tgfile, identifier in pairs:
        tg = tgt.read_textgrid(tgfile)
        tier = tg.get_tier_by_name(args.tier)
        matches = tier.get_annotations_with_text(args.regex, regex=True)

        for m in matches:
            rows.append((str(m.start_time), str(m.end_time), str(m.duration()), m.text, identifier))

    with open(args.output_path, 'w') as out:
        out.write("start\tend\tduration\tlabel\tidentifier\n")
        for row in rows:
            out.write('\t'.join(row) + '\n')


if __name__ == '__main__':
    main()
