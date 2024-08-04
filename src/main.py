from collections import defaultdict
from dataclasses import dataclass
from datetime import date
import os
import argparse
from pathlib import Path
from pprint import pprint
from shutil import (rmtree, move, copy2)
from typing import Callable

from package import sorter, group_functions

group_functions_mapper = {
    'last-modified-ym': group_functions.group_by_last_modified_ym
}

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
                    prog='File Date Sorter',
                    description='Sort files by creation date seperated into years and months',
                    formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('source',
                        help="Source directory", type=Path)
    parser.add_argument('output',
                        help="Output directory", type=Path)
    
    parser.add_argument('-r', '--recursive',
                        help="Recursively search source directory", type=bool,
                        const=True, default=False, nargs='?')
    parser.add_argument('-c', '--copy', 
                        help="Copy files into destination directory instead of moving them", type=bool,
                        const=True, default=False, nargs='?')
    parser.add_argument('-f', '--file-types',
                        help="File types to extract. Use '*' to select all files.", type=bool,
                        default=[".jpg", ".png", ".mp4"], nargs='+')
    parser.add_argument('-g', '--group-by', choices=['last-modified-y', 'last-modified-ym', 'last-modified-ymd', 'file-type']
                        help="Grouping method", type=str,
                        default="last-modifed-ym")

    args = parser.parse_args()

    if args.group_by not in group_functions_mapper:
        raise Exception(f'Group by mode "{args.group_by}" does not exist!')
    group_by_callback = group_functions_mapper[args.group_by]
    
    sort_options = sorter.SortOptions(args.source, args.recursive, args.output, args.copy, args.file_types, group_by_callback)

    sorter.run(sort_options)