# FileSorter

```
usage: File Sorter [-h] [-r [RECURSIVE]] [-c [COPY]] [-f FILTER] [--ignore-case [IGNORE_CASE]] [-g {last-modified-y,last-modified-ym,last-modified-ymd,date-taken-y,date-taken-ym,date-taken-ymd,file-type}] [-v] source output

Sort files recursively. Ability to filter via regex and choose to copy instead of move. Supports various grouping modes.

positional arguments:
  source                Source directory from which the files are pulled
  output                Output directory into which the files are placed

options:
  -h, --help            show this help message and exit
  -r [RECURSIVE], --recursive [RECURSIVE]
                        Recursively search source directory (default: False)
  -c [COPY], --copy [COPY]
                        Copy files into destination directory instead of moving them (default: False)
  -f FILTER, --filter FILTER
                        File types to extract represented as a regex. Use ".*" to select all files (default: .*)
  --ignore-case [IGNORE_CASE]
                        Ignore case-sensitivity when performing filter (default: False)
  -g {last-modified-y,last-modified-ym,last-modified-ymd,date-taken-y,date-taken-ym,date-taken-ymd,file-type}, --group-by {last-modified-y,last-modified-ym,last-modified-ymd,date-taken-y,date-taken-ym,date-taken-ymd,file-type}
                        Grouping method. (last-modified-y = Group by last modified seperated into years, last-modified-ym = Group by last modified seperated into years and then months, last-modified-ymd = Group by last modified seperated into years, months and then days, date-taken-y =
                        Group by date taken seperated into years, date-taken-ym = Group by date taken seperated into years and then months, date-taken-ymd = Group by date taken seperated into years, months and then days, file-type = Group by file type) (default: date-taken-ym)
  -v, --verbose         Verbosity of the programm. (WARNING = 0, INFO = 1, DEBUG = 2) (default: 0)

Author: Dilan Boskan
```
