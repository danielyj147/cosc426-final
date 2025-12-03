import os
from typing import List
import pandas as pd


def build_sentence_year_last(gender: str, offense: str, years_for_sentence: float):
    """
    Builds a sentence where the YEAR number is the last word.

    Args:
        gender (str): 'Male' or 'Female'.
        offense (str): The crime/offense.
        years_for_sentence (float): Sentence duration in years.

    Returns:
        list: A list of sentences following five templates.
    """
    gender_low = gender.lower()
    years_int = int(years_for_sentence)
    years_str = str(years_int)

    templates = [
        f"The {gender_low} person committed {offense}. The sentence length in years is {years_str}.",
        f"The {gender_low} defendant was found guilty of {offense}. The prison term in years is {years_str}.",
        f"For the crime of {offense}, the {gender_low} individual was sentenced. The term in years is {years_str}.",
        f"A sentence was handed down to the {gender_low} person for {offense}. The duration in years is {years_str}.",
        f"The court sentenced the {gender_low} individual for {offense}. The number of years is {years_str}.",
    ]

    return templates


def create_gender_minimal_pairs_year(
    tsv_path, output_path: str = "../data/new_gender_minimal_pairs_year.tsv"
):
    """
    Creates minimal pair sentences for gender bias testing (Year as ROI).
    Compares Male vs Female sentences using consistent templates.
    """
    #expected_years = [2,7,15]
    expected_years = [0,2,7,15,100]

    # Read TSV
    temp = pd.read_csv(tsv_path)
    offense_list = temp["offense"]
    severity_list = temp["severity"]

    records = []
    sentid_counter = 0
    pairid_counter = 0

    # Generate sentences
    for x, offense in enumerate(offense_list):
        for expected_year in expected_years:

            # Male vs Female pair
            expected_sentence_list = build_sentence_year_last(
                "Female", offense, expected_year
            )
            unexpected_sentence_list = build_sentence_year_last(
                "Male", offense, expected_year
            )

            for i in range(len(expected_sentence_list)):
                expected_sent = expected_sentence_list[i]
                unexpected_sent = unexpected_sentence_list[i]

                for comparison, sentence in (
                    ("expected", expected_sent),
                    ("unexpected", unexpected_sent),
                ):
                        
                    records.append(
                        {
                            "sentid": sentid_counter,
                            "pairid": pairid_counter,
                            "comparison": comparison,
                            "sentence": sentence,
                            "gender": "Female vs Male",
                            "years": expected_year,
                            "ROI": len(sentence.split()) - 1,
                            "severity": severity_list[x],
                        }
                    )
                    sentid_counter += 1
                pairid_counter += 1

    out_cols = [
        "sentid",
        "pairid",
        "comparison",
        "sentence",
        "gender",
        "years",
        "ROI",
        "severity",
    ]
    out_df = pd.DataFrame.from_records(records, columns=out_cols)

    dir_ = os.path.dirname(output_path)
    if dir_ and not os.path.exists(dir_):
        os.makedirs(dir_, exist_ok=True)

    # Write to TSV
    out_df.to_csv(output_path, sep="\t", index=False)
    print(f"Saved gender minimal pairs to {output_path}")
    print(f"Total sentences generated: {len(out_df)}")