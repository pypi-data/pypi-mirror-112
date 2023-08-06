#!/usr/bin/env python
""" A simple HTML page generation for tables

This generates a simple HTML page for displaying images/text. Must be called
from the directory in which the images are to be generated.

Usage: The nth columns of images/text are given using the `-n` command line
arguments. For example, this command will generate a html page consisting of a
two-column table with headers PDF and CDF and images following the glob paths.

  $ koala_table -1 PDF *pdf.png -2 CDF *.png

"""

import argparse
import os
from ._version import get_versions

__version__ = get_versions()["version"]


def get_args():
    MAX_COLUMNS = 5
    parser = argparse.ArgumentParser(
        "koala_table",
        usage=f"koala_table v{__version__}\n" + __doc__
    )
    parser.add_argument("-1", "--column1", required=True, nargs="+")
    for ii in range(2, MAX_COLUMNS + 1):
        parser.add_argument(f"-{ii}", f"--column{ii}", default=None, nargs="+")
    parser.add_argument(
        "--image-size",
        type=int,
        default=500,
        help="Individual image size, defaults to 500",
    )
    parser.add_argument(
        "--page-name",
        type=str,
        default="index.html",
        help="Output name, defaults to index.html",
    )
    args = parser.parse_args()
    return args


def write_to_file(args, body):
    text = ["<!DOCTYPE html>", "<html>", "<body>"]
    text += get_style()
    text += body
    text += ["</body>", "</html>"]
    index_file = f"{args.page_name}"
    with open(index_file, "w+") as f:
        print("\n".join(text), file=f)


def get_style():
    dirname = os.path.dirname(os.path.abspath(__file__))
    style_file = os.path.join(dirname, "simple_style.css")
    with open(style_file, "r") as f:
        style = f.read().split("\n")
    return style


def get_table_list(args):
    """ Generates the ncols x nrows list of files to show in the table """
    ncols = 1
    nrows = len(args.column1)
    table_list = [args.column1]

    col_idx = 2
    while True:
        column_name = f"column{col_idx}"
        if getattr(args, column_name, None) is not None:
            column = getattr(args, column_name)
            ncols += 1
            if len(column) > nrows:
                print(f"Column {col_idx} has more rows than Column 1, truncating")
                column = column[:nrows]
            elif len(column) < nrows:
                print(f"Column {col_idx} has fewer rows than Column 1, fill with None")
                column += [None] * (nrows - len(column))
            table_list.append(column)
            col_idx += 1
        else:
            break

    return table_list


def convert_element_to_HTML(args, element, row=None):
    tag = "td"
    if element is None:
        inner = "N/A"
    elif os.path.isfile(element):
        inner = f'<img src="{element}"  width="{args.image_size}">'
    else:
        inner = element
        # If element is for the first row, set it as table header
        if row == 0:
            tag = "th"
    return f"<{tag}> {inner} </{tag}>"


def convert_table_list_to_body(args, table_list):
    """ Generates the body (a list of HTML strings) """
    body = ['<table style="width:80%">']
    ncols = len(table_list)
    nrows = len(table_list[0])
    for i in range(nrows):
        body += ["<tr>"]
        for j in range(ncols):
            body += [convert_element_to_HTML(args, table_list[j][i], row=i)]
        body += ["</tr>"]
    return body


def main():
    args = get_args()
    table_list = get_table_list(args)
    body = convert_table_list_to_body(args, table_list)
    write_to_file(args, body)
