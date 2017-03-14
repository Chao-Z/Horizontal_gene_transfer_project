# the first script for hgt: based on formula to parse blast result to get potential id
# used command: python Parse_blast_result.py blastp_result_file parse_out_result_file
# the blastp_result_file should be sort with query id !!!

import sys
import math
from math import log


f1 = open(sys.argv[1],'r')
f2 = open(sys.argv[2],'w')

f2.write('Gene_ID' + '\t' + 'HGT_evalue' + '\t' + 'Algae_evalue' + '\t' + 'Non_plant_evalue' + '\t' + 'HGT_score' + '\t' + 'Algae_score' + '\t' + 'Non_plant_score' + '\t' + 'HGT_identify' + '\t' + 'Algae_identify' + '\t' + 'Non_plant_identify' + '\n')

List1 = []
last_Evalue_P,last_Evalue_N = 1,1
last_score_P, last_score_N = 0,0
last_identify_P, last_identify_N = 0,0
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
            last_Evalue_P = Evalue
            last_score_P = Score
            last_identify_P = Identify
        if ID2[0] != 'A':
            last_Evalue_N = Evalue
            last_score_N = Score
            last_identify_N = Identify
    else:
        if ID1 in List1:
            if ID2[0] == 'A':
                last_Evalue_P = min(Evalue,last_Evalue_P)
                last_score_P = max(Score,last_score_P)
                last_identify_P = max(Identify,last_identify_P)
            if ID2[0] != 'A':
                last_Evalue_N = min(Evalue,last_Evalue_N)
                last_score_N = max(Score,last_score_N)
                last_identify_N = max(Identify,last_identify_N)
        if ID1 not in List1:
            HGT_AI = math.log(last_Evalue_P + 1e-180) - math.log(last_Evalue_N + 1e-180)
            HGT_Index = last_score_N - last_score_P
            HGT_Identify = last_identify_N - last_identify_P
            f2.write(last_ID1 + '\t' + str(HGT_AI) + '\t' + str(last_Evalue_P) + '\t' + str(last_Evalue_N) + '\t' + str(HGT_Index) + '\t' + str(last_score_P) + '\t' + str(last_score_N) + '\t' + str(HGT_Identify) + '\t' + str(last_identify_P) + '\t' + str(last_identify_N) + '\n')
            List1.append(ID1)
            if ID2[0] == 'A':
                last_Evalue_P,last_Evalue_N = Evalue,1
                last_score_P,last_score_N = Score,0
                last_identify_P,last_identify_N = Identify,0
            if ID2[0] != 'A':
                last_Evalue_N,last_Evalue_P = Evalue,1
                last_score_N,last_score_P = Score,0
                last_identify_N,last_identify_P = Identify,0
    last_ID1 = ID1
if sply != '': f2.write(last_ID1 + '\t' + str(math.log(last_Evalue_P + 1e-180) - math.log(last_Evalue_N + 1e-180)) + '\t' + str(last_Evalue_P) + '\t' + str(last_Evalue_N) + '\t' + str(last_score_N - last_score_P) + '\t' + str(last_score_P) + '\t' + str(last_score_N) + '\t' + str(last_identify_N - last_identify_P) + '\t' + str(last_identify_P) + '\t' + str(last_identify_N) + '\n') # make sure don't miss the last one when parsing
f1.close()
f2.close()