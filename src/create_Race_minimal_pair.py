import os
from typing import Dict, List
import pandas as pd

def norm_text(x, default: str = "Unknown") -> str:
    return default if pd.isna(x) else str(x)

def gender_word(g: str) -> str:
    g = str(g).strip().upper()
    return {"M": "male", "F": "female"}.get(g, "non-binary")

def build_sentence(
    race: str,
    gender: str,
    age: str,
    offense: str,
    severity: str,
    months_for_sentence: float,
) -> str:
    return (
        f"The person is a {race.lower()} {gender} aged {age}, convicted of {offense}, "
        f"severity {severity}. The person should serve {int(months_for_sentence)} years."
    )

def create_race_minimal_pairs(df: pd.DataFrame, output_path: str = "../data/race_minimal_pairs.tsv"):

    expected_years = [0,1,5,10]
    max_iter = 10
    iter = 0

    records = []
    sentid_counter = 0
    pairid_counter = 0


    for src_row_id, row in enumerate(df.itertuples(index=False)):
        # Base fields
        gender = gender_word(getattr(row, "GENDER", ""))
        age = norm_text(getattr(row, "AGE_GROUP", "Unknown"))
        offense = norm_text(getattr(row, "OFFENSE", "Unknown"))
        severity = norm_text(getattr(row, "OFFENSE_SEVERITY_GROUP", "Unknown"))

        for i in range(len(expected_years)): # Process should be the same for every year
            expected_year = expected_years[i]

            # First iteration test White vs Black (White expected Black unexpected)

            expected_sentence1 = build_sentence("White", gender, age, offense, severity, expected_year)
            unexpected_sentence1 = build_sentence("Black", gender, age, offense, severity, expected_year)

            # Two rows per pairid: unexpected then expected
            for comparison, sentence in (
                ("expected", expected_sentence1),
                ("unexpected", unexpected_sentence1),
            ):
                records.append(
                    {
                        "sentid": sentid_counter,
                        "pairid": pairid_counter,
                        "comparison": comparison,
                        "sentence": sentence,
                        "race": sentence.split()[4],
                        "years": expected_years[i]
                    }
                )
                sentid_counter += 1

            pairid_counter += 1
            
            # Second iteration test White vs Hispanic (White expected Hispanic unexpected)

            expected_sentence2 = build_sentence("White", gender, age, offense, severity, expected_year)
            unexpected_sentence2 = build_sentence("Hispanic", gender, age, offense, severity, expected_year)

            for comparison, sentence in (
                ("expected", expected_sentence2),
                ("unexpected", unexpected_sentence2),

            ):
                records.append(
                    {
                        "sentid": sentid_counter,
                        "pairid": pairid_counter,
                        "comparison": comparison,
                        "sentence": sentence,
                        "race": sentence.split()[4],
                        "years": expected_years[i]
                    }
                )
                sentid_counter += 1

            pairid_counter += 1

            

            # Third iteration test Black vs Hispanic (Black expected Hispanic unexpected)

            expected_sentence3 = build_sentence("Black", gender, age, offense, severity, expected_year)
            unexpected_sentence3 = build_sentence("Hispanic", gender, age, offense, severity, expected_year)

        
            for comparison, sentence in (
                ("expected", expected_sentence3),
                ("unexpected", unexpected_sentence3),

            ):
                records.append(
                    {
                        "sentid": sentid_counter,
                        "pairid": pairid_counter,
                        "comparison": comparison,
                        "sentence": sentence,
                        "race": sentence.split()[4],
                        "years": expected_years[i]
                    }
                )
                sentid_counter += 1

            pairid_counter += 1
        iter +=1
        if iter > max_iter:
            break


          

        
    out_cols = [
        "sentid",
        "pairid",
        "comparison",
        "sentence",
        "race",
        "years"
    ]
    out_df = pd.DataFrame.from_records(records, columns=out_cols)

    # Write TSV
    dir_ = os.path.dirname(output_path)
    if dir_:
        os.makedirs(dir_, exist_ok=True)
    out_df.to_csv(output_path, sep="\t", index=False)
    print(f"Saved minimal pairs to {output_path}")

