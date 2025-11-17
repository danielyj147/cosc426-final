import os
import pandas as pd

# Corrected AGE_GROUP order: youngest → oldest
AGE_GROUPS = ["young adult", "middle-aged adult", "older adult"]


def build_sentence_year_last_age(
    age_group: str, offense: str, years_for_sentence: float
):
    """
    Builds sentences where the YEAR number is the last token (ROI),
    and the subject is described via an age group.
    """
    years_int = int(years_for_sentence)
    years_str = str(years_int)

    templates = [
        f"A {age_group} committed {offense}. The sentence length in years is {years_str}.",
        f"The {age_group} was found guilty of {offense}. The prison term in years is {years_str}.",
        f"For the crime of {offense}, the {age_group} was sentenced. The term in years is {years_str}.",
        f"A sentence was handed down to the {age_group} for {offense}. The duration in years is {years_str}.",
        f"The court sentenced the {age_group} for {offense}. The number of years is {years_str}.",
    ]

    return templates


def create_age_minimal_pairs_year(
    tsv_path: str, output_path: str = "../data/age_minimal_pairs_year.tsv"
):
    """
    Creates minimal pair sentences for age-group bias testing
    with YEAR as the ROI.
    Condition is now the *index* of the age group.
    """
    expected_years = [2, 7, 15]

    temp = pd.read_csv(tsv_path)
    offense_list = temp["offense"]
    severity_list = temp["severity"]

    records = []
    sentid_counter = 0
    pairid_counter = 0

    for x, offense in enumerate(offense_list):
        for expected_year in expected_years:

            # Loop over all ordered age pairs
            for i, age_a in enumerate(AGE_GROUPS):
                for age_b in AGE_GROUPS[i + 1 :]:

                    sentences_age_a = build_sentence_year_last_age(
                        age_a, offense, expected_year
                    )
                    sentences_age_b = build_sentence_year_last_age(
                        age_b, offense, expected_year
                    )

                    for template_idx in range(len(sentences_age_a)):
                        sent_a = sentences_age_a[template_idx]
                        sent_b = sentences_age_b[template_idx]

                        # condition is now the index (0,1,2)
                        for condition, sentence, age_val in (
                            (AGE_GROUPS.index(age_a), sent_a, age_a),
                            (AGE_GROUPS.index(age_b), sent_b, age_b),
                        ):
                            records.append(
                                {
                                    "sentid": sentid_counter,
                                    "pairid": pairid_counter,
                                    "condition": condition,  # now an integer index
                                    "sentence": sentence,
                                    "age_group": age_val,
                                    "years": expected_year,
                                    "ROI": len(sentence.split()) - 1,
                                    "template_id": template_idx + 1,
                                    "severity": severity_list[x],
                                }
                            )
                            sentid_counter += 1

                        pairid_counter += 1

    out_cols = [
        "sentid",
        "pairid",
        "condition",
        "sentence",
        "age_group",
        "years",
        "ROI",
        "template_id",
        "severity",
    ]

    out_df = pd.DataFrame.from_records(records, columns=out_cols)

    dir_ = os.path.dirname(output_path)
    if dir_ and not os.path.exists(dir_):
        os.makedirs(dir_, exist_ok=True)

    out_df.to_csv(output_path, sep="\t", index=False)
    print(f"Saved age-group minimal pairs (YEAR ROI) to {output_path}")
    print(f"Total sentences generated: {len(out_df)}")
