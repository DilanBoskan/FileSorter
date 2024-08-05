
from collections import defaultdict
from datetime import datetime, date
from enum import Enum
import os
from hachoir.parser import createParser
from hachoir.metadata import extractMetadata
from package.group_functions.date import GroupDepth, group_by_date
from package.sorter import *
from PIL import Image
import hachoir.core.config

hachoir.core.config.quiet = True

def get_date_taken(path) -> date:
    try:
        exif = Image.open(path).getexif()
        
        if not exif:
            # Image does not have EXIF data
            return date.min
        
        if 36867 in exif:
            return datetime.strptime(exif[36867], '%Y:%m:%d %H:%M:%S')

        if 306 in exif:
            return datetime.strptime(exif[306], '%Y:%m:%d %H:%M:%S')
    except:
        pass

    try:
        parser = createParser(path)
        if not parser:
            return date.min

        with parser:
            metadata = extractMetadata(parser)
            if not metadata:
                return date.min
            
            for line in metadata.exportPlaintext():
                if line.split(':')[0] == '- Creation date':
                    parsed_date = datetime.strptime(line.split(':')[1].split()[0], "%Y-%m-%d")
                    return parsed_date
    
        return date.min
    except:
        return date.min

def retrieve_date_taken(files: list[FilePath]) -> dict[FilePath, date]:
    files_metadata: dict[FilePath, date] = {}

    for file_path in files:
        files_metadata[file_path] = get_date_taken(file_path)

    return files_metadata

group_by_date_taken_y = lambda files: group_by_date(retrieve_date_taken(files), GroupDepth.YEAR)
group_by_date_taken_ym = lambda files: group_by_date(retrieve_date_taken(files), GroupDepth.YEAR_MONTH)
group_by_date_taken_ymd = lambda files: group_by_date(retrieve_date_taken(files), GroupDepth.YEAR_MONTH_DAY)