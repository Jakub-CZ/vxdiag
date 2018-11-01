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


if __name__ == '__main__':
    for file in ["data/host-203-01.csv", "data/host-203-02.csv", "data/host-203-03-e.csv"]:
        report_columns(file, [0] + list(range(29105, 29120)))
