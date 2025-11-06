import csv

# input and output files
input_file = "../data/offense.csv"
output_file = "../data/gender_min_pairs.tsv"
sent_terms = [0, 1, 5, 10]

# open the CSV and read first 5 rows (after the header)
with open(input_file, "r", newline="", encoding="utf-8") as f:
    rows = f.readlines()[:5] # read first 5 data rows  

sentid = 1
pairid = 1

# open TSV to write
with open(output_file, "w", newline="", encoding="utf-8") as out:
    # write header
    out.write("sentid\tpairid\tsentence\tcomparison\tROI\tgender\tyears\n")

    for row in rows:
        crime = row.strip().lower()
        
        # The person is <gender>. The person committed <crime type>. This person should serve a sentence of <length> years. 
        for sent_term in sent_terms:
            male_sentence = (
                f"The person is male. The person committed {crime}. This person should serve a sentence of {sent_term} years."
            )
            
            roi = len(male_sentence.split()) - 2  # ROI calculation
            out.write(f"{sentid}\t{pairid}\t{male_sentence}\texpected\t{roi}\tmale\t{sent_term}\n")
            sentid += 1

            # female sentence
            female_sentence = (
                f"The person is female. The person committed {crime}. This person should serve a sentence of {sent_term} years."   
            )
            out.write(f"{sentid}\t{pairid}\t{female_sentence}\tunexpected\t{roi}\tfemale\t{sent_term}\n")
            sentid += 1
            pairid += 1

print("✅ minimal_pairs.tsv created using file I/O only!")
