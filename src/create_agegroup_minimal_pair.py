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
    where YEAR is the ROI (last token).
    Always ensures the younger group comes first in the pair.
    """
    expected_years = [0, 2, 7, 15, 100]

    temp = pd.read_csv(tsv_path)
    offense_list = temp["offense"]
    # type_list = temp["type"]
    severity_list = temp["severity"]

    records = []
    sentid_counter = 0
    pairid_counter = 0

    for x, offense in enumerate(offense_list):
        for expected_year in expected_years:
            # Loop over all ordered pairs (younger first)
            for i, age_a in enumerate(AGE_GROUPS):
                for age_b in AGE_GROUPS[i + 1 :]:
                    expected_sentence_list = build_sentence_year_last_age(
                        age_a, offense, expected_year
                    )
                    unexpected_sentence_list = build_sentence_year_last_age(
                        age_b, offense, expected_year
                    )

                    for template_idx in range(len(expected_sentence_list)):
                        expected_sent = expected_sentence_list[template_idx]
                        unexpected_sent = unexpected_sentence_list[template_idx]

                        for comparison, sentence, age_val in (
                            ("expected", expected_sent, age_a),
                            ("unexpected", unexpected_sent, age_b),
                        ):
                            records.append(
                                {
                                    "sentid": sentid_counter,
                                    "pairid": pairid_counter,
                                    "comparison": comparison,
                                    "sentence": sentence,
                                    "age_pair": f"{age_a} vs {age_b}",
                                    "age_group": age_val,
                                    "years": expected_year,
                                    "ROI": len(sentence.split()) - 1,
                                    "template_id": template_idx + 1,
                                    # "type": type_list[x],
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
        "age_pair",
        "age_group",
        "years",
        "ROI",
        "template_id",
        # "type",
        "severity",
    ]

    out_df = pd.DataFrame.from_records(records, columns=out_cols)

    dir_ = os.path.dirname(output_path)
    if dir_ and not os.path.exists(dir_):
        os.makedirs(dir_, exist_ok=True)

    out_df.to_csv(output_path, sep="\t", index=False)
    print(f"Saved age-group minimal pairs (YEAR ROI) to {output_path}")
    print(f"Total sentences generated: {len(out_df)}")
