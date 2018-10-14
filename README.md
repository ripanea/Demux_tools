# Demuxtiplex tools

This is a set of tools that could be useful when demultiplexing a FASTQ.

The only requirement is ***Python 3***. 

## Barcode counter *(barcode_counter.py)*

This script counts the frequency of all the barcodes present in the FASTQ file.

### Usage

The **input** is *one* FASTQ file provided as file or from standard input ("-").

The **output** is a tab separated list of barcodes and their count.

### Examples

    # Input directly from file
    ./barcode_counter.py a_fastq_file.fastq.gz > barcode_counts.tsv

    # Input from decompressed standard input
    pigz -p 8 -d -c a_fastq_file.fastq.gz | ./barcode_counter.py - > barcode_counts.tsv

## Barcode extractor *(barcode_extractor.py)*

This script extracts only the reads that have the specified barcodes.

### Usage

    usage: barcode_extractor.py [-h] [-z] [-x OUTPUT_SUFFIX] -i FASTQS
                                [FASTQS ...] -b BARCODES [BARCODES ...]
    
    optional arguments:
      -h, --help            show this help message and exit
      -z, --compressed      Output is compressed. Much slower!
      -x OUTPUT_SUFFIX, --suffix OUTPUT_SUFFIX
                            Output suffix to be appended to all fastq file names.
                            Default: '_demuxed'.
      -i FASTQS [FASTQS ...], --fastqs FASTQS [FASTQS ...]
                            The path to the fastq files to be demultiplexed.
      -b BARCODES [BARCODES ...], --barcodes BARCODES [BARCODES ...]
                            The set of barcodes that need to be extracted from
                            each fastq file.

The **input** is a list of FASTQ files and one or more barcodes that will be extracted in one single file.

The **output** are FASTQ files that contain only the correctly barcoded reads.

### Examples

    # Extracting reads with barcode ACGTACGT from 4 fastq files
    ./barcode_extractor.py -i FQ1 FQ2 FQ3 FQ4 -b ACGTACGT

    # Extracting reads with barcodes ACGTACGT, NCGTACGT from 2 fastq file with an output prefix of "_filtered"
    ./barcode_extractor.py -x _filtered -i FQ1 FQ2 -b ACGTACGT NCGTACGT

    # Extracting reads with barcode ACGTACGT from 2 fastq files with compressed output. Note: significantly slower
    ./barcode_extractor.py -z -i FQ1 FQ2 -b ACGTACGT