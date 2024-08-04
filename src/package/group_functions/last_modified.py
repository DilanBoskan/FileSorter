
from collections import defaultdict
from datetime import date
from enum import Enum
import os

from package.sorter import *

def retrieve_last_modified(files: list[FilePath]) -> dict[FilePath, date]:
    files_metadata: dict[FilePath, date] = {}
    for file_path in files:
        files_metadata[file_path] = date.fromtimestamp(os.stat(file_path).st_mtime)
    
    return files_metadata

def group_by_last_modified_y(files: list[FilePath]) -> GroupedResult:
    # Retrieve data to be sorted by
    files_metadata = retrieve_last_modified(files)

    # Group files by year
    grouped_files: dict[int, list[FilePath]] = defaultdict(lambda: [])
    for prev_file_path in files_metadata:
        year = files_metadata[prev_file_path].year

        grouped_files[year].append(prev_file_path)

    # Convert to GroupedResult
    grouped_result: GroupedResult = []
    for year, values in sorted(grouped_files.items(), key=lambda x: x[0]):
        grouped_result.append((str(year), [], values))

    return grouped_result

def group_by_last_modified_ym(files: list[FilePath]) -> GroupedResult:
    # Retrieve data to be sorted by
    files_metadata = retrieve_last_modified(files)

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
            month_results.append((str(month).zfill(2), [], files))

        grouped_result.append((str(year), month_results, []))

    return grouped_result

def group_by_last_modified_ymd(files: list[FilePath]) -> GroupedResult:
    # Retrieve data to be sorted by
    files_metadata = retrieve_last_modified(files)
    
    # Group files by year and month
    grouped_files: dict[int, dict[int, dict[int, list[FilePath]]]] = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: [])))
    for prev_file_path in files_metadata:
        year = files_metadata[prev_file_path].year
        month = files_metadata[prev_file_path].month
        day = files_metadata[prev_file_path].day

        grouped_files[year][month][day].append(prev_file_path)

    # Convert to GroupedResult
    grouped_result: GroupedResult = []
    for year, year_values in sorted(grouped_files.items(), key=lambda x: x[0]):
        month_results: list[Result] = []
        for month, month_values in sorted(year_values.items(), key=lambda x: x[0]):
            day_results: list[Result] = []
            for day, files in sorted(month_values.items(), key=lambda x: x[0]):
                day_results.append((str(day).zfill(2), [], files))

            month_results.append((str(month).zfill(2), day_results, []))

        grouped_result.append((str(year), month_results, []))

    return grouped_result