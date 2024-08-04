from collections import defaultdict
from dataclasses import dataclass
from datetime import date
from enum import Enum
import os
import argparse
from pathlib import Path
from pprint import pprint
import re
from shutil import (rmtree, move, copy2)
from typing import Callable
import logging

from package import sorter, helper
from package.group_functions import (group_by_last_modified_y, group_by_last_modified_ym, group_by_last_modified_ymd)

class Verbosity(Enum):
    WARNING = 0
    INFO = 1
    DEBUG = 2

def is_regex_type(value: str):
    if not helper.is_regex(value):
        raise argparse.ArgumentTypeError(f'"{value}" is not a valid regex!')
    return value
    
    
if __name__ == '__main__':
    verbosity_list = str.join(", ", [f"{v.name} = {v.value}" for v in Verbosity])

    group_functions_mapper = {
        'last-modified-y': group_by_last_modified_y,
        'last-modified-ym': group_by_last_modified_ym,
        'last-modified-ymd': group_by_last_modified_ymd
    }
    log_level_mapper = {
        Verbosity.WARNING: logging.WARNING,
        Verbosity.INFO: logging.INFO,
        Verbosity.DEBUG: logging.DEBUG,
    }

    parser = argparse.ArgumentParser(
                    prog='File Sorter',
                    description='Sort files',
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
    parser.add_argument('-f', '--filter',
                        help='File types to extract represented as a regex. Use ".*" to select all files', type=is_regex_type,
                        default='.*')
    parser.add_argument('--ignore-case',
                        help='Ignore case-sensitivity when performing regex', type=bool,
                        const=True, default=False, nargs='?')
    parser.add_argument('-g', '--group-by', choices=['last-modified-y', 'last-modified-ym', 'last-modified-ymd', 'file-type'],
                        help="Grouping method", type=str,
                        default="last-modified-ym")
    parser.add_argument('-v', '--verbose',
                        help=f'Verbosity of the programm. ({verbosity_list})',
                        
                        action='count', default=0)

    args = parser.parse_args()

    # Process args
    if args.group_by not in group_functions_mapper:
        raise Exception(f'Group-by mode "{args.group_by}" does not exist!')
    group_by_callback = group_functions_mapper[args.group_by]

    if (verbosity := Verbosity(args.verbose)) not in log_level_mapper:
        raise Exception(f'Verbosity of level "{args.verbose}" does not exist!')
    log_level = log_level_mapper[verbosity]
    
    file_filter = re.compile(args.filter, re.IGNORECASE if args.ignore_case else 0)

    sort_options = sorter.SortOptions(args.source, args.recursive, args.output, args.copy, file_filter, group_by_callback)

    # Set up logger
    logger = logging.getLogger()
    logger.setLevel(log_level)
    handler = logging.StreamHandler()
    handler.setFormatter(helper.CustomFormatter())
    logger.addHandler(handler)

    # Run sorter
    sorter.run(sort_options)