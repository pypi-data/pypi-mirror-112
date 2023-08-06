dustmasker -in nucl_data.fas -infmt fasta -parse_seqids -outfmt maskinfo_asn1_bin -out mask_nucl_dustmasker.asnb
windowmasker -in nucl_data.fas -infmt fasta -mk_counts -parse_seqids -out tmp 
windowmasker -in nucl_data.fas -infmt fasta -ustat tmp -outfmt maskinfo_asn1_bin -parse_seqids -out mask_nucl_windowmasker.asnb
rm tmp
