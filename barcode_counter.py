#!/usr/bin/env python3
import sys
import os
import logging
import gzip


def get_barcodes(file_obj):

    # Initialize the barcode count table
    barcodes = {}

    # Initialize read counter
    reads_processed = 0

    # Get reads from file handler object
    for line in file_obj:

        # Convert to string if bytes sequence
        if isinstance(line, bytes):
            line = line.decode("utf-8")

        # Obtain the actual barcode
        barcode = line.strip().rsplit(":", 1)[1]

        # Initialize the barcode in the dictionary if not present yet
        if barcode not in barcodes:
            barcodes[barcode] = 0

        # Increment the barcode count
        barcodes[barcode] += 1

        # Read the next three lines as we only care of the barcode
        for _ in range(3):
            file_obj.readline()

        # Count the currently processed line
        reads_processed += 1

        # Log the progress
        if reads_processed % 10000 == 0:
            sys.stderr.write("Processed reads: {0}\r".format(reads_processed))

    return barcodes


def main():

    # Obtain input file path
    input_fastq = sys.argv[1]

    # Create file handle
    if input_fastq == "-":
        # Input is from standard input
        barcodes = get_barcodes(sys.stdin)
    else:
        # Input is a file
        # Check if the file exists
        if not os.path.exists(input_fastq):
            logging.error("Fastq file '{0}' not found!".format(input_fastq))
            raise IOError("Input file not found!")

        if input_fastq.lower().endswith(".gz"):
            with gzip.open(input_fastq, "rb", encoding="utf-8") as inp:
                barcodes = get_barcodes(inp)
        else:
            with open(input_fastq, "r", encoding="utf-8") as inp:
                barcodes = get_barcodes(inp)

    # Print barcodes sorted by their count
    for barcode, count in sorted(barcodes.items(), key=lambda item: item[1], reverse=True):
        print("{0}\t{1}".format(barcode, count))


if __name__ == "__main__":
    main()
