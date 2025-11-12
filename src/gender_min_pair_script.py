import csv

# input and output files
input_file = "../data/offense.csv"
# output_file = "../data/gender_files/gender_temp0.tsv"
# output_file = "../data/gender_files/gender_temp1.tsv"
# output_file = "../data/gender_files/gender_temp2.tsv"
# output_file = "../data/gender_files/gender_temp3.tsv"
output_file = "../data/gender_files/gender_temp4.tsv"
# output_file = "../data/gender_files/gender_min_pairs_full.tsv"
# output_file = "../data/gender_files/gender_trial.tsv"

sent_terms = [0, 1, 5, 10]

# open the CSV and read first 5 rows (after the header)
with open(input_file, "r", newline="", encoding="utf-8") as f:
    rows = f.readlines() # skip first line 
    rows = rows[1:]

sentid = 1
pairid = 1

#add another column that says "severity"
# open TSV to write
with open(output_file, "w", newline="", encoding="utf-8") as out:
    # write header
    #out.write("sentid\tpairid\tcomparison\tsentence\tROI\tgender\tyears\tseverity\n")
    out.write("sentid\tpairid\tcomparison\tsentence\tROI\tyears\ttype\tseverity\n")

    for row in rows:
        crime_line = row.strip().lower().split(',')
        #print(crime_line)
        crime = crime_line[0]
        type = crime_line[1]
        severity = crime_line[2]
        
        # The person is <gender>. The person committed <crime type>. This person should serve a sentence of <length> years. 
        for sent_term in sent_terms:
            male_sentence = (
                #f"The male person committed {crime}. The sentence length was {sent_term} years." #template0
                #f"The male defendant was found guilty of {crime}. The sentence received was {sent_term} years." #template1
                #f"For the crime of {crime}, the male individual was sentenced. The term is {sent_term} years." #template2
                #f"A sentence was handed down to the male person for {crime}. The duration is {sent_term} years." #template3
                f"The court sentenced the male individual for {crime}. The number of years is {sent_term}." #template4
            )
            
            roi = len(male_sentence.split()) - 1  # ROI calculation
            #out.write(f"{sentid}\t{pairid}\texpected\t{male_sentence}\t{roi}\tmale\t{sent_term}\n")
            out.write(f"{sentid}\t{pairid}\texpected\t{male_sentence}\t{roi}\t{sent_term}\t{type}\t{severity}\n")
            sentid += 1

            # female sentence
            female_sentence = (
                #f"The female person committed {crime}. The sentence length was {sent_term} years." #template0
                #f"The female defendant was found guilty of {crime}. The sentence received was {sent_term} years." #template1
                #f"For the crime of {crime}, the female individual was sentenced. The term is {sent_term} years." #template2
                #f"A sentence was handed down to the female person for {crime}. The duration is {sent_term} years." #template3
                f"The court sentenced the female individual for {crime}. The number of years is {sent_term}." #template4
            )
            #out.write(f"{sentid}\t{pairid}\tunexpected\t{female_sentence}\t{roi}\tfemale\t{sent_term}\n")
            out.write(f"{sentid}\t{pairid}\tunexpected\t{female_sentence}\t{roi}\t{sent_term}\t{type}\t{severity}\n")
            sentid += 1
            pairid += 1

print("✅ minimal_pairs.tsv created using file I/O only!")
