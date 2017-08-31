import csv
import argparse


def parser():
    parser = argparse.ArgumentParser(description="Cut data for a segment from a timeseries")
    parser.add_argument('--segment_list', required=True, action="store", type=str, help="File containing list of item URLs")
    parser.add_argument('--timeseries', required=True, action="store", type=str, help="time series data (comma separated file names)")
    parser.add_argument('--identifier', required=True, action="store", type=str, help="Time series dataset identifiers (comma separated)")
    parser.add_argument('--cutat', required=True, action="store", type=float, help="cut point 0-1")
    parser.add_argument('--output_path', required=True, action="store", type=str, help="Path to output file")
    return parser.parse_args()


def read_segment_list(filename):
    """Read an segment list from a file
    which should be a tabular formatted file
    with columns start, end, label, duration, identifier
    Return a dictionary with the 'identifier' field as keys
    and a dictionary of other values as the values.
    """

    segments = []
    with open(filename) as fd:
        csvreader = csv.DictReader(fd, dialect='excel-tab')
        if 'identifier' not in csvreader.fieldnames:
            return None

        for row in csvreader:
            segments.append(row)

    return segments


def get_tsfile(ident, tsfiles):
    """Get the tsfile that matches the identifier """

    for tsid, dsname in tsfiles:
        if ident in tsid:
            return dsname

    return ''


def cut(tsfiles, segfile, cutpoint):
    """Cut data from tsfile corresponding to the
    cutpoint (0-1) for the segment with the id
    in segs.
    Return... """

    segments = read_segment_list(segfile)

    headers = ['identifier', 'label']
    result = []

    for seg in segments:

        start = float(seg['start'])
        end = float(seg['end'])
        label = seg['label']
        ident = seg['identifier']
        tsfile = get_tsfile(ident, tsfiles)

        if tsfile == '':
            continue

        collect = []
        with open(tsfile, 'r') as fd:
            reader = csv.reader(fd, dialect=csv.excel_tab)
            for row in reader:
                if row[0] == 'time':
                    tsheader = row
                elif start < float(row[0]) < end:
                    collect.append(row)

        # grab the row at the cut point(s)
        n = int(cutpoint * len(collect))
        row = [ident, label]
        row.extend(collect[n])
        result.append(row)

    headers.extend(tsheader)
    return headers, result


if __name__ == '__main__':

    args = parser()

    # get the list of timeseries files
    tsfiles = args.timeseries.split(',')
    tsidents = args.identifier.split(',')

    headers, rows = cut(zip(tsidents, tsfiles), args.segment_list, args.cutat)

    with open(args.output_path, 'w') as out:
        writer = csv.writer(out, dialect=csv.excel_tab)
        writer.writerow(headers)
        for row in rows:
            writer.writerow(row)
