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

    Each pairid corresponds to THREE sentences:
    one for each age group (young, middle-aged, older),
    with the same offense, year, and template, differing only by age.
    - 'condition' is the index of the age group in AGE_GROUPS.
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
            # Precompute templates for each age group for this offense/year
            age_templates = []
            for age_idx, age_group in enumerate(AGE_GROUPS):
                templates = build_sentence_year_last_age(
                    age_group, offense, expected_year
                )
                age_templates.append((age_idx, age_group, templates))

            # Assume all age groups have the same number of templates
            num_templates = len(age_templates[0][2])

            # For each template, create a pair containing all 3 age groups
            for template_idx in range(num_templates):
                for age_idx, age_group, templates in age_templates:
                    sentence = templates[template_idx]

                    records.append(
                        {
                            "sentid": sentid_counter,
                            "pairid": pairid_counter,
                            "condition": age_idx,  # 0, 1, 2
                            "sentence": sentence,
                            "age_group": age_group,  # "young adult", etc.
                            "years": expected_year,
                            "ROI": len(sentence.split()) - 1,
                            "template_id": template_idx + 1,
                            "severity": severity_list[x],
                        }
                    )
                    sentid_counter += 1

                # after all 3 age groups for this template/offense/year
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
