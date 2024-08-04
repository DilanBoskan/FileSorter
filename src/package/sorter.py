from dataclasses import dataclass
import os
from pathlib import Path
from shutil import copy2, move, rmtree
from typing import Callable

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
    file_types: list[str]
    group_by_callback: Callable[[list[FilePath]], GroupedResult]

def run(options: SortOptions):
    # Validation
    if not options.input.exists():
        raise Exception(f'Input directory "{options.input}" does not exist!')
    if not options.input.is_dir():
        raise Exception(f'Input directory "{options.input}" is not a directory!')
    if not options.output.exists():
        r = input(f'Output directory "{options.output}" does not exist. Do you wish to create it? (Y/N) ')
        if (r.lower()[0] != 'y'):
            print('Canceled!')
            return
        os.mkdir(options.output)
    if not options.output.is_dir():
        raise Exception(f'Output directory "{options.input}" is not a directory!')
    if len(os.listdir(options.output)) > 0:
        r = input(f'Output directory "{options.output}" contains folders or files. PROCEEDING WILL DELETE ALL FOLDERS AND FILES IN THE OUTPUT FOLDER. Do you wish to continue it? (Y/N) ')
        if (r.lower()[0] != 'y'):
            print('Canceled!')
            return
        rmtree(options.output)
        os.mkdir(options.output)
        
    # Collect all files
    all_files = os.walk(options.input) if options.recursive else [[str(options.input), [], [item for item in os.listdir(options.input) if os.path.isfile(os.path.join(options.input, item))]]]
    
    filtered_files = [ \
        os.path.join(result[0], filtered_file_name)
        for result in all_files
        for filtered_file_name in result[2] if any([filtered_file_name.lower().endswith(file_type.lower()) for file_type in options.file_types])
        ][:10]
    
    # Group results
    grouped_result = options.group_by_callback(filtered_files)

    def recursive_process_result(base_dir: str, results: list[Result]):
        for result in results:
            result_dir = os.path.join(base_dir, result[0])
            os.mkdir(result_dir)

            # Sub results
            recursive_process_result(result_dir, result[1])

            # Files
            for prev_file_path in result[2]:
                new_file_path = os.path.join(result_dir, os.path.basename(prev_file_path))

                # Make sure there are no duplicates
                base_name, base_ext = os.path.splitext(os.path.basename(prev_file_path))   
                while os.path.exists(new_file_path):
                    n = 1
                    while True:
                        new_file_path = os.path.join(result_dir, '{}_{:0>2}.{}'.format(base_name, n, base_ext))
                        n += 1

                if options.copy:
                    copy2(prev_file_path, new_file_path)
                else:
                    move(prev_file_path, new_file_path)
    
    recursive_process_result(str(options.output), grouped_result)
