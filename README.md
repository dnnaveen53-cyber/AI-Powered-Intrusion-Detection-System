# AI-Powered Intrusion Detection System (AI-IDS)

An end-to-end machine learning-based Intrusion Detection System that classifies network traffic into five categories using the NSL-KDD dataset.

## Project Overview

This project uses supervised machine learning to detect and classify network intrusions.

**Traffic categories:**
- Normal
- DoS (Denial of Service)
- Probe
- R2L (Remote to Local)
- U2R (User to Root)

## Dataset

This project exclusively uses the NSL-KDD dataset.

Dataset source:
https://github.com/Jehuty4949/NSL_KDD

The repository is a public GitHub mirror, not an official CIC repository.

Dataset files:
- KDDTrain+.txt
- KDDTest+.txt
- Field Names.csv
- Attack Types.csv

## Technologies Used

| Component | Technology |
|---|---|
| Programming | Python |
| Machine Learning | Scikit-learn |
| Model | Random Forest |
| Data Processing | Pandas, NumPy |
| API | FastAPI |
| Dashboard | Streamlit |
| Database | SQLite |
| Testing | Pytest |

## Project Structure

```text
AI-Powered-IDS/
├── api/
├── artifacts/
├── dashboard/
├── data/
│   ├── processed/
│   └── raw/
├── scripts/
├── src/
├── tests/
├── .gitignore
├── README.md
└── requirements.txt