import argparse
import os

# argparse
usage = os.path.basename(__file__) + "--fasta input_fasta --out output_file"
description = "Split fasta into multiple files with individual sequences"
parser = argparse.ArgumentParser(usage=usage, description=description)
parser.add_argument("--fasta", help = "Input fasta file", required=True)
parser.add_argument("--out",   help = "Output directory", required=True)
args = parser.parse_args()

# function to remove problematic characters in sequence names
def edit_name(name):
    name = name.replace('|', '_').replace(':', '').replace(',','').replace(' ', '_')
    if name[-1] == '.':
        name = name[:-1]
    return(name)

# function to split fasta and write to files to output folder
def split_fasta(fasta, output_directory):
    fasta = open(fasta, 'r')
    output_fasta = ''
    for line in fasta:
        if line.startswith('>'):
            if output_fasta != '':
                output_fasta.close()
            sequence_name = line[1:].rstrip('\n')
            sequence_name = edit_name(sequence_name)
            output_fasta = open(output_directory + '/' + sequence_name + ".fasta", 'w')
            output_fasta.write('>'+sequence_name+'\n')
        else:
            output_fasta.write(line)
    output_fasta.close()

# make output dir if it does not exist
if not os.path.exists(args.out):
    os.mkdir(args.out)

# split fasta
split_fasta(args.fasta, args.out)

