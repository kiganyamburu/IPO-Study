# IPO Analysis Project

This project analyzes stock IPOs from 2012 to 2023, focusing on SPACs, return performance, and index inclusion (S&P 500 and Russell 1000).

## Project Structure

- **`project1_analysis.py`**: The main Python script that performs the data cleaning, analysis, and plot generation.
- **`project1_report.md`**: A detailed report containing the answers to the project questions and analysis results.
- **`extract_pdf.py`**: A utility script used to extract text from the original project PDF.
- **Data Files**:
    - `stock_ipos_20231004.csv`: Main IPO data.
    - `list_of_all_spacs.xlsx`: List of SPAC companies.
    - `sp500_202308.xlsx`: S&P 500 constituents.
    - `russ_1000_202308.xlsx`: Russell 1000 constituents.

## Setup and Usage

1.  **Install Dependencies**:
    Ensure you have Python installed, then install the required libraries:
    ```bash
    pip install pandas numpy seaborn matplotlib statsmodels openpyxl pypdf
    ```

2.  **Run the Analysis**:
    Execute the main analysis script:
    ```bash
    python project1_analysis.py
    ```
    This will:
    - Process the data.
    - Print statistical summaries to the console.
    - Generate plots (e.g., `spac_counts_by_year.png`, `scatter_22_252.png`).
    - Save a processed dataset to `stock_ipos_processed.csv`.

## Analysis Overview

The analysis covers:
1.  **Data Preparation**: Cleaning dates and identifying SPACs/Index members.
2.  **SPAC Analysis**: Examining the trend of SPAC IPOs over time.
3.  **Return Analysis**: Comparing IPO returns against the Russell 1000 index.
4.  **Predictive Analysis**: Investigating if early returns (Day 0, Month 1) predict long-term (1-year) performance.
5.  **Inclusion Performance**: Analyzing how S&P 500 and Russell 1000 inclusion correlates with returns.

For detailed findings, please refer to `project1_report.md`.
