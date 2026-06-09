# 📊 ML Experiment Tracker

Automatically trains scikit-learn models and logs experiment results to a Google Sheet — no manual copy-pasting, no lost runs.

## What It Does

Runs a configurable set of Logistic Regression experiments on the Iris dataset, validates each result with Pydantic, and appends a clean row to a Google Sheet for every run.

Each logged row includes:
- Timestamp
- Dataset name
- Max iterations
- Solver used
- Accuracy score

## Stack

| Layer | Tool |
|---|---|
| Model training | scikit-learn |
| Schema validation | Pydantic |
| Cloud logging | gspread + Google Sheets API |

## Setup

### 1. Install dependencies

```bash
pip install gspread pydantic scikit-learn google-auth
```

### 2. Google Sheets credentials

- Create a [Google Cloud service account](https://console.cloud.google.com/iam-admin/serviceaccounts)
- Download the JSON key and save it as `service_account.json` in the project root
- Share your Google Sheet with the service account email (Editor access)

### 3. Create the Sheet

Create a Google Sheet named exactly:
```
ML Experiment Tracker
```
The script auto-creates the header row on first run.

### 4. Run

```bash
python main.py
```

## Output

```
🤖 Loading Iris Dataset and preparing training partitions...
✅ Logged Run: Solver=saga  | Accuracy=73.33%
✅ Logged Run: Solver=saga  | Accuracy=96.67%
✅ Logged Run: Solver=lbfgs | Accuracy=100.00%
```

## Adding Experiments

Edit the `experiments` list in `log_experiment_to_sheets()`:

```python
experiments = [
    {"max_iter": 10,  "solver": "saga"},
    {"max_iter": 50,  "solver": "saga"},
    {"max_iter": 100, "solver": "lbfgs"},
    # add more configs here
]
```

Any new solver or iteration count supported by `sklearn.linear_model.LogisticRegression` works out of the box.

## Project Structure

```
.
├── main.py                # Entry point
├── service_account.json   # GCP credentials (not committed)
└── README.md
```

> ⚠️ Never commit `service_account.json`. Add it to `.gitignore`.
