import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import os

import statsmodels.formula.api as smf

# Set plot style
sns.set(rc={"figure.figsize":(10, 6)})

def load_and_prep_data():
    print("--- Loading Data ---")
    # 1. Load Data
    stock_ipos = pd.read_csv('stock_ipos_20231004.csv')
    print("Initial shape:", stock_ipos.shape)
    
    # 2. Clean Dates
    stock_ipos = stock_ipos.dropna(subset=['ipo_date']) # Ensure ipo_date is present
    stock_ipos['ipo_date'] = pd.to_datetime(stock_ipos['ipo_date'])
    stock_ipos['year'] = stock_ipos['ipo_date'].dt.year
    stock_ipos['month'] = stock_ipos['ipo_date'].dt.month
    print("Shape after date cleaning:", stock_ipos.shape)
    
    return stock_ipos

def identify_groups(stock_ipos):
    print("\n--- Identifying Groups (SPACs, S&P, Russell) ---")
    
    # 3. Identify SPACs
    try:
        stock_spacs = pd.read_excel('list_of_all_spacs.xlsx')
        spacs_tkrs = list(stock_spacs['symbol'])
        stock_ipos['spac'] = np.where(stock_ipos['symbol'].isin(spacs_tkrs), 'yes', 'no')
        print("SPACs found in IPO data:", stock_ipos['spac'].value_counts().get('yes', 0))
    except Exception as e:
        print(f"Error loading SPACs: {e}")

    # 4. Identify S&P 500
    try:
        sp500 = pd.read_excel('sp500_202308.xlsx')
        # Assuming 'Symbol' or similar column exists, need to check from previous inspection
        # Previous inspection showed: ['Symbol', 'Name', ...] for sp500? No, wait.
        # Let's assume 'Symbol' or 'Ticker' based on typical files, but I should check the inspection output again.
        # Inspection output for sp500_202308.xlsx was: ['symbol', 'name', ...] (guessed based on typical)
        # Actually, let's look at the previous turn's output for inspect_data.py
        # Output was: --- sp500_202308.xlsx --- ... [1 rows x 4 columns] ... symbol ...
        # So column is 'symbol'.
        sp500_tkrs = list(sp500['symbol'])
        stock_ipos['sp'] = np.where(stock_ipos['symbol'].isin(sp500_tkrs), 'yes', 'no')
        print("S&P 500 stocks in IPO data:", stock_ipos['sp'].value_counts().get('yes', 0))
    except Exception as e:
        print(f"Error loading S&P 500: {e}")

    # 5. Identify Russell 1000
    try:
        russ1000 = pd.read_excel('russ_1000_202308.xlsx')
        # Inspection output for russ_1000 was: ... symbol ...
        russ_tkrs = list(russ1000['symbol'])
        stock_ipos['russell'] = np.where(stock_ipos['symbol'].isin(russ_tkrs), 'yes', 'no')
        print("Russell 1000 stocks in IPO data:", stock_ipos['russell'].value_counts().get('yes', 0))
    except Exception as e:
        print(f"Error loading Russell 1000: {e}")
        
    return stock_ipos

def analyze_spacs(stock_ipos):
    print("\n--- Analyzing SPACs ---")
    # 2. (i) SPAC share over time
    ipos_spacs_count = stock_ipos.groupby(['year', 'spac'])['symbol'].count().reset_index()
    
    plt.figure()
    sns.barplot(x='year', y='symbol', hue='spac', data=ipos_spacs_count)
    plt.title("Number of IPOs by Year (SPAC vs Non-SPAC)")
    plt.ylabel("Count")
    plt.savefig("spac_counts_by_year.png")
    print("Saved plot: spac_counts_by_year.png")
    
    # 2. (ii) SPACs in S&P and Russell
    spac_only = stock_ipos[stock_ipos['spac'] == 'yes']
    print("SPACs in S&P 500:", spac_only['sp'].value_counts())
    print("SPACs in Russell 1000:", spac_only['russell'].value_counts())

def analyze_returns(stock_ipos):
    print("\n--- Analyzing Returns ---")
    # 3. Compare IPO vs Russell returns
    # Columns to describe
    cols = ['ipo_date', 'sym_day0_OTC', 'iwv_day0_OTC',
            'sym_1day_ret', 'iwv_1day_ret',
            'sym_5day_ret', 'iwv_5day_ret',
            'sym_22day_ret', 'iwv_22day_ret',
            'sym_91day_ret', 'iwv_91day_ret',
            'sym_252day_ret', 'iwv_252day_ret']
    
    desc = stock_ipos[cols].describe()
    print(desc)
    
    # Specific comparisons (Mean, Median, Std)
    # We can extract these from 'desc' or calculate explicitly for clarity
    windows = ['day0_OTC', '1day_ret', '5day_ret', '22day_ret', '91day_ret', '252day_ret']
    
    print("\nComparison (IPO vs Russell):")
    print(f"{'Window':<15} | {'IPO Mean':<10} | {'Russ Mean':<10} | {'IPO Med':<10} | {'Russ Med':<10} | {'IPO Std':<10} | {'Russ Std':<10}")
    print("-" * 95)
    
    for w in windows:
        sym_col = f"sym_{w}"
        iwv_col = f"iwv_{w}"
        
        if sym_col in stock_ipos.columns and iwv_col in stock_ipos.columns:
            print(f"{w:<15} | "
                  f"{stock_ipos[sym_col].mean():.4f}     | {stock_ipos[iwv_col].mean():.4f}     | "
                  f"{stock_ipos[sym_col].median():.4f}     | {stock_ipos[iwv_col].median():.4f}     | "
                  f"{stock_ipos[sym_col].std():.4f}     | {stock_ipos[iwv_col].std():.4f}")

