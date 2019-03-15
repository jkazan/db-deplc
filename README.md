# wetch - conky and lua for system monitoring

Detach .db file from all PLC dependency, allowing for simple testing and OPI development without any PLC connected.

#### Usage
```sh
usage: deplc.py [-h] original_path copy_path

Remove PLC dependent db code

positional arguments:
  original_path  Path to original file
  copy_path      Path to new copy

optional arguments:
  -h, --help     show this help message and exit
```