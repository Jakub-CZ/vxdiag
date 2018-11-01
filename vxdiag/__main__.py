import sys
from os.path import splitext

from .read import save_as_csv, slice_columns

if __name__ == '__main__':
    args = sys.argv
    if len(args) < 4:
        print("Pouziti: python -m vxdiag <csv-jmeno> <start> <konec> [<start> <konec> ...]")
        print("")
        print("\t<start> a <konec> je rozsah sloupcu (pocitano od 1), ktere chces vyexportovat")
        exit(1)
    csv_file = args[1]
    filename_ext = splitext(csv_file)
    csv_file_out = "%s-out%s" % filename_ext
    columns = [int(i) for i in args[2:]]
    intervals = list(zip(columns[::2], columns[1::2]))
    print(" vstupni soubor:\t%s" % csv_file)
    print("        sloupce:\t%s" % ", ".join("(%d-%d)" % t for t in intervals))
    print("vystupni soubor:\t%s" % csv_file_out)

    save_as_csv(csv_file_out, slice_columns(csv_file, [i for a, b in intervals for i in range(a-1, b)]))
