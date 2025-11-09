# COSC426 Final Project

> "Always code as if the person maintaining your code will be a violent psychopath who knows where you live."
> — John F. Woods, 1991

## Project Ideas

1. AI Judge: Can AI accurately deliver sentences without bias?
   1. Factors: gender, race, criminal history, crime category
   2. Datasets
      * [“Sentencing” tagged datasets — Bureau of Justice Statistics / Data.gov](https://opendata.dc.gov/api/download/v1/items/f92f4556f26b4737a040fb996eaefca3/csv?layers=40)
      * [Interactive Data Analyzer — United States Sentencing Commission](https://www.ussc.gov/research/interactive-data-analyzer)
      * [Commission Datafiles — USSC (Criminal History of Sentenced Individuals)](https://www.ussc.gov/research/datafiles/commission-datafiles)
      * [Data Collections Search — BJS](https://bjs.ojp.gov/data-collections/search)
      * [National Corrections Reporting Program (NCRP) — BJS](https://bjs.ojp.gov/data-collection/national-corrections-reporting-program-ncrp)
      * [Monitoring of Federal Criminal Sentences Series — Inter‑university Consortium for Political and Social Research (ICPSR)](https://www.icpsr.umich.edu/web/ICPSR/series/83)

## Useful Links

* [Final project guidelines](https://github.com/grushaprasad/cosc426/blob/main/Final.md)
* [Final project ideas drive folder](https://drive.google.com/drive/folders/1p5AcgjCE0tW6U1ZDN9drd0lNvblybIJG?usp=drive_link)
  * [Leo](https://docs.google.com/document/d/1LDaLPa9x91dwVEzw2E7FRhyDq0Z00k9eCd1bkGcXFLw/edit?usp=sharing)
  * [Ernest](https://docs.google.com/document/d/1ty6Isl06Nyz1xLo2TmdapZ73X9VOvSIC_nXssAXq5FE/edit?usp=sharing)
  * [Dan](https://docs.google.com/document/d/1OQwR_mrWLYyhGlXbdcltnK5IAQQpknUwkkok7i4w3Q4/edit?usp=sharing)
* [VS Code on HPC](https://turing-login.colgate.edu/pun/sys/dashboard/batch_connect/sys/vscode/session_contexts/new)
* [NLPScholar](https://github.com/forrestdavis/NLPScholar)

## Quick Start

1. Install [uv](https://docs.astral.sh/uv/getting-started/installation/) (a fast, all-in-one Python package and project management tool)

2. Install dependencies

    ```bash
    uv sync
    ```

3. Activate the venv

    ```bash
    source .venv/bin/activate
    ```

4. Install recommended VS Code extensions

    1. For compiling LaTeX: [LaTeX Workshop](https://marketplace.visualstudio.com/items?itemName=James-Yu.latex-workshop)

## Data Generation

You can generate the required data simply by running [**main.ipynb**](/notebooks/main.ipynb).
If you prefer to do it manually, follow the steps below:

1. Download the publicly available [felony sentences dataset](https://opendata.dc.gov/api/download/v1/items/f92f4556f26b4737a040fb996eaefca3/csv?layers=40).
2. Load the file into a DataFrame.
3. Pass the DataFrame as input to the `create_minimal_pairs` function from `src/create_minimal_pairs.py`.

## Project Structure

```text
.
├── README.md
├── assets // images
├── configs // NLPScholar Configs
├── data
│   └── offense.csv // Offenses used for minimalpairs generation
├── notebooks // Jupyter Notebooks
├── predictions // NLPScholar Predictions
├── pyproject.toml
├── report // Final Paper
├── results // NLPScholar Results
├── src // Python Scripts
└── uv.lock
```

## Contributors

## Citations

## TODO

1. Data Generation (11/9)
    * [ ] Race (Leo)
    * [ ] Gender (Ernest)
    * [ ] Age Group (Dan)
2. NLP Scholar Config (11/9)
    * [ ] Race (Leo)
    * [ ] Gender (Ernest)
    * [ ] Age Group (Dan)
3. Generate Predictions and Results (11/9)
    * [ ] Race (Leo)
    * [ ] Gender (Ernest)
    * [ ] Age Group (Dan)
