# Horizontal_gene_transfer_project
Three python scripts are wrote for inferring HGT events. 

Parse_blast_result.py can be used to parse blastp results based on HGT AI, HGT Index, as well as HGT Identity. 

HGT AI = log(best_hit_Evalue_in_A_database + 1e-180) - log(best_hit_Evalue_in_B_database + 1e-180);

HGT Index = best_hit_Score_in_A_database - best_hit_Score_in_B_database; 

HGT Identity = best_hit_Identity_in_A_database - best_hit_Identity_in_B_database

Extract_fasta_1.py can be used for extracting top 50 to 100 hit sequences from potential donate organisms.

Extract_fasta_2.py can be used for extracting all hit sequences from close organisms.

-------------------------------------------------------------------------------------------------------------------------------------

Please let’s assume have two fasta files of different protein sequences database with name Prepare_A.fa and Prepare_B.fa respectively. The Prepare_A.fa is the background proteins and from close organisms with the research species, and Prepare_B is from the potential donate organisms.  

1 For clearly distinguish two different protein sequences, using following commands to change the name per sequences and then combine it:

sed 's/>/>A|/g' Prepare_A.fa > A.fa

sed 's/>/>B|/g' Prepare_B.fa > B.fa

cat A.fa B.fa > HGT_identify_database.fa

2 Now use local blast to produce blastp result: 

makeblastdb -in HGT_identify_database.fa -dbtype prot -out HGT_identify_database

blastp -db HGT_identify_database -query fasta_file -outfmt 6 -out HGT_identify_blastp_result.txt -evalue 1e-5

3 Using first python script to get HGT AI, HGT Index, as well as HGT Identity per query proteins:

python Parse_blast_result.py HGT_identify_blastp_result.txt HGT_identify_blastp_result_parse_result.txt


4 Using second python script to extract protein sequences of donate organisms (B.fa; B database) from 50 to 100:

python Extract_fasta_1.py B.fa HGT_identify_blastp_result.txt ID_file

Note: ID_file contains all candidate ids, one per line; like:

ID1

ID2

……

5 Using third python script to extract all similar sequences of close(background) organisms (A.fa; A database):

python Extract_fasta_2.py A.fa Blastp_result

Note: Blastp_result file only includes query ids you want to extract and their blastp hits; like:

ID1 hit1

ID1 hit2

……

ID2 hit1

ID2 hit2

……

6 Combining two files into one file used to do alignment and build phylogenic tree:

for i in ID1 ID2 …; do cat $i.1.fa $i.2.fa > $i.c.fa; done

7 The following commands are used in my project to do alignment, delete unconserved regions and construct phylogenic tree:

for i in *.c.fa; do mafft -auto $i > $i.ali.fa; done

for i in *.ali.fa; do trimAI –in $i –out $i.del.fa –automated1; done

for i in *.del.fa; do raxmlHPC –f d –m PROTCATAUTO –p 123456 –s $i –n $i.tre; done

Actually you could select other methods and programs you like to build trees, such as MrBayes.
