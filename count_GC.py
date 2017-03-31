import sys

f2 = open(sys.argv[2],'w')

def read_fasta(file_name):
    name,seq = None,[]
    for line in file_name:
        line = line.rstrip()
        if line.startswith(">"):
            if name:yield(name,''.join(seq))
            name, seq = line, []
        else:
            seq.append(line)
    if name: yield (name, ''.join(seq))

print >> f2, 'Gene_id' + '\t' + 'GC_content' + '\t' + 'GC_skew'
with open(sys.argv[1],'r') as files:
    for name,seq in read_fasta(files):
        Seq_str = seq.strip().upper()
        Count_G = Seq_str.count('G')
        Count_C = Seq_str.count('C')
        GC_content = (Count_G + Count_C) / float(len(Seq_str))
        GC_skew = (Count_G - Count_C) / float((Count_G + Count_C))
        print >> f2, name.split()[0][1:] + '\t' + str(GC_content) + '\t' + str(GC_skew)

f2.close()
