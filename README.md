# Horizontal_gene_transfer_project
Three python scripts are wrote for inferring HGT event. 

Parse_blast_result.py will be used to parse blastp result based on HGT AI, HGT Index, as well as HGT Identity. HGT AI = best_hit_Evalue_in_A_database + 1e-180) - log(best_hit_Evalue_in_B_database + 1e-180); HGT Index = best_hit_Score_in_A_database - best_hit_Score_in_B_database; HGT Identity = best_hit_Identity_in_A_database - best_hit_Identity_in_B_database

Extract_fasta_1.py will be used for extracting top 50 to 100 hit sequences from potential donate organisms.

Extract_fasta_2.py will be used for extracting all hit sequences from close organisms.

