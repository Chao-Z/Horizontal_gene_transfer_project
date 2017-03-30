# used to extract fasta sequences from 50 to 100 in HGT identify 
# command: python Extract_fasta_1.py file1(protein file) file2(blastp result) file3(ID file)
# file3 is the id file containing the id you want to extract
import sys

f2 = open(sys.argv[2],'r')
f3 = open(sys.argv[3],'r')

All_list = set((line.split()[0] for line in f3))
Check_id_list = []
B_id = []
in_accession_ids = False
Last_ID,Final_ID = '',''
# function for parse fasta sequences in id and sequences
def read_fasta(file):
    name,seq = None,[]
    for line in file:
        line = line.rstrip()
        if line.startswith('>'):
            if name:yield(name,''.join(seq))
            name, seq = line, []
        else:
            seq.append(line)
    if name: yield (name, ''.join(seq))

# find plant and non_plant id per query
for line in f2:
    ID1 = line.split()[0]
    ID2 = line.split()[1]
    if ID1 in All_list:
        if len(Check_id_list) == 0:
            Check_id_list.append(ID1)
            if ID2[0] != 'A':
                B_id.append(ID2)
        if ID1 in Check_id_list:
            Final_ID = ID1
            if ID2 not in B_id and ID2[0] != 'A':
                B_id.append(ID2)
        if ID1 not in Check_id_list:
            Check_id_list.append(ID1)
            New_file = open(Last_ID + '.fa','w')
            New_B_id = []
            if len(B_id) >= 100:
                New_B_id = B_id[0:100]
            else:
                New_B_id = B_id
            with open(sys.argv[1]) as files:
                for name,seq in read_fasta(files):
                    accessorID = name.split()[0]
                    accessorID_1 = accessorID[1:]
                    in_accession_ids = accessorID_1 in New_B_id
                    if in_accession_ids:
                        print >> New_file, name
                        print >> New_file, seq
            B_id = []
            if ID2[0] != 'A':
                B_id.append(ID2)
        Last_ID = ID1
New_file = open(Final_ID + '.fa','w')
New_B_id = []
if len(B_id) >= 100:
    New_B_id = B_id[0:100]
else:
    New_B_id = B_id
with open(sys.argv[1]) as files:
    for name,seq in read_fasta(files):
        accessorID = name.split()[0]
        accessorID_1 = accessorID[1:]
        in_accession_ids = accessorID_1 in New_B_id
        if in_accession_ids:
            print >> New_file, name
            print >> New_file, seq
f2.close()
f3.close()
New_file.close()
