# Imperial Marriage Pact

A backend matching pipeline that turns survey responses into ranked preferences and final pairings.

This project was built for a campus-wide matching initiative. Responses were collected with Google Forms, exported to Excel, and processed with Python. There was no custom frontend: the engineering focus was the data pipeline, compatibility model, and matching workflow.

## Project flow

```mermaid
flowchart LR
    A[Google Form responses] --> B[Excel export]
    B --> C[Clean and validate responses]
    C --> D[Build participant feature vectors]
    D --> E[Score and rank compatible candidates]
    E --> F[Generate pairings]
    F --> G[Export matched and unmatched results]
```

## How it works

1. **Collect responses:** Participants answer demographic, preference, and 49 compatibility questions through Google Forms.
2. **Prepare the data:** pandas loads the spreadsheet, normalizes column names, and constructs one participant record per response.
3. **Model compatibility:** Survey answers become numerical vectors. Euclidean distance measures similarity, while mutually incompatible gender, age, or race preferences receive distance penalties.
4. **Create preference rankings:** Every participant receives an ordered list of candidates based on the resulting distance.
5. **Generate pairings:** A preference-based matching heuristic, inspired by stable matching, works through those rankings to assign pairs.
6. **Select and export a run:** The pipeline repeats the randomized assignment process and keeps the run with the most high-compatibility matches. It writes separate matched and unmatched sheets to Excel.

## What I built

- End-to-end processing from survey export to deliverable results
- Participant data model and compatibility constraints
- Pairwise scoring and preference-list construction
- Matching and repeated-run selection logic
- Excel reporting for matched and unmatched participants

## Technical decisions

- **Python, pandas, and NumPy** keep the batch workflow simple and auditable.
- **Vector distance** provides an interpretable baseline for comparing survey responses.
- **Soft penalties** allow preference constraints to affect rankings without making the search brittle.
- **Repeated randomized runs** reduce sensitivity to the initial participant ordering.

## Repository structure

```text
files/
├── marriagepact2.py   # fuller implementation and reporting workflow
└── marriagepact3.py   # streamlined matching pipeline
```

## Running the analysis

Use a local spreadsheet with the column names expected by the script. Participant data is sensitive and should not be committed to the repository.

```bash
python -m venv .venv
source .venv/bin/activate
pip install pandas numpy xlsxwriter openpyxl
python files/marriagepact3.py
```

Before running it on a new form, update the input filename and participant count in the script.

## Limitations and next steps

- The current system is a batch analysis pipeline, not a hosted application.
- The matching routine is inspired by stable matching but is not presented as a formally verified Gale–Shapley implementation.
- Preference penalties and the 80% selection threshold are hand-designed and would benefit from evaluation against participant feedback.
- A future version could add schema validation, automated tests, configuration files, and an administrator-facing results dashboard.

## Context

This is an independent student implementation inspired by the broader Marriage Pact concept. It is not affiliated with the official Marriage Pact organization.

A student publication covered the campus initiative: [Imperial College's Marriage Pact](https://felixonline.co.uk/articles/imperial-marriage-pact/).