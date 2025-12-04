import pandas as pd
import numpy as np

# Load the processed data (or load fresh and prepare)
print("=" * 80)
print("QUESTION 5: SPACs vs Non-SPACs Return Analysis")
print("=" * 80)

# Load data
stock_ipos = pd.read_csv('stock_ipos_20231004.csv')
stock_ipos = stock_ipos.dropna(subset=['ipo_date'])
stock_ipos['ipo_date'] = pd.to_datetime(stock_ipos['ipo_date'])

# Identify SPACs
try:
    stock_spacs = pd.read_excel('list_of_all_spacs.xlsx')
    spacs_tkrs = list(stock_spacs['symbol'])
    stock_ipos['spac'] = np.where(stock_ipos['symbol'].isin(spacs_tkrs), 'yes', 'no')
except Exception as e:
    print(f"Error loading SPACs: {e}")

print("\n5(i) Day 0 Return Analysis:")
print("-" * 80)

# Flag abnormal returns (returns >= 1 or 100% are considered abnormal)
stock_ipos['day0_lvl'] = np.where(stock_ipos['sym_day0_OTC'] < 1, 'normal', 'abnormal')

# Summarize day0 return by SPACs
day0_summary = stock_ipos.groupby(['day0_lvl', 'spac'])['sym_day0_OTC'].agg(['mean', 'median', 'std', 'count', 'min', 'max'])
print("\nDay 0 Return Statistics by Level and SPAC Status:")
print(day0_summary)

print("\n" + "=" * 80)
print("COMMENTS ON SPAC vs NON-SPAC DAY 0 RETURNS:")
print("=" * 80)

# Calculate overall stats for comparison
spac_day0 = stock_ipos.groupby('spac')['sym_day0_OTC'].agg(['mean', 'median', 'std', 'count'])
print("\nOverall Day 0 Return by SPAC Status:")
print(spac_day0)

print("\n5(ii) Analysis for Other Return Windows:")
print("-" * 80)

windows = ['sym_5day_ret', 'sym_22day_ret', 'sym_91day_ret', 'sym_252day_ret']
window_names = ['5-day', '22-day (1-month)', '91-day (3-month)', '252-day (1-year)']

for w, name in zip(windows, window_names):
    print(f"\n{name} Return Statistics by SPAC Status:")
    print("-" * 60)
    summary = stock_ipos.groupby('spac')[w].agg(['mean', 'median', 'std', 'count', 'min', 'max'])
    print(summary)

print("\n" + "=" * 80)
print("QUESTION 6: IPO Return Performance - Index Inclusion Analysis")
print("=" * 80)

# Identify S&P 500
try:
    sp500 = pd.read_excel('sp500_202308.xlsx')
    sp500_tkrs = list(sp500['symbol'])
    stock_ipos['sp'] = np.where(stock_ipos['symbol'].isin(sp500_tkrs), 'yes', 'no')
except Exception as e:
    print(f"Error loading S&P 500: {e}")

# Identify Russell 1000
try:
    russ1000 = pd.read_excel('russ_1000_202308.xlsx')
    russ_tkrs = list(russ1000['symbol'])
    stock_ipos['russell'] = np.where(stock_ipos['symbol'].isin(russ_tkrs), 'yes', 'no')
except Exception as e:
    print(f"Error loading Russell 1000: {e}")

print("\n6. S&P 500 Inclusion Performance (1-year return):")
print("-" * 80)
sp_performance = stock_ipos.groupby('sp')['sym_252day_ret'].agg(['mean', 'median', 'std', 'count', 'min', 'max'])
print(sp_performance)

print("\n6(i) Russell 1000 Inclusion Performance (1-year return):")
print("-" * 80)
russell_performance = stock_ipos.groupby('russell')['sym_252day_ret'].agg(['mean', 'median', 'std', 'count', 'min', 'max'])
print(russell_performance)

print("\n" + "=" * 80)
print("ANALYSIS COMPLETE")
print("=" * 80)
