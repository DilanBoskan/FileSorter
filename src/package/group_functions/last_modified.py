
from collections import defaultdict
from datetime import date
from enum import Enum
import os

from sorter import *

def group_by_last_modified_ym(files: list[FilePath]) -> GroupedResult:
    # Retrieve data to be sorted by
    files_metadata: dict[FilePath, date] = {}
    for file_path in files:
        files_metadata[file_path] = date.fromtimestamp(os.stat(file_path).st_mtime)

    # Group files by year and month
    grouped_files: dict[int, dict[int, list[FilePath]]] = defaultdict(lambda: defaultdict(lambda: []))
    for prev_file_path in files_metadata:
        year = files_metadata[prev_file_path].year
        month = files_metadata[prev_file_path].month

        grouped_files[year][month].append(prev_file_path)

    # Convert to GroupedResult
    grouped_result: GroupedResult = []
    for year, values in sorted(grouped_files.items(), key=lambda x: x[0]):
        month_results: list[Result] = []
        for month, files in sorted(values.items(), key=lambda x: x[0]):
            month_result: Result = (str(month).zfill(2), [], files)
            month_results.append(month_result)

        grouped_result.append((str(year), month_results, []))

    return grouped_result
