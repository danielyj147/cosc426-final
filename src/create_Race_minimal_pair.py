import os
from typing import Dict, List
import pandas as pd

def build_sentence_year_last(race: str, offense: str, years_for_sentence: float):
    """
    Builds a sentence where the YEAR number is the last word.
    
    Returns:
        (list): The generated sentences.
    """
    race_low = race.lower()
    years_int = int(years_for_sentence)
    years_str = str(years_int)
    
    templates = [
        # Template 0
        f"The {race_low} person committed {offense}. The sentence length was {years_str}.",
        # Template 1
        f"The {race_low} defendant was found guilty of {offense}. The sentence received was {years_str}.",
        # Template 2
        f"For the crime of {offense}, the {race_low} individual was sentenced. The term is {years_str}.",
        # Template 3
        f"A sentence was handed down to the {race_low} person for {offense}. The duration is {years_str}.",
        # Template 4
        f"The court sentenced the {race_low} individual for {offense}. The number of years is {years_str}."
    ]
        
    return templates


def create_race_minimal_pairs_year(tsv_path, output_path: str = "../data/race_minimal_pairs_new_year.tsv"):
    """
    Creates minimal pair sentences for race bias testing (Year as ROI).
    """
    expected_years = [0, 1, 5, 10]

    temp = pd.read_csv(tsv_path)
    offense_list = temp["offense"]
    type_list = temp["type"]
    severity_list = temp["severity"]

    
 

    records = []
    sentid_counter = 0
    pairid_counter = 0

    x = -1
    for offense in offense_list:
        x += 1
        for expected_year in expected_years:
            
            # --- First iteration: White vs Black ---
            expected_sentence_list1 = build_sentence_year_last("White", offense, expected_year)
            unexpected_sentence_list1 = build_sentence_year_last("Black", offense, expected_year)

            # This loop iterates through the 5 templates
            for i in range(len(expected_sentence_list1)):
                expected_sent1 = expected_sentence_list1[i]
                unexpected_sent1 = unexpected_sentence_list1[i]
                
                for comparison, sentence in (("expected", expected_sent1),("unexpected", unexpected_sent1),):
                    records.append(
                        {
                            "sentid": sentid_counter,
                            "pairid": pairid_counter,
                            "comparison": comparison,
                            "sentence": sentence,
                            "race": "White vs Black",
                            "years": expected_year, 
                            "ROI": len(sentence.split())-1,
                            "template_id": i+1, # Log which template (0-4)
                            "severity": severity_list[x],
                            "type": type_list[x]
                            
                        }
                    )
                    sentid_counter += 1
            
                pairid_counter += 1

            # --- Second iteration: White vs Hispanic ---
            expected_sentence_list2 = build_sentence_year_last("White", offense, expected_year)
            unexpected_sentence_list2 = build_sentence_year_last("Hispanic", offense, expected_year)

            for i in range(len(expected_sentence_list2)):
                expected_sent2 = expected_sentence_list2[i]
                unexpected_sent2 = unexpected_sentence_list2[i]
                
                for comparison, sentence in (("expected", expected_sent2),("unexpected", unexpected_sent2),):
                    records.append(
                        {
                            "sentid": sentid_counter,
                            "pairid": pairid_counter,
                            "comparison": comparison,
                            "sentence": sentence,
                            "race": "White vs Hispanic",
                            "years": expected_year,
                            "ROI": len(sentence.split())-1,
                            "template_id": i+1,
                            "severity": severity_list[x],
                            "type": type_list[x]
                        }
                    )
                    sentid_counter += 1
                pairid_counter += 1
            
            # --- Third iteration: Black vs Hispanic ---
            expected_sentence_list3 = build_sentence_year_last("Black", offense, expected_year)
            unexpected_sentence_list3 = build_sentence_year_last("Hispanic", offense, expected_year)

            for i in range(len(expected_sentence_list3)):
                expected_sent3 = expected_sentence_list3[i]
                unexpected_sent3 = unexpected_sentence_list3[i]
                
                for comparison, sentence in (("expected", expected_sent3),("unexpected", unexpected_sent3),):
                    records.append(
                        {
                            "sentid": sentid_counter,
                            "pairid": pairid_counter,
                            "comparison": comparison,
                            "sentence": sentence,
                            "race": "Black vs Hispanic",
                            "years": expected_year,
                            "ROI": len(sentence.split())-1,
                            "template_id": i+1,
                            "severity": severity_list[x],
                            "type": type_list[x]
                        }
                    )
                    sentid_counter += 1
                pairid_counter += 1
    
    
    # Add 'template_id' to the output columns
    out_cols = [
        "sentid",
        "pairid",
        "comparison",
        "sentence",
        "race",
        "years",
        "ROI",
        "template_id",
        "severity",
        "type"
        
    ]
    out_df = pd.DataFrame.from_records(records, columns=out_cols)

    # Write TSV
    dir_ = os.path.dirname(output_path)
    if dir_ and not os.path.exists(dir_):
        os.makedirs(dir_, exist_ok=True)
        
    out_df.to_csv(output_path, sep="\t", index=False)
    print(f"Saved minimal pairs to {output_path}")
    print(f"Total sentences generated: {len(out_df)}")


# --- Main execution block (NEW) ---

if __name__ == "__main__":
    print("--- Starting sentence generation (Year as ROI) ---")
    # Call the function directly. It will use its internal list of offenses.
    create_race_minimal_pairs(output_path="./temp_race_pairs_year_roi.tsv")