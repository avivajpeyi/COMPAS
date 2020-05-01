""" Module to parse a COMPAS file
"""

import argparse

import numpy as np


def parse_header(header_str, delimiter):
    """

    :param header_str:
    :param delimiter:
    :return:
    """
    headers = header_str.split(delimiter)  # split header using delimiter
    headers = [h.strip() for h in headers]  # remove trailing whitespaces in each header
    return headers


def parse_data(filehandler, delimiter):
    """
    Read and parse the data from the file
    data values are extracted to 2-d list ([column][row])

    :param filehandler:
    :param delimiter:
    :return:
    """
    data = np.genfromtxt(
        fname=filehandler,
        skip_header=2,
        delimiter=delimiter,
        autostrip=True,
        names=True
    )
    names = data.dtype.names

    # initalise an empty list of values
    num_rows, num_cols = len(data), len(names)
    values = [[0.0 for _ in range(num_rows)] for _ in range(num_cols)]
    # read the data from the file into 2-d values list
    for row in range(num_rows):
        # extract the data values to a 2-d list
        for column in range(min(num_cols, len(data[row]))):
            values[column][row] = data[row][column]

    return values, names


def process_file(filename, delimiter=','):
    """Read and return the names, types, units and values stored in a COMPAS file.

    If there is a failure, all returned lists will be empty (e.g. unable to open file).

    :param filename: str
        The COMPAS data filepath.
    :param delimiter: str
        Character for specifying the boundary between separate cols in the COMPAS file.
        Default is ','
    :return: Tuple(list, list, list, list)
        names  - 1-d list of column names (headings)
        types  - 1-d list of column data types
        units  - 1-d list of column units
        values - 2-d list of data values: values[column][row]

    """
    with open(filename, mode='r') as fi:
        types = parse_header(fi.readline(), delimiter)  # types on 1st line
        units = parse_header(fi.readline(), delimiter)  # units on 2nd line
        fi.seek(0)  # reset filehandler
        values, names = parse_data(fi, delimiter)
        return names, types, units, values


def get_filename_from_cli():
    """
    :return: str
        Filename entered in CLI
    """
    parser = argparse.ArgumentParser(description='COMPAS data file parse example.')
    parser.add_argument(
        'filename',
        metavar='filename',
        type=str,
        nargs=1,
        help='name of COMPAS data file'
    )
    args = parser.parse_args()
    return args.filename


def generate_data_summary(names, types, units, values):
    """

    :param names:
    :param types:
    :param units:
    :param values:
    :return:
    """
    output_data = []

    # Counts
    output_data.append(f'column names  count = {len(names)}')
    output_data.append(f'column types  count = {len(types)}')
    output_data.append(f'values column count = {len(values)}')
    output_data.append(f'values row    count = {len(values[0])}')

    # Column names and types and units
    output_data.append('\nColumn names:\n')
    for idx, n in enumerate(names):
        output_data.append(f'Column{idx}, Name = {n}')
    output_data.append('\nColumn types:\n')
    for idx, t in enumerate(types):
        output_data.append(f'Column{idx}, Type = {t}')
    output_data.append('\nColumn units:\n')
    for idx, u in enumerate(units):
        output_data.append(f'Column{idx}, Units = {u}')

    # the data can be accessed by value[column][row]
    # print a couple of values

    if len(values) > 4 and len(values[0]) > 14:
        print()

        column = 3
        row = 5
        print(
            'Column', column, ', name =', names[column], ', type =', types[column],
            ', units =',
            units[column], ', value at row', row, '=', values[column][row])

        column = 4
        row = 14
        print(
            'Column', column, ', name =', names[column], ', type =', types[column],
            ', units =',
            units[column], ', value at row', row, '=', values[column][row])

    # look for a specific column name

    columnName = 'Radius_1'
    try:
        whichColumn = names.index(columnName)
    except ValueError:
        print('\nColumn name', columnName, 'not found!')
        whichColumn = -1

    if whichColumn >= 0:
        print('\nColumn name', columnName, 'is column index', whichColumn, '(0-based)')

    # print a couple of values from the column just found

    if len(values[whichColumn]) > 17:
        print()

        column = whichColumn

        row = 3
        print(
            'Column', column, ', name =', names[column], ', type =', types[column],
            ', units =',
            units[column], ', value at row', row, '=', values[column][row])

        row = 16
        print(
            'Column', column, ', name =', names[column], ', type =', types[column],
            ', units =',
            units[column], ', value at row', row, '=', values[column][row])



    data_summary = "\n".join(output_data)
    return data_summary


def main():
    filename = get_filename_from_cli()
    print(f'Processing file {filename}')
    names, types, units, values = process_file(filename)
    data_summary = generate_data_summary(names, types, units, values)
    print(data_summary)


if __name__ == '__main__':
    main()
