# -*- coding: utf-8 -*-

import csv
from collections.abc import Sequence

from humanfriendly.tables import format_pretty_table


def is_sequence(obj):
    if isinstance(obj, str):
        return False
    return isinstance(obj, Sequence)


def slice_columns(csv_file, indices):
    if not is_sequence(indices):
        indices = [indices]
    with open(csv_file) as f:
        yield indices
        for record in csv.reader(f):
            yield [record[i] for i in indices]


def save_as_csv(csv_file, rows):
    with open(csv_file, "w", newline='') as f:
        csv.writer(f).writerows(rows)


def get_columns(csv_file, indices):
    if not is_sequence(indices):
        indices = [indices]
    with open(csv_file) as f:
        for i, record in enumerate(csv.reader(f)):
            yield [i or "ROW", len(record)] + [record[i] for i in indices]


def report_columns(csv_file, indices):
    print("\n" + format_pretty_table([["    %s    " % csv_file]], horizontal_bar="="))
    data = get_columns(csv_file, indices)
    header = next(data)
    header_legend = list(zip(["ROW", "LENGTH"] + indices, header))
    header_short = next(zip(*header_legend))
    print("Cisla a nazvy sloupcu:")
    print(format_pretty_table(header_legend[2:]))
    print(format_pretty_table(data, header_short))


def filter_values(csv_file, condition=lambda val: float(val) == 5600.):
    header = None
    with open(csv_file) as f:
        for row_n, record in enumerate(csv.reader(f)):
            if row_n <= 0:  # just save header
                header = record
                continue
            if not record[-1]:
                record.pop()  # remove empty value at the end
            cols_values = [(i, val) for i, val in enumerate(record)
                           if i > 0 and condition(val)]  # skip first column with date
            headers = [header[i] for i, _ in cols_values]
            yield row_n, cols_values, headers


def report_filtered_values(csv_file):
    global row
    all_headers = set()
    for row, values, headers in filter_values(csv_file):
        if values:
            print(row, ":", values)
            print("headers:\n\t%s" % "\n\t".join(headers))
            all_headers.update(h.rsplit("\\", maxsplit=1)[-1] for h in headers)
    print("\nVSECHNY HLAVICKY SDRUZENE PODLE TYPU: %s" % all_headers)


def get_rows(csv_file, indices, _all=False, with_header=True):
    if not is_sequence(indices):
        indices = [indices]
    indices = set(indices)
    with open(csv_file) as f:
        for i, record in enumerate(csv.reader(f)):
            if not with_header and i == 0:
                continue
            if not _all and not indices:  # all requested rows returned
                break
            if not record[-1]:
                record.pop()  # remove empty value at the end
            if _all or i in indices:
                yield [i, len(record)] + record  # list
                indices.discard(i)


def to_floats(record):
    for i, val in enumerate(record[2 + 1:]):  # skip row number, record length and date/time
        try:
            float(val)
        except ValueError as e:
            yield "#%d: %s" % (i, e)


if __name__ == '__main__':
    # FILE = "data/host-203-02.csv"
    # rows = (get_rows(FILE, (4, 5)))
    # # rows = get_rows("data/host-203-02.csv", None, _all=True, with_header=False)
    # for row in rows:
    #     excps = list(to_floats(row))
    #     assert not excps, excps[:1000]
    # # TODO: sum(delta^2) přes krátká sliding window
    #
    # exit(0)

    for file in ["data/host-203-01.csv", "data/host-203-02.csv", "data/host-203-03-e.csv"]:
        report_columns(file, [0] + list(range(31118, 31132)))
        report_filtered_values(file)  # lambda val: 5700. > float(val) > 5500.
        break
