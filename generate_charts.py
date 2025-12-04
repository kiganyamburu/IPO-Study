import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Set style
sns.set_style('whitegrid')
plt.rcParams['figure.figsize'] = (10, 6)

# Load and prepare data
print("Loading data...")
stock_ipos = pd.read_csv('stock_ipos_20231004.csv')
stock_ipos = stock_ipos.dropna(subset=['ipo_date'])
stock_ipos['ipo_date'] = pd.to_datetime(stock_ipos['ipo_date'])

# Identify SPACs
stock_spacs = pd.read_excel('list_of_all_spacs.xlsx')
spacs_tkrs = list(stock_spacs['symbol'])
stock_ipos['spac'] = np.where(stock_ipos['symbol'].isin(spacs_tkrs), 'yes', 'no')

# Identify S&P 500 and Russell 1000
sp500 = pd.read_excel('sp500_202308.xlsx')
sp500_tkrs = list(sp500['symbol'])
stock_ipos['sp'] = np.where(stock_ipos['symbol'].isin(sp500_tkrs), 'yes', 'no')

russ1000 = pd.read_excel('russ_1000_202308.xlsx')
russ_tkrs = list(russ1000['symbol'])
stock_ipos['russell'] = np.where(stock_ipos['symbol'].isin(russ_tkrs), 'yes', 'no')

print("Generating visualizations...")

# 1. Day 0 Returns Comparison
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

day0_means = stock_ipos.groupby('spac')['sym_day0_OTC'].mean()
axes[0].bar(['Non-SPAC', 'SPAC'], day0_means.values, color=['#2E86AB', '#A23B72'])
axes[0].set_ylabel('Mean Return')
axes[0].set_title('Day 0 Mean Returns: SPAC vs Non-SPAC')
axes[0].axhline(y=0, color='black', linestyle='--', linewidth=0.8)
axes[0].grid(axis='y', alpha=0.3)

filtered_data = stock_ipos[stock_ipos['sym_day0_OTC'] < 2]
sns.boxplot(x='spac', y='sym_day0_OTC', data=filtered_data, ax=axes[1], 
            palette=['#2E86AB', '#A23B72'])
axes[1].set_xticklabels(['Non-SPAC', 'SPAC'])
axes[1].set_ylabel('Day 0 Return')
axes[1].set_xlabel('')
axes[1].set_title('Day 0 Return Distribution (filtered < 200%)')
axes[1].axhline(y=0, color='black', linestyle='--', linewidth=0.8)

plt.tight_layout()
plt.savefig('day0_comparison.png', dpi=300, bbox_inches='tight')
print("✓ Saved: day0_comparison.png")
plt.close()

# 2. Multi-window Mean Returns
windows = ['sym_day0_OTC', 'sym_5day_ret', 'sym_22day_ret', 'sym_91day_ret', 'sym_252day_ret']
window_labels = ['Day 0', '5-day', '22-day', '91-day', '252-day']

spac_means = [stock_ipos[stock_ipos['spac'] == 'yes'][w].mean() for w in windows]
nonspac_means = [stock_ipos[stock_ipos['spac'] == 'no'][w].mean() for w in windows]

x = np.arange(len(window_labels))
width = 0.35

fig, ax = plt.subplots(figsize=(12, 6))
bars1 = ax.bar(x - width/2, nonspac_means, width, label='Non-SPAC', color='#2E86AB')
bars2 = ax.bar(x + width/2, spac_means, width, label='SPAC', color='#A23B72')

ax.set_xlabel('Time Window')
ax.set_ylabel('Mean Return')
ax.set_title('Mean Returns Across Time Windows: SPAC vs Non-SPAC')
ax.set_xticks(x)
ax.set_xticklabels(window_labels)
ax.legend()
ax.axhline(y=0, color='black', linestyle='--', linewidth=0.8)
ax.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig('multiwindow_comparison.png', dpi=300, bbox_inches='tight')
print("✓ Saved: multiwindow_comparison.png")
plt.close()

# 3. Volatility Comparison
spac_stds = [stock_ipos[stock_ipos['spac'] == 'yes'][w].std() for w in windows]
nonspac_stds = [stock_ipos[stock_ipos['spac'] == 'no'][w].std() for w in windows]

fig, ax = plt.subplots(figsize=(12, 6))
bars1 = ax.bar(x - width/2, nonspac_stds, width, label='Non-SPAC', color='#2E86AB')
bars2 = ax.bar(x + width/2, spac_stds, width, label='SPAC', color='#A23B72')

