from collections import defaultdict
from datetime import datetime
from datetime import date
from enum import Enum
from package.sorter import FilePath, GroupedResult, Result

class GroupDepth(Enum):
    YEAR = 0
    YEAR_MONTH = 1
    YEAR_MONTH_DAY = 2

def group_by_date(files_metadata: dict[FilePath, date], depth: GroupDepth) -> GroupedResult:
    # Extract all with invalid date
    invalid_files = []
    for file_path, _ in filter(lambda f: f[1] == date.min, list(files_metadata.items())):
        invalid_files.append(file_path)
        del files_metadata[file_path]
    
    grouped_files: dict[int, dict[int, dict[int, list[FilePath]]]] = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: [])))
    for file_path in files_metadata:
        year = files_metadata[file_path].year
        month = files_metadata[file_path].month
        day = files_metadata[file_path].day

        grouped_files[year][month][day].append(file_path)

    # Convert to GroupedResult
    grouped_result: GroupedResult = []
    
    for year, year_values in sorted(grouped_files.items(), key=lambda x: x[0]):
        if depth == GroupDepth.YEAR:
            all_files: list[FilePath] = []
            for month, month_values in sorted(year_values.items(), key=lambda x: x[0]):
                for day, files in sorted(month_values.items(), key=lambda x: x[0]):
                    all_files.extend(files)

            grouped_result.append((str(year), [], all_files))
        elif depth == GroupDepth.YEAR_MONTH:
            all_month_files: list[Result] = []
            for month, month_values in sorted(year_values.items(), key=lambda x: x[0]):
                all_files: list[FilePath] = []
                for day, files in sorted(month_values.items(), key=lambda x: x[0]):
                    all_files.extend(files)
                all_month_files.append((str(month).zfill(2), [], all_files))

            grouped_result.append((str(year), all_month_files, []))
        elif depth == GroupDepth.YEAR_MONTH_DAY:
            all_month_files: list[Result] = []
            for month, month_values in sorted(year_values.items(), key=lambda x: x[0]):
                all_day_files: list[Result] = []
                for day, files in sorted(month_values.items(), key=lambda x: x[0]):
                    all_day_files.append((str(day).zfill(2), [], files))

                all_month_files.append((str(month).zfill(2), all_day_files, []))

            grouped_result.append((str(year), all_month_files, []))

    if len(invalid_files):
        grouped_result.append(("No date", [], invalid_files))

    return grouped_result
