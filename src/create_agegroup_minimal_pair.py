import os
import pandas as pd

# data/origin.tsv `AGE_GROUP` column's unique values
AGE_GROUPS = ["22-30", "61-70", "31-40", "18-21", "41-50", "15-17", "51-60", "71+"]


def build_sentence_age_last(age_group: str, offense: str, years_for_sentence: float):
    """
    Builds sentences where the AGE GROUP is the last token (ROI).
    Example ROI: '22-30', '71+'.
    """
    years_int = int(years_for_sentence)
    years_str = str(years_int)

    templates = [
        f"The person who committed {offense} and got {years_str} years is {age_group}.",
        f"The defendant was found guilty of {offense} with a {years_str}-year sentence and is {age_group}.",
        f"The individual sentenced to {years_str} years for {offense} is {age_group}.",
        f"For the crime of {offense}, the defendant given {years_str} years is {age_group}.",
        f"The person convicted of {offense} and handed {years_str} years is {age_group}.",
    ]

    return templates


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
        f"A person aged {age_group} committed {offense}. The sentence length was {years_str}.",
        f"The defendant aged {age_group} was found guilty of {offense}. The sentence received was {years_str}.",
        f"For the crime of {offense}, the individual aged {age_group} was sentenced. The term is {years_str}.",
        f"A sentence was handed down to the person aged {age_group} for {offense}. The duration is {years_str}.",
        f"The court sentenced the individual aged {age_group} for {offense}. The number of years is {years_str}.",
    ]

    return templates


def create_age_minimal_pairs_age(
    tsv_path: str, output_path: str = "../data/age_minimal_pairs_age.tsv"
):
    """
    Creates minimal pair sentences for age-group bias testing
    where AGE GROUP is the ROI (last token).
    All unordered pairs of AGE_GROUPS are generated.
    """
    expected_years = [0, 1, 5, 10]

    temp = pd.read_csv(tsv_path)
    offense_list = temp["offense"]

    records = []
    sentid_counter = 0
    pairid_counter = 0

    for offense in offense_list:
        for expected_year in expected_years:
            for i, age_a in enumerate(AGE_GROUPS):
                for age_b in AGE_GROUPS[i + 1 :]:
                    expected_sentence_list = build_sentence_age_last(
                        age_a, offense, expected_year
                    )
                    unexpected_sentence_list = build_sentence_age_last(
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
    ]

    out_df = pd.DataFrame.from_records(records, columns=out_cols)

    dir_ = os.path.dirname(output_path)
    if dir_ and not os.path.exists(dir_):
        os.makedirs(dir_, exist_ok=True)

    out_df.to_csv(output_path, sep="\t", index=False)
    print(f"Saved age-group minimal pairs (AGE ROI) to {output_path}")
    print(f"Total sentences generated: {len(out_df)}")


def create_age_minimal_pairs_year(
    tsv_path: str, output_path: str = "../data/age_minimal_pairs_year.tsv"
):
    """
    Creates minimal pair sentences for age-group bias testing
    where YEAR is the ROI (last token).
    All unordered pairs of AGE_GROUPS are generated.
    """
    expected_years = [0, 1, 5, 10]

    temp = pd.read_csv(tsv_path)
    offense_list = temp["offense"]
    type_list = temp["type"]
    severity_list = temp["severity"]

    records = []
    sentid_counter = 0
    pairid_counter = 0
    x=-1
    for offense in offense_list:
        x+=1
        for expected_year in expected_years:
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
                                    "type": type_list[x],
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
        "type",
        "severity",
    ]

    out_df = pd.DataFrame.from_records(records, columns=out_cols)

    dir_ = os.path.dirname(output_path)
    if dir_ and not os.path.exists(dir_):
        os.makedirs(dir_, exist_ok=True)

    out_df.to_csv(output_path, sep="\t", index=False)
    print(f"Saved age-group minimal pairs (YEAR ROI) to {output_path}")
    print(f"Total sentences generated: {len(out_df)}")
