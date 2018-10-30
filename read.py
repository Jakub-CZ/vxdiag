import csv
import string
from collections.abc import Sequence

from humanfriendly.tables import format_pretty_table


def is_sequence(obj):
    if isinstance(obj, str):
        return False
    return isinstance(obj, Sequence)


def get_columns(csv_file, indices):
    if not is_sequence(indices):
        indices = [indices]
    with open(csv_file) as f:
        for record in csv.reader(f):
            yield (len(record), ) + tuple(record[i] for i in indices)


def report_columns(csv_file, indices):
    print("\n" + format_pretty_table([["    %s    " % csv_file]], horizontal_bar="="))
    data = get_columns(csv_file, indices)
    header = next(data)
    header_legend = list(zip(["length"] + list(string.ascii_letters), header))
    header_short = next(zip(*header_legend))
    print(format_pretty_table(header_legend))
    print(format_pretty_table(data, header_short))


if __name__ == '__main__':
    for file in ["data/host-203-01.csv", "data/host-203-02.csv", "data/host-203-03-e.csv"]:
        report_columns(file, list(range(29110, 29116)))
