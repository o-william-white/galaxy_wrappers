import argparse

# argparse
usage = "python get_kmers.py --input example.fasta --kmer_size  kmer_size"
description = "Return kmers counts for sequences in a fasta file."
parser = argparse.ArgumentParser(usage=usage, description=description)
parser.add_argument("--fasta",     help = "Input fasta/q file", required=True)
parser.add_argument("--kmer_size", help = "Kmer size", required=True, type=int)
args = parser.parse_args()

# function to read fasta
def read_fasta(filename):
    name, seq = None,""
    fasta = open(filename, "r")
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
    fasta.close()

# function to create dict of kmers of length k in a given fasta file
def get_kmers(fasta, k):
    kmer_dict = {}
    for name, seq in fasta:
        for i in range(len(seq)-k+1):
            kmer = seq[i:i+k]
            if kmer_dict.get(kmer) == None:
                kmer_dict[kmer] = 1
            else:
                kmer_dict[kmer] = kmer_dict[kmer] + 1
    return kmer_dict

# read fasta
fasta = read_fasta(args.fasta)

# create dict
kmer_dict = get_kmers(fasta, args.kmer_size)

# write kmer counts
kmer_out = open("kmer_counts.txt", "w")
for kmer, count in kmer_dict.items():
    kmer_out.write(kmer + "\t" + str(count) + "\n")
kmer_out.close()

# write log file
kmer_log = open("log.txt", "w")
kmer_log.write(str(len(kmer_dict)) + " kmers identified")
kmer_log.close()

