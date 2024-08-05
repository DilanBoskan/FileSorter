
from collections import defaultdict
from datetime import date
from enum import Enum
import os

from package.group_functions.date import GroupDepth, group_by_date
from package.sorter import *

def retrieve_last_modified(files: list[FilePath]) -> dict[FilePath, date]:
    files_metadata: dict[FilePath, date] = {}
    for file_path in files:
        files_metadata[file_path] = date.fromtimestamp(os.stat(file_path).st_mtime)
    
    return files_metadata

group_by_last_modified_y = lambda files: group_by_date(retrieve_last_modified(files), GroupDepth.YEAR)
group_by_last_modified_ym = lambda files: group_by_date(retrieve_last_modified(files), GroupDepth.YEAR_MONTH)
group_by_last_modified_ymd = lambda files: group_by_date(retrieve_last_modified(files), GroupDepth.YEAR_MONTH_DAY)