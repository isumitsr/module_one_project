# From Forecasts to Stock Decisions

### Project Title: Probabilistic safety-stock design across Walmart stores using the M5 dataset.

This project is part of the AAI 500 Probability and Statistics for AI course in the Master of Science (M.S) in Applied Artificial Intelligence program at the University of San Diego.

**Project status:** Planned

## Project objective

Retailers must decide how much inventory to hold when future demand is uncertain. Too little inventory can lead to stockouts and missed sales, while too much inventory ties up cash and increases holding risk. A fixed buffer does not respond to the different demand patterns of individual products and stores.

This project investigates whether probabilistic demand forecasts can support better safety-stock decisions than a simple forecasting method combined with a fixed inventory buffer. We will compare forecast accuracy, forecast uncertainty, simulated stockouts, service levels, and inventory held under clearly stated replenishment assumptions.

Our central research question is:

> Under stated replenishment assumptions, can probabilistic forecasts reduce simulated stockouts or inventory held compared with a simple forecasting and fixed-buffer approach?

## Installation

### 1. Clone the repository

```bash
git clone <repository-url>
cd <repository-folder>
```

### 2. Create the Python environment

```bash
python3.11 -m venv .venv
source .venv/bin/activate       # macOS/Linux
# .venv\Scripts\Activate.ps1   # Windows PowerShell

python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 3. Authenticate with Kaggle

The M5 files are subject to Kaggle's competition rules. Before the first download:

1. Sign in to [Kaggle](https://www.kaggle.com/).
2. Open the [M5 Forecasting - Accuracy data page](https://www.kaggle.com/competitions/m5-forecasting-accuracy/data) and accept the competition rules.
3. Generate an API token from [Kaggle API settings](https://www.kaggle.com/settings/api).
4. Authenticate on your computer:

```bash
python -c "import kagglehub; kagglehub.login()"
```

Never commit a Kaggle token or credential file to this repository.

### 4. Download and verify the data

Run the project download helper from the repository root:

```bash
python scripts/download_data.py
```

The script downloads the five official competition files into `data/raw/`, verifies their checksums, and skips files that are already valid. The raw CSV files are excluded from Git because of their size and Kaggle's competition terms.

Complete this step before running the analysis notebooks.

### 5. Start the project notebooks

Start JupyterLab from the repository root:

```bash
jupyter lab
```

Open the notebooks in numeric order, beginning with:

```text
notebooks/01_data_audit_and_eda.ipynb
```

The first notebook also checks the local data and calls the download helper automatically if a required file is missing or invalid. Once the data audit passes, continue developing the remaining notebooks and project sections in their documented order.

See [`setup.md`](setup.md) for the complete environment, authentication, data-download, and verification instructions.

## Team members and contributors

- Sumit Chaurasia
- Lala Ram
- AAI 500 Group 1

## Methods used

- Exploratory data analysis of demand, seasonality, intermittency, and variability
- Time-series forecasting
- Probability distributions and predictive uncertainty
- [to be updated, as we go along]

## Technologies

- Python
- pandas and NumPy for data preparation
- Matplotlib/ Seaborn for visualization
- SciPy for probability distributions and statistical calculations
- statsmodels for statistical forecasting
- scikit-learn and/or a quantile-regression library for the machine-learning comparison
- Jupyter Notebook/ VSCode Notebooks
- Git and GitHub for version control and collaboration
- Trello for Project Management

## Project description

### Dataset

The project uses the public M5 Walmart sales dataset. The competition data contain daily unit sales for 3,049 products sold across 10 stores in California, Texas, and Wisconsin. This produces 30,490 product-store time series. The data also include calendar events and weekly selling prices.

| File | Purpose | Main contents |
|---|---|---|
| `sales_train_validation.csv` | Historical demand | Product and store identifiers plus daily sales from `d_1` through `d_1913` |
| `sales_train_evaluation.csv` | Extended evaluation data | Historical sales through `d_1941`, including the competition evaluation period |
| `calendar.csv` | Date and event information | Dates, weekdays, months, years, events, and SNAP indicators |
| `sell_prices.csv` | Price information | Store, item, selling week, and selling price |

The raw sales file is in wide format. We will reshape the daily columns into a long time-series table and merge the calendar and price information using the appropriate date and store-item keys.

### Series selection

The full M5 dataset is large, so the analysis will use a documented sample of product-store series. The sample will represent different stores, categories, and demand patterns, including relatively stable, seasonal, intermittent, and highly variable series. The selection rule and final series list will be recorded in the repository so that the analysis can be reproduced.

### Planned analysis workflow

1. Audit the raw files, data types, missing values, duplicate keys, and date coverage.
2. Convert the sales data from wide to long format.
3. Merge calendar events and selling prices without using future information.
4. Explore trends, weekly seasonality, event effects, zero-sales days, and demand variability.
5. Create chronological training, validation, and test periods.
6. [to be updated as we go along]

### Inventory-policy comparison

The probabilistic policy will use an upper forecast quantile for demand during the assumed lead time. In simplified form:

```text
Order-up-to level = forecast demand during lead time + uncertainty buffer
Safety stock = order-up-to level - expected demand during lead time
```

The comparison policy will use a simple forecast and a fixed buffer. Lead times, review frequency, starting inventory, replenishment rules, and any holding or stockout-cost assumptions will be stated before the simulation is run.

### Research questions and hypotheses

**Research question 1:** Do probabilistic forecasts produce better simulated service outcomes than a fixed-buffer policy?

**Hypothesis 1:** At comparable average inventory levels, a probabilistic policy will produce a lower simulated stockout rate or higher simulated service level than the fixed-buffer policy.

**Research question 2:** How does the target service level affect inventory held and stockouts?

**Hypothesis 2:** Increasing the target service level will reduce simulated stockouts but require more inventory.

**Research question 3:** Does better average forecast accuracy always produce better inventory decisions?

**Hypothesis 3:** The model with the best point-forecast metric will not necessarily produce the best balance between service and inventory because the quality of the uncertainty estimate also matters.

### Evaluation metrics

Forecast performance will be evaluated with metrics such as MAE, RMSE, WAPE, and quantile or pinball loss where appropriate. Predictive uncertainty will be assessed using interval coverage and interval width. Inventory policies will be compared using simulated stockout rate, service level or fill rate, average inventory held, and the tradeoff between service and inventory.

### Scope and limitations

The M5 data record observed sales, not complete inventory positions or unmet customer demand. The dataset also does not provide the supplier lead times, replenishment rules, or inventory costs required to reproduce Walmart's actual decisions. Therefore, lead times, starting inventory, ordering rules, and cost assumptions will be explicit modeling assumptions. Stockouts, service levels, and inventory outcomes reported in this project are simulation results, not measured Walmart outcomes.

The results will apply only to the selected product-store series and the assumptions used in the simulation. They should not be interpreted as a recommendation for Walmart's actual inventory system without additional operational data.

## Repository structure

```text
.
├── README.md
├── setup.md
├── requirements.txt
├── docs/
│   ├── README.md
│   └── project_structure.md
├── data/
│   ├── raw/              # Downloaded M5 files, not committed to GitHub
│   └── processed/        # Generated analysis-ready data, if needed
├── scripts/
│   └── download_data.py  # Kaggle download and checksum verification
├── notebooks/
│   ├── 01_data_audit_and_eda.ipynb
│   ├── 02_forecasting.ipynb
│   ├── 03_uncertainty_and_safety_stock.ipynb
│   └── 04_inventory_simulation.ipynb
├── src/
│   ├── data_prep.py
│   ├── forecasting.py
│   ├── inventory_simulation.py
│   └── evaluation.py
├── reports/
│   └── figures/
└── LICENSE
```

## License and data use

The project code will use the license specified in the repository's `LICENSE` file. The M5 files remain subject to the Kaggle competition rules and are not redistributed through this repository. Users should download the data directly from Kaggle and follow its terms of use.

## Acknowledgments

We thank the University of San Diego faculty and Prof. Haisav Chokshi for guidance in the AAI 500 Probability and Statistics for AI course. We also acknowledge the M5 competition organizers and the authors of the M5 competition paper for making the retail forecasting data and documentation available.

### Reference

Makridakis, S., Spiliotis, E., & Assimakopoulos, V. (2022). The M5 competition: Background, organization, and implementation. *International Journal of Forecasting, 38*(4), 1325–1336. https://doi.org/10.1016/j.ijforecast.2021.07.007
