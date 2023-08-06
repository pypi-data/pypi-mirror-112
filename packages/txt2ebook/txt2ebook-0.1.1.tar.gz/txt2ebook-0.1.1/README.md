# txt2ebook

Console tool to convert txt file to different ebook format.

## Installation

From PyPI:

```
pip install txt2ebook
```

## Usage

Showing help message:

```
txt2ebook --help
Usage: txt2ebook [OPTIONS] FILENAME

Options:
  --help  Show this message and exit.
```

If no file was specified:

```
txt2ebook
Usage: txt2ebook [OPTIONS] FILENAME
Try 'txt2ebook --help' for help.

Error: Missing argument 'FILENAME'.
```

Convert a txt file into epub:

```
txt2book ebook.txt
```

## Copyright and License

Copyright (C) 2021 Kian-Meng, Ang

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
