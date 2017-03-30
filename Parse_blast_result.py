# the first script for hgt: based on formula to parse blast result to get potential id
# used command: python Parse_blast_result.py blastp_result_file parse_out_result_file
# the blastp_result_file should be sort with query id !!!

import sys
import math
from math import log


f1 = open(sys.argv[1],'r')
f2 = open(sys.argv[2],'w')

f2.write('Gene_ID' + '\t' + 'HGT_evalue' + '\t' + 'A_evalue' + '\t' + 'B_evalue' + '\t' + 'HGT_score' + '\t' + 'A_score' + '\t' + 'B_score' + '\t' + 'HGT_identify' + '\t' + 'A_identify' + '\t' + 'B_identify' + '\n')

List1 = []
last_Evalue_A,last_Evalue_B = 1,1
last_score_A, last_score_B = 0,0
last_identify_A, last_identify_B = 0,0
for line in f1:
    sply = line.split()
    ID1 = sply[0]
    ID2 = sply[1]
    Identify = float(sply[2])
    Evalue = float(sply[10])
    Score = float(sply[11])
    if len(List1) == 0:
        List1.append(ID1)
        if ID2[0] == 'A':
            last_Evalue_A = Evalue
            last_score_A = Score
            last_identify_A = Identify
        if ID2[0] != 'A':
            last_Evalue_B = Evalue
            last_score_B = Score
            last_identify_B = Identify
    else:
        if ID1 in List1:
            if ID2[0] == 'A':
                last_Evalue_A = min(Evalue,last_Evalue_A)
                last_score_A = max(Score,last_score_A)
                last_identify_A = max(Identify,last_identify_A)
            if ID2[0] != 'A':
                last_Evalue_B = min(Evalue,last_Evalue_B)
                last_score_B = max(Score,last_score_B)
                last_identify_B = max(Identify,last_identify_B)
        if ID1 not in List1:
            HGT_AI = math.log(last_Evalue_A + 1e-180) - math.log(last_Evalue_B + 1e-180)
            HGT_Index = last_score_B - last_score_A
            HGT_Identify = last_identify_B - last_identify_A
            f2.write(last_ID1 + '\t' + str(HGT_AI) + '\t' + str(last_Evalue_A) + '\t' + str(last_Evalue_B) + '\t' + str(HGT_Index) + '\t' + str(last_score_A) + '\t' + str(last_score_B) + '\t' + str(HGT_Identify) + '\t' + str(last_identify_A) + '\t' + str(last_identify_B) + '\n')
            List1.append(ID1)
            if ID2[0] == 'A':
                last_Evalue_A,last_Evalue_B = Evalue,1
                last_score_A,last_score_B = Score,0
                last_identify_A,last_identify_B = Identify,0
            if ID2[0] != 'A':
                last_Evalue_B,last_Evalue_A = Evalue,1
                last_score_B,last_score_A = Score,0
                last_identify_B,last_identify_A = Identify,0
    last_ID1 = ID1
if sply != '': f2.write(last_ID1 + '\t' + str(math.log(last_Evalue_A + 1e-180) - math.log(last_Evalue_B + 1e-180)) + '\t' + str(last_Evalue_A) + '\t' + str(last_Evalue_B) + '\t' + str(last_score_B - last_score_A) + '\t' + str(last_score_A) + '\t' + str(last_score_B) + '\t' + str(last_identify_B - last_identify_A) + '\t' + str(last_identify_A) + '\t' + str(last_identify_B) + '\n') # make sure don't miss the last one when parsing

f1.close()
f2.close()
