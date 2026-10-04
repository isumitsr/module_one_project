# Local project setup

This guide explains how to prepare a local environment for the M5 safety-stock project.

## 1. Requirements

- Python 3.11
- Git
- At least 5 GB of free disk space for the environment, raw data, and later processed datasets
- Access to the M5 dataset

## 2. Create and activate a virtual environment

From the repository root, run:

```bash
python3.11 -m venv .venv
source .venv/bin/activate
```

On Windows PowerShell, activate the environment with:

```powershell
.venv\Scripts\Activate.ps1
```

## 3. Install the dependencies

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Register the environment as a Jupyter kernel:

```bash
python -m ipykernel install --user --name m5-safety-stock --display-name "Python (M5 Safety Stock)"
```

## 4. Authenticate with Kaggle

The M5 files are hosted as Kaggle competition data. Before the first download:

1. Sign in to [Kaggle](https://www.kaggle.com/).
2. Open the [M5 Forecasting - Accuracy data page](https://www.kaggle.com/competitions/m5-forecasting-accuracy/data).
3. Join the competition or accept its data rules when Kaggle prompts you.
4. Open [Kaggle API settings](https://www.kaggle.com/settings/api) and generate an API token.
5. Authenticate locally by running:

```bash
python -c "import kagglehub; kagglehub.login()"
```

Do not add an API token or Kaggle credential file to this repository.

## 5. Download the raw data

Run the project download helper from the repository root:

```bash
python scripts/download_data.py
```

The script downloads and verifies these files in `data/raw/`:

- `calendar.csv`
- `sales_train_evaluation.csv`
- `sales_train_validation.csv`
- `sample_submission.csv`
- `sell_prices.csv`

The script skips the download when all five local files already have the expected checksums. Raw data are excluded from Git and must not be committed.

## 6. Start JupyterLab

Run this command from the repository root:

```bash
jupyter lab
```

Open the notebooks in their numeric order. Select the **Python (M5 Safety Stock)** kernel if Jupyter does not choose it automatically.

## 7. Verify the setup

Open `notebooks/01_data_audit_and_eda.ipynb`, restart the kernel, and run all cells. A successful setup should:

- download the M5 files from Kaggle when they are missing;
- find and verify all five raw CSV files;
- load the files without an exception;
- display the audit tables; and
- complete with no failed checks caused by missing or corrupted files.

The notebook uses project-relative paths. It should therefore be run from this repository rather than from an unrelated working directory.
