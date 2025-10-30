# COSC426 Final Project

> "Always code as if the person maintaining your code will be a violent psychopath who knows where you live."
> — John F. Woods, 1991

## Project Ideas

1. AI Judge: Can AI accurately deliver sentences without bias?
   1. Factors: gender, race, criminal history, crime category
   2. Datasets
      * [Interactive Data Analyzer — United States Sentencing Commission](https://www.ussc.gov/research/interactive-data-analyzer)
      * [Commission Datafiles — USSC (Criminal History of Sentenced Individuals)](https://www.ussc.gov/research/datafiles/commission-datafiles)
      * [“Sentencing” tagged datasets — Bureau of Justice Statistics / Data.gov](https://catalog.data.gov/dataset/?tags=sentencing)
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

## Project Structure

```text
.
├── README.md
├── assets # images & figures
├── configs # NLPScholar configs
├── data
├── notebooks
│   └── main.ipynb
├── pyproject.toml
├── report # paper
│   ├── acl2023.sty
│   ├── acl_natbib.bst
│   ├── custom.bib
│   ├── main.pdf
│   └── main.tex
└── uv.lock
```

## Contributors

## Citations
