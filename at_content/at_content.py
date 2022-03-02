
import argparse
import os

# argparse
usage = os.path.basename(__file__) + " --fasta input_fasta --out output_file"
description = "AT content of sequences in a fasta"
parser = argparse.ArgumentParser(usage=usage, description=description)
parser.add_argument("--fasta", help = "Input fasta file", required=True)
parser.add_argument("--out",   help = "Output file",      required=True)
args = parser.parse_args()

# read fasta
def read_fasta(filename):
    name, seq = None,""
    with open(filename, 'r') as fasta:
        for line in fasta:
            if line.startswith('>') and name == None:
                name = line.rstrip('\n').replace('>','')
            else:
                if line.startswith('>') and name != None:
                    yield [name, seq]
                    name = line.rstrip('\n').replace('>','')
                    seq = ''
                else:
                    seq = seq + line.rstrip('\n')
        yield [name, seq]

# at content
def at_content(seq):
    return (seq.count("A") + seq.count("T")) / len(seq)
assert at_content("ATCG") == 0.5

#
fa = read_fasta(args.fasta)
with open(args.out, "w") as out:
    for name, sequence in fa:
        out.write(name + "\t" + str(at_content(sequence)) + "\n")

