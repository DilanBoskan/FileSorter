from __future__ import absolute_import
from dataclasses import dataclass, asdict
from enum import Enum
import json
import os
from pathlib import Path
from pprint import pformat
import re
from shutil import copy2, move, rmtree
from textwrap import indent
from typing import Callable, Optional, Pattern
import logging
from alive_progress import alive_bar
from . import helper

FilePath = str
DirName = str
Result = tuple[DirName, list["Result"], list[FilePath]]
GroupedResult = list[Result]

@dataclass
class SortOptions:
    input: Path
    recursive: bool
    output: Path
    copy: bool
    filter: Pattern
    group_by_callback: Callable[[list[FilePath]], GroupedResult]


def warning_get_user_input(message: str) -> str:
    logger.warning(message)
    r = input()
    logger.debug(f'User inputted "{r}"')

    return r

logger = logging.getLogger(__name__)

def run(options: SortOptions):
    logger.debug(f'Running sorter with options:\n{indent(pformat(asdict(options), indent=2, sort_dicts=False), "     ")}')
    
    # Validation
    logger.debug(f'Validating inputs')
    if not options.input.exists():
        raise Exception(f'Input directory "{options.input}" does not exist!')
    if not options.input.is_dir():
        raise Exception(f'Input directory "{options.input}" is not a directory!')
    if not options.output.exists():
        r = warning_get_user_input(f'Output directory "{options.output}" does not exist. Do you wish to create it? (Y/N)')

        if r.lower()[0] != 'y':
            logger.info('Canceled!')
            return
        os.mkdir(options.output)
    if not options.output.is_dir():
        raise Exception(f'Output directory "{options.input}" is not a directory!')
    if len(os.listdir(options.output)) > 0:
        r = warning_get_user_input(f'Output directory "{options.output}" contains folders or files. Do you wish to delete, append or cancel? (D/A/C)')

        if r.lower()[0] == 'd':
            r = warning_get_user_input(f'ALL FOLDERS AND FILES IN THE OUTPUT DIRECTORY "{options.output}" WILL BE PERMANENTLY DELETED. Do you wish to continue? (Y/N)')

            if r.lower()[0] != 'y':
                logger.info('Canceled!')
                return
            
            # Delete
            logger.debug(f'User chose to delete contents of output directory')
            rmtree(options.output)
            os.mkdir(options.output)
        elif r.lower()[0] == 'a':
            # Append
            logger.debug(f'User chose to append to output directory')
        else:
            logger.info('Canceled!')
            return
        
    # Collect all files
    logger.info('Collecting files')
    all_files = os.walk(options.input) if options.recursive else [[str(options.input), [], [item for item in os.listdir(options.input) if os.path.isfile(os.path.join(options.input, item))]]]
    
    logger.info('Filtering files')
    filtered_files = [ \
        os.path.join(result[0], filtered_file_name)
        for result in all_files
        for filtered_file_name in result[2] if re.match(options.filter, filtered_file_name)
        ]
    logger.debug(f'Aggregated {len(filtered_files)} files')
    
    # Group results
    logger.info('Grouping files')
    grouped_result = options.group_by_callback(filtered_files)

    def recursive_process_result(base_dir: str, results: list[Result], progress_tracker: Optional[Callable[[], None]] = None):
        for result in results:
            result_dir = os.path.join(base_dir, result[0])
            if not os.path.isdir(result_dir):
                os.mkdir(result_dir)

            # Sub results
            recursive_process_result(result_dir, result[1], progress_tracker)

            # Files
            for prev_file_path in result[2]:
                new_file_path = os.path.join(result_dir, os.path.basename(prev_file_path))

                # Make sure there are no duplicates
                base_name, base_ext = os.path.splitext(os.path.basename(prev_file_path))   
                n = 1
                while os.path.exists(new_file_path):
                    new_file_path = os.path.join(result_dir, '{}_{:0>2}.{}'.format(base_name, n, base_ext))
                    n += 1

                if options.copy:
                    copy2(prev_file_path, new_file_path)
                else:
                    move(prev_file_path, new_file_path)
    
                if progress_tracker:
                    progress_tracker()
    
    logger.info('Moving/copying files')

    with alive_bar(len(filtered_files)) as next_it:
        recursive_process_result(str(options.output), grouped_result, next_it)

    logger.info("Finished!")
