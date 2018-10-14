#!/usr/bin/env python3
import os
import gzip
import argparse
import logging
from multiprocessing import Process


class BarcodeExtractor(Process):

    def __init__(self, input_file, barcodes, output_suffix, gz_output):

        super(BarcodeExtractor, self).__init__()

        self.input_file = input_file
        self.barcodes = barcodes
        self.output_suffix = output_suffix
        self.gz_output = gz_output

        self.daemon = True

    def _get_input_file_handler(self):

        if self.input_file.lower().endswith(".gz"):
            return gzip.open(self.input_file, "rb")
        else:
            return open(self.input_file, "rb")

    def _get_output_file_handler(self):

        if self.input_file.lower().endswith(".gz"):
            data = self.input_file.rsplit(".", 2)
            basename = data[0]
            extension = ".".join(data[1:])

        else:
            basename, extension = self.input_file.rsplit(".", 1)

        output_filename = "{0}{1}.{2}".format(basename, self.output_suffix, extension)

        if self.gz_output:
            return gzip.open(output_filename, "wb")
        else:
            return open(output_filename.replace(".gz", ""), "wb")

    def run(self):

        reads_processed = 0

        print("({0}) Started processing.".format(self.input_file))

        with self._get_output_file_handler() as out:
            with self._get_input_file_handler() as inp:
                for line in inp:

                    # Convert to string if bytes sequence
                    decoded_line = line.decode("utf-8")

                    # Get the barcode of the read
                    barcode = decoded_line.strip().rsplit(":", 1)[1]

                    # Log the progress
                    reads_processed += 1
                    if reads_processed % 10**6 == 0:
                        print("({0}) Processed reads: {1}M".format(self.input_file, int(reads_processed/10**6)))

                    # Check if the barcode is the required one
                    if barcode not in self.barcodes:

                        # Skip the read information
                        for _ in range(3):
                            inp.readline()

                        # Continue to next read
                        continue

                    # Write read to output file
                    out.write(line)
                    for _ in range(3):
                        out.write(inp.readline())

        print("({0}) Finished processing.".format(self.input_file))


def configure_argparser(argparser_obj):

    # Compressed output
    argparser_obj.add_argument("-z", "--compressed",
                               action="store_true",
                               dest="gz_output",
                               required=False,
                               default=False,
                               help="Output is compressed. Much slower!")

    # Output suffix
    argparser_obj.add_argument("-x", "--suffix",
                               action="store",
                               dest="output_suffix",
                               required=False,
                               default="_demuxed",
                               help="Output suffix to be appended to all fastq file names. Default: '_demuxed'.")

    # List of fastq files
    argparser_obj.add_argument("-i", "--fastqs",
                               action="store",
                               nargs="+",
                               dest="fastqs",
                               required=True,
                               help="The path to the fastq files to be demultiplexed.")

    # List of barcodes to be extracted
    argparser_obj.add_argument("-b", "--barcodes",
                               action="store",
                               nargs="+",
                               dest="barcodes",
                               required=True,
                               help="The set of barcodes that need to be extracted from each fastq file.")


def main():

    # Generate argument parser
    argparser_obj = argparse.ArgumentParser()

    # Configure argparser
    configure_argparser(argparser_obj)

    # Parse arguments
    args = argparser_obj.parse_args()

    # Check if all FASTQ files are present
    for fastq in args.fastqs:
        if not os.path.exists(fastq):
            logging.error("Fastq file '{0}' not found!".format(fastq))
            raise IOError("Input file not found!")

    # Create an extractor for each fastq file
    extractors = [BarcodeExtractor(fastq, args.barcodes, args.output_suffix, args.gz_output) for fastq in args.fastqs]

    # Start all extractors
    for extractor in extractors:
        extractor.start()

    # Wait for all extractors to finish
    for extractor in extractors:
        extractor.join()


if __name__ == "__main__":
    main()
