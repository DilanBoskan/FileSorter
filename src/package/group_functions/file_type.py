
import os
from package.sorter import FilePath, GroupedResult


def group_by_file_type(files: list[FilePath]) -> GroupedResult:
    extensions = {}

    for f in files:
        ext = os.path.splitext(f)[1][1:].upper()
        if ext not in extensions:  
            extensions[ext] = []

        extensions[ext].append(f)

    result: GroupedResult = []
    for ext, values in extensions.items():
        result.append((ext, [], values))
        
    return result