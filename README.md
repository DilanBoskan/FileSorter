# FileSorter

```
usage: File Sorter [-h] [-r [RECURSIVE]] [-c [COPY]] [-f FILE_TYPES [FILE_TYPES ...]] [-g {last-modified-y,last-modified-ym,last-modified-ymd,file-type}] source output

Sort files

positional arguments:
  source                Source directory
  output                Output directory

options:
  -h, --help            show this help message and exit
  -r [RECURSIVE], --recursive [RECURSIVE]
                        Recursively search source directory (default: False)
  -c [COPY], --copy [COPY]
                        Copy files into destination directory instead of moving them (default: False)
  -f FILE_TYPES [FILE_TYPES ...], --file-types FILE_TYPES [FILE_TYPES ...]
                        File types to extract. Use '*' to select all files. (default: ['.jpg', '.png', '.mp4'])
  -g {last-modified-y,last-modified-ym,last-modified-ymd,file-type}, --group-by {last-modified-y,last-modified-ym,last-modified-ymd,file-type}
                        Grouping method (default: last-modifed-ym)
```
