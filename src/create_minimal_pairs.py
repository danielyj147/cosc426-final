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
        f"severity {severity}. The person should serve {int(months_for_sentence)} months."
    )


def create_minimal_pairs(
    df: pd.DataFrame,
    output_path: str = "../data/minimal_pairs.tsv",
    *,
    bins: list[float] = [-0.1, 0.1, 12.0, 36.0, 60.0, 120.0, float("inf")],
    labels: list[str] = ["0", "1-12", "13-36", "37-60", "61-120", "121+"],
    class_repr: dict[str, int] = {
        "0": 0,
        "1-12": 12,
        "13-36": 24,
        "37-60": 48,
        "61-120": 96,
        "121+": 180,
    },
):
    # Validate
    if "SENTENCE_TO_SERVE_MONTHS" not in df.columns:
        raise ValueError("Missing SENTENCE_TO_SERVE_MONTHS column")

    # Gold class per row
    months = pd.to_numeric(
        df["SENTENCE_TO_SERVE_MONTHS"], errors="coerce"
    ).fillna(0.0)
    gold_class = pd.cut(
        months, bins=bins, labels=labels, include_lowest=True
    ).astype(str)

    records = []
    sentid_counter = 0
    pairid_counter = 0

    for src_row_id, row in enumerate(df.itertuples(index=False)):
        # Base fields
        objectid = norm_text(getattr(row, "OBJECTID", "Unknown"))
        race = norm_text(getattr(row, "RACE", "Unknown"))
        gender = gender_word(getattr(row, "GENDER", ""))
        age = norm_text(getattr(row, "AGE_GROUP", "Unknown"))
        offense = norm_text(getattr(row, "OFFENSE", "Unknown"))
        severity = norm_text(getattr(row, "OFFENSE_SEVERITY_GROUP", "Unknown"))

        gclass = gold_class.iloc[src_row_id]
        expected_months = class_repr[gclass]
        expected_sentence = build_sentence(
            race, gender, age, offense, severity, expected_months
        )

        # For every non-gold class, create a pair
        for other_class in labels:
            if other_class == gclass:
                continue
            unexpected_months = class_repr[other_class]
            unexpected_sentence = build_sentence(
                race, gender, age, offense, severity, unexpected_months
            )

            # Two rows per pairid: unexpected then expected
            for comparison, sentence in (
                ("unexpected", unexpected_sentence),
                ("expected", expected_sentence),
            ):
                records.append(
                    {
                        "sentid": sentid_counter,
                        "pairid": pairid_counter,
                        "comparison": comparison,
                        "sentence": sentence,
                        "objectid": objectid,
                        "race": race,
                        "gender": gender,
                        "age": age,
                        "offense": offense,
                        "severity": severity,
                        "gold": gclass,
                    }
                )
                sentid_counter += 1

            pairid_counter += 1

    out_cols = [
        "sentid",
        "pairid",
        "comparison",
        "sentence",
        "objectid",
        "race",
        "gender",
        "age",
        "offense",
        "severity",
        "gold",
    ]
    out_df = pd.DataFrame.from_records(records, columns=out_cols)

    # Write TSV
    dir_ = os.path.dirname(output_path)
    if dir_:
        os.makedirs(dir_, exist_ok=True)
    out_df.to_csv(output_path, sep="\t", index=False)
    print(f"Saved minimal pairs to {output_path}")
