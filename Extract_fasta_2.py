# this file used to extract all blastp hit sequences per query gene
# used command: python Extract_fasta_2.py Protein_database.fa Blastp_result.txt
# please note the blastp_result file will only contain the query id you want to extrace and their hits 

import sys

f1 = open(sys.argv[2],'r')

All_list, Check_list, Final_list = [],[],[]
ID1, ID2, ID3, Last_id = '','','',''

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

for line in f1:
    ID1 = line.split()[0]
    ID2 = line.split()[1]
    if ID1 not in Check_list:
        if len(Check_list) == 0:
            All_list.append(ID2)
            Check_list.append(ID1)
        else:
            New_file = open(Last_id + '.fa','w')
            Final_list = set((All_list))
            with open(sys.argv[1],'r') as files:
                for name,seq in read_fasta(files):
                    ID3 = name.split()[0]
                    if ID3[1:] in All_list:
                        print >> New_file, '>' + ID3
                        print >> New_file, seq
            All_list = []
            All_list.append(ID2)
            Check_list.append(ID1)
    else:
        All_list.append(line.split()[1])
    Last_id = ID1
New_file = open(Last_id + '.fa','w')
Final_list = set((All_list))
with open(sys.argv[1],'r') as files:
    for name,seq in read_fasta(files):
        ID3 = name.split()[0]
        if ID3[1:] in All_list:
            print >> New_file, '>' + ID3
            print >> New_file, seq
f1.close()
New_file.close()
