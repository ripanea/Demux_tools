# Demuxtiplex tools

This is a set of tools that could be useful when demultiplexing a FASTQ.

The only requirement is ***Python 3***. 

## Barcode counter *(barcode_counter.py)*

This script counts the frequency of all the barcodes present in the FASTQ file. The **input** is *one* FASTQ file 
provided as file or from standard input. The **output** is a tab separated list of barcodes and their count.

Examples of how to run the script:

    # Input directly from file
    ./barcode_counter.py a_fastq_file.fastq.gz > barcode_counts.tsv

    # Input from decompressed standard input
    pigz -p 8 -d a_fastq_file.fastq.gz | ./barcode_counter.py - > barcode_counts.tsv