def predictive_analysis(stock_ipos):
    print("\n--- Predictive Analysis ---")
    
    # 4. (i) Correlation Matrix
    sym_ret = ['sym_day0_OTC', 'sym_1day_ret', 'sym_5day_ret', 'sym_22day_ret', 
               'sym_91day_ret', 'sym_252day_ret']
    corr_matrix = stock_ipos[sym_ret].corr()
    print("\nCorrelation Matrix:")
    print(corr_matrix)
    
    # 4. (ii) Regression: 1-year ~ 1-month
    print("\nRegression (1-year ~ 1-month):")
    lm_22d = smf.ols('sym_252day_ret ~ sym_22day_ret', data=stock_ipos).fit()
    print(lm_22d.summary())
    
    # 4. (iii) Look-ahead Bias Analysis
    # (a) Scatter plot
    plt.figure()
    sns.scatterplot(x='sym_22day_ret', y='sym_252day_ret', data=stock_ipos)
    plt.title("One Year Return against First Month Return")
    plt.savefig("scatter_22_252.png")
    print("Saved plot: scatter_22_252.png")
    
    # (c) Filter outliers
    stock_ipos_filtered = stock_ipos[stock_ipos['sym_22day_ret'] < 5]
    print(f"\nFiltered data shape: {stock_ipos_filtered.shape} (Original: {stock_ipos.shape})")
    
    # (d) Regression on filtered data
    print("\nRegression on Filtered Data:")
    lm_filtered = smf.ols('sym_252day_ret ~ sym_22day_ret', data=stock_ipos_filtered).fit()
    print(lm_filtered.summary())
    
    # (f) Create 11-month return
    stock_ipos_filtered = stock_ipos_filtered.copy() # Avoid SettingWithCopyWarning
    stock_ipos_filtered['sym_22_252_ret'] = (1 + stock_ipos_filtered['sym_252day_ret']) / (1 + stock_ipos_filtered['sym_22day_ret']) - 1
    
    # (g) Predict 11-month return
    print("\nCorrelation with 11-month return:")
    print(stock_ipos_filtered[['sym_22day_ret', 'sym_252day_ret', 'sym_22_252_ret']].corr())
    
    plt.figure()
    sns.scatterplot(x='sym_22day_ret', y='sym_22_252_ret', data=stock_ipos_filtered)
    plt.title("11-Month Return against First Month Return")
    plt.savefig("scatter_22_252_11month.png")
    print("Saved plot: scatter_22_252_11month.png")
    
    return stock_ipos_filtered

def analyze_spac_vs_nonspac(stock_ipos):
    print("\n--- SPAC vs Non-SPAC Returns ---")
    
    # 5. (i) Day 0 Return
    # Flag abnormal return (example logic from PDF, though PDF logic was: < 1 'normal', else 'abnormal'?? 
    # Wait, PDF said: np.where ( stock_ipos['sym_day0_OTC'] < 1 , 'normal', 'abnormal' )
    # Usually < 0 is negative return, but maybe it means < 100%? Or maybe it's a price?
    # 'sym_day0_OTC' is likely a return. If it's a return, < 0 is loss. 
    # Let's stick to the PDF instruction: "np.where ( stock_ipos['sym_day0_OTC'] < 1 , 'normal', 'abnormal' )"
    # Wait, if return is decimal, 1 is 100%. Maybe it means outliers?
    # Let's just implement what it says or a reasonable interpretation.
    # Actually, looking at the PDF text again: "stock_ipos['day0_lvl'] = np.where ( stock_ipos['sym_day0_OTC'] < 1 , 'normal', 'abnormal' )"
    # This implies returns > 1 (100%) are abnormal.
    
    stock_ipos['day0_lvl'] = np.where(stock_ipos['sym_day0_OTC'] < 1, 'normal', 'abnormal')
    
    print("\nDay 0 Return Stats by Level and SPAC:")
    print(stock_ipos.groupby(['day0_lvl', 'spac'])['sym_day0_OTC'].agg(['mean', 'median', 'std', 'count', 'min', 'max']))
    
    # 5. (ii) Other windows
    windows = ['sym_5day_ret', 'sym_22day_ret', 'sym_91day_ret', 'sym_252day_ret']
    for w in windows:
        print(f"\n{w} Stats by SPAC:")
        print(stock_ipos.groupby('spac')[w].agg(['mean', 'median', 'std', 'count']))

def analyze_inclusion_performance(stock_ipos):
    print("\n--- Inclusion Performance (S&P/Russell) ---")
    
    # 6. Compare IPO return for included vs excluded
    # Focus on one-year returns (sym_252day_ret)
    
    print("\nS&P 500 Inclusion Performance (1-year return):")
    print(stock_ipos.groupby('sp')['sym_252day_ret'].agg(['mean', 'median', 'std', 'count']))
    
    print("\nRussell 1000 Inclusion Performance (1-year return):")
    print(stock_ipos.groupby('russell')['sym_252day_ret'].agg(['mean', 'median', 'std', 'count']))

def main():
    stock_ipos = load_and_prep_data()
    stock_ipos = identify_groups(stock_ipos)
    analyze_spacs(stock_ipos)
    analyze_returns(stock_ipos)
    stock_ipos_filtered = predictive_analysis(stock_ipos)
    analyze_spac_vs_nonspac(stock_ipos)
    analyze_inclusion_performance(stock_ipos)
    
    # Save processed data for next steps
    stock_ipos.to_csv("stock_ipos_processed.csv", index=False)
    print("\nSaved processed data to stock_ipos_processed.csv")

if __name__ == "__main__":
    main()
