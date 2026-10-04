# M5 raw data

Download the official dataset from the Kaggle competition page:

**Dataset:** [M5 Forecasting - Accuracy](https://www.kaggle.com/competitions/m5-forecasting-accuracy/data)

Kaggle requires contributors to sign in, accept the competition rules, and configure an API token. Follow `setup.md`, then run this command from the repository root:

```bash
python scripts/download_data.py
```

Place the downloaded files in this directory without changing their filenames. The analysis expects these files:

- `calendar.csv`
- `sales_train_validation.csv`
- `sales_train_evaluation.csv`
- `sample_submission.csv`
- `sell_prices.csv`

The helper verifies the downloaded files before analysis. The dataset files are intentionally excluded from Git because of their size and Kaggle's competition terms.
