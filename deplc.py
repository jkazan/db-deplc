#!/usr/bin/env python3
#
#  Copyright (c) 2019 Johannes C. Kazantzidis
#
#  The program is free software: You can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published
#  by the Free Software Foundation.
#
#  This program is provided as is, WITHOUT ANY WARRANTY. See the GNU General
#  Public License for more details.
#
#  You should have received a copy of the GNU General Public License along with
#  this program. If not, see https://www.gnu.org/licenses/gpl.txt

import argparse
import os
import re

__version__ = '1.0'
__author__ = 'Johannes C. Kazantzidis'

def dePLC(original_path, copy_path, bad_records, bad_words, io_intr):
    """Detach .db file from all PLC dependency.

    Args:
        original_path: Path to original file.
        copy_path: Path to new file, detached from PLC.
        bad_records: List of strings indicating a record to skip.
        bad_words: List of strings indicating line to skip.
        io_intr: Scan time to replace "I/O Intr".
    """
    bad_record_flag = False
    with open(original_path) as old_file, open(copy_path, "w") as new_file:
        for line in old_file:
            if bad_record_flag:
                if not "record(" in line:
                    continue
                else:
                    bad_record_flag = False
            if not any(bad_word in line for bad_word in bad_words):
                if any(bad_record in line for bad_record in bad_records):
                    bad_record_flag = True
                    continue

                if "I/O Intr" in line:
                    line = re.sub("I/O Intr", ".5 second", line)

                new_file.write(line)

def main(original_path, copy_path):
    """Detach .db file from all PLC dependency.

    Args:
        original_path: Path to original file.
        copy_path: Path to new file, detached from PLC.
    """
    # If a line contains any of these strings, it will skip the record
    bad_records = ["record(asyn"]

    # If a line contains any of these strings, it will skip the line
    bad_words = [
        "@asyn",
        "@$(PLCNAME)",
        "asynInt32",
        "asynUInt32Digital",
        "S7plc",
        "T=",
        "asynFloat"
        ]

    # Scan time as replacement for "I/O Intr"
    io_intr = ".5 second"

    # Parse original file and write to new copy
    dePLC(original_path, copy_path, bad_records, bad_words, io_intr)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Remove PLC dependent db code")
    parser.add_argument("original_path", type=str, help="Path to original file")
    parser.add_argument("copy_path", type=str, help="Path to new copy")
    args = parser.parse_args()
    main(args.original_path, args.copy_path)