ax.set_xlabel('Time Window')
ax.set_ylabel('Standard Deviation')
ax.set_title('Return Volatility Across Time Windows: SPAC vs Non-SPAC')
ax.set_xticks(x)
ax.set_xticklabels(window_labels)
ax.legend()
ax.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig('volatility_comparison.png', dpi=300, bbox_inches='tight')
print("✓ Saved: volatility_comparison.png")
plt.close()

# 4. S&P 500 Performance
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

sp_stats = stock_ipos.groupby('sp')['sym_252day_ret'].agg(['mean', 'median'])
x_pos = np.arange(2)
width = 0.35

axes[0].bar(x_pos - width/2, sp_stats['mean'].values, width, label='Mean', color='#F18F01')
axes[0].bar(x_pos + width/2, sp_stats['median'].values, width, label='Median', color='#C73E1D')
axes[0].set_ylabel('1-Year Return')
axes[0].set_title('S&P 500 Inclusion: 1-Year Return Performance')
axes[0].set_xticks(x_pos)
axes[0].set_xticklabels(['Not Included', 'Included'])
axes[0].legend()
axes[0].axhline(y=0, color='black', linestyle='--', linewidth=0.8)
axes[0].grid(axis='y', alpha=0.3)

filtered_sp = stock_ipos[stock_ipos['sym_252day_ret'] < 3]
sns.boxplot(x='sp', y='sym_252day_ret', data=filtered_sp, ax=axes[1],
            palette=['#2E86AB', '#F18F01'])
axes[1].set_xticklabels(['Not Included', 'Included'])
axes[1].set_ylabel('1-Year Return')
axes[1].set_xlabel('')
axes[1].set_title('1-Year Return Distribution (filtered < 300%)')
axes[1].axhline(y=0, color='black', linestyle='--', linewidth=0.8)

plt.tight_layout()
plt.savefig('sp500_performance.png', dpi=300, bbox_inches='tight')
print("✓ Saved: sp500_performance.png")
plt.close()

# 5. Russell 1000 Performance
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

russell_stats = stock_ipos.groupby('russell')['sym_252day_ret'].agg(['mean', 'median'])

axes[0].bar(x_pos - width/2, russell_stats['mean'].values, width, label='Mean', color='#06A77D')
axes[0].bar(x_pos + width/2, russell_stats['median'].values, width, label='Median', color='#005F73')
axes[0].set_ylabel('1-Year Return')
axes[0].set_title('Russell 1000 Inclusion: 1-Year Return Performance')
axes[0].set_xticks(x_pos)
axes[0].set_xticklabels(['Not Included', 'Included'])
axes[0].legend()
axes[0].axhline(y=0, color='black', linestyle='--', linewidth=0.8)
axes[0].grid(axis='y', alpha=0.3)

filtered_russell = stock_ipos[stock_ipos['sym_252day_ret'] < 3]
sns.boxplot(x='russell', y='sym_252day_ret', data=filtered_russell, ax=axes[1],
            palette=['#2E86AB', '#06A77D'])
axes[1].set_xticklabels(['Not Included', 'Included'])
axes[1].set_ylabel('1-Year Return')
axes[1].set_xlabel('')
axes[1].set_title('1-Year Return Distribution (filtered < 300%)')
axes[1].axhline(y=0, color='black', linestyle='--', linewidth=0.8)

plt.tight_layout()
plt.savefig('russell1000_performance.png', dpi=300, bbox_inches='tight')
print("✓ Saved: russell1000_performance.png")
plt.close()

# 6. Index Comparison
fig, ax = plt.subplots(figsize=(10, 6))

categories = ['Not Included', 'S&P 500', 'Russell 1000']
means = [
    stock_ipos[(stock_ipos['sp'] == 'no') & (stock_ipos['russell'] == 'no')]['sym_252day_ret'].mean(),
    stock_ipos[stock_ipos['sp'] == 'yes']['sym_252day_ret'].mean(),
    stock_ipos[stock_ipos['russell'] == 'yes']['sym_252day_ret'].mean()
]

bars = ax.bar(categories, means, color=['#2E86AB', '#F18F01', '#06A77D'])
ax.set_ylabel('Mean 1-Year Return')
ax.set_title('Index Inclusion Impact on 1-Year Returns')
ax.axhline(y=0, color='black', linestyle='--', linewidth=0.8)
ax.grid(axis='y', alpha=0.3)

for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height,
            f'{height:.2%}', ha='center', va='bottom')

plt.tight_layout()
plt.savefig('index_comparison.png', dpi=300, bbox_inches='tight')
print("✓ Saved: index_comparison.png")
plt.close()

print("\n✓ All visualizations generated successfully!")
