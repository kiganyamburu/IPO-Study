# IPO Analysis Report: Questions 5 & 6
## SPAC vs Non-SPAC Returns and Index Inclusion Performance

**Author:** Ryan Nduta  
**Date:** December 4, 2025  
**Course:** IPO Analysis  
**Dataset:** 3,681 IPOs (stock_ipos_20231004.csv)

---

## Executive Summary

This report analyzes IPO return performance across two key dimensions:
1. **SPAC vs Non-SPAC comparison** across multiple time horizons
2. **Index inclusion impact** (S&P 500 and Russell 1000) on 1-year returns

**Key Findings:**
- SPACs underperform Non-SPACs but show lower volatility
- Index inclusion strongly predicts superior performance (~8-9x higher returns)
- Only 1.4% of IPOs achieve S&P 500 inclusion, 3.9% achieve Russell 1000

---

## 1. Introduction

### 1.1 Research Questions

**Question 5:** Do SPAC returns differ from other IPO returns?
- 5(i): Day 0 return analysis with abnormal return flagging
- 5(ii): Multi-window return comparison (5, 22, 91, 252 days)

**Question 6:** How does index inclusion affect IPO performance?
- S&P 500 inclusion impact on 1-year returns
- Russell 1000 inclusion impact on 1-year returns

### 1.2 Dataset Overview

- **Total IPOs:** 3,681
- **SPACs:** 251 (6.8%)
- **Non-SPACs:** 3,430 (93.2%)
- **S&P 500 Included:** 51 (1.4%)
- **Russell 1000 Included:** 143 (3.9%)

---

## 2. Methodology

### 2.1 Data Preparation

```python
# Load and prepare data
stock_ipos = pd.read_csv('stock_ipos_20231004.csv')
stock_ipos = stock_ipos.dropna(subset=['ipo_date'])
stock_ipos['ipo_date'] = pd.to_datetime(stock_ipos['ipo_date'])
```

### 2.2 SPAC Identification

```python
# Identify SPACs
stock_spacs = pd.read_excel('list_of_all_spacs.xlsx')
spacs_tkrs = list(stock_spacs['symbol'])
stock_ipos['spac'] = np.where(
    stock_ipos['symbol'].isin(spacs_tkrs), 'yes', 'no'
)
```

### 2.3 Index Inclusion Identification

```python
# Identify S&P 500
sp500 = pd.read_excel('sp500_202308.xlsx')
sp500_tkrs = list(sp500['symbol'])
stock_ipos['sp'] = np.where(
    stock_ipos['symbol'].isin(sp500_tkrs), 'yes', 'no'
)

# Identify Russell 1000
russ1000 = pd.read_excel('russ_1000_202308.xlsx')
russ_tkrs = list(russ1000['symbol'])
stock_ipos['russell'] = np.where(
    stock_ipos['symbol'].isin(russ_tkrs), 'yes', 'no'
)
```

---

## 3. Question 5: SPAC vs Non-SPAC Performance

### 3.1 Question 5(i): Day 0 Return Analysis

#### Methodology

```python
# Flag abnormal returns (>= 100%)
stock_ipos['day0_lvl'] = np.where(
    stock_ipos['sym_day0_OTC'] < 1, 
    'normal', 
    'abnormal'
)

# Summary statistics
day0_summary = stock_ipos.groupby(['day0_lvl', 'spac'])[
    'sym_day0_OTC'
].agg(['mean', 'median', 'std', 'count', 'min', 'max'])
```

#### Results

**Table 1: Day 0 Return Statistics by Level and SPAC Status**

| Category | Mean | Median | Std Dev | Count | Min | Max |
|----------|------|--------|---------|-------|-----|-----|
| **Abnormal, Non-SPAC** | 2.918 | 2.245 | 3.010 | 30 | 1.017 | 17.750 |
| **Normal, Non-SPAC** | -0.005 | 0.000 | 0.127 | 3,400 | -0.851 | 0.974 |
| **Normal, SPAC** | -0.009 | 0.000 | 0.070 | 251 | -0.550 | 0.429 |

**Table 2: Overall Day 0 Return by SPAC Status**

| Category | Mean | Median | Std Dev | Count |
|----------|------|--------|---------|-------|
| **Non-SPAC** | 0.021 (2.1%) | 0.000 | 0.408 | 3,430 |
| **SPAC** | -0.009 (-0.9%) | 0.000 | 0.070 | 251 |

#### Key Findings

1. **SPACs have lower and negative mean Day 0 returns**
   - SPACs: -0.88% vs Non-SPACs: +2.09%
   - Difference of 2.97 percentage points

2. **SPACs show significantly lower volatility**
   - SPAC std dev: 0.070 vs Non-SPAC: 0.408
   - SPACs are ~5.8x less volatile

3. **Abnormal returns (≥100%) only occur in Non-SPACs**
   - 30 cases with mean return of 292%
   - Range: 102% to 1,775%

4. **Both groups have median returns of 0%**
   - Suggests many IPOs trade at offer price on Day 0
   - Distribution is right-skewed for Non-SPACs

5. **SPACs have narrower return range**
   - SPACs: -55% to +43%
   - Non-SPACs: -85% to +1,775%

---

### 3.2 Question 5(ii): Multi-Window Return Analysis

#### Methodology

```python
# Analyze returns across different windows
windows = ['sym_5day_ret', 'sym_22day_ret', 
           'sym_91day_ret', 'sym_252day_ret']

for window in windows:
    summary = stock_ipos.groupby('spac')[window].agg([
        'mean', 'median', 'std', 'count'
    ])
```

#### Results

**Table 3: Returns and Volatility Across Time Windows**

| Window | Non-SPAC Mean | SPAC Mean | Non-SPAC Std | SPAC Std | Non-SPAC Median | SPAC Median |
|--------|---------------|-----------|--------------|----------|-----------------|-------------|
| **Day 0** | 2.09% | -0.88% | 0.408 | 0.070 | 0.00% | 0.00% |
| **5-day** | 3.40% | 2.13% | 1.252 | 0.276 | 0.00% | 0.10% |
| **22-day** | 4.72% | 3.03% | 1.344 | 0.377 | 0.22% | 0.31% |
| **91-day** | 6.07% | 3.02% | 2.007 | 0.477 | 0.10% | 0.92% |
| **252-day** | 4.26% | 1.31% | 2.968 | 0.157 | -0.70% | 3.73% |

#### Key Findings

1. **Non-SPACs consistently outperform across all horizons**
   - Day 0: +2.97 pp advantage
   - 5-day: +1.27 pp advantage
   - 22-day: +1.69 pp advantage
   - 91-day: +3.05 pp advantage
   - 252-day: +2.95 pp advantage

2. **SPACs demonstrate consistently lower volatility**
   - All time windows show 3-19x lower standard deviation
   - Most dramatic at 252-day: 2.968 vs 0.157

3. **Performance patterns diverge over time**
   - Non-SPACs peak at 91-day (6.07%) then decline
   - SPACs peak early (5-day: 2.13%) then stabilize

4. **Median returns tell a different story**
   - At 1-year: Non-SPACs have negative median (-0.70%)
   - SPACs maintain positive median (3.73%)
   - Suggests Non-SPACs have more extreme negative outliers

5. **Extreme outliers in Non-SPACs**
   - Maximum returns: 6,138%, 5,798%, 8,920%, 12,920%
   - SPAC maximums: 410%, 581%, 750%, 64%

---

## 4. Question 6: Index Inclusion Performance

### 4.1 S&P 500 Inclusion Impact

#### Methodology

```python
# S&P 500 inclusion performance
sp_performance = stock_ipos.groupby('sp')[
    'sym_252day_ret'
].agg(['mean', 'median', 'std', 'count', 'min', 'max'])
```

#### Results

**Table 4: S&P 500 Inclusion Performance (1-Year Returns)**

| Category | Mean | Median | Std Dev | Count | Min | Max |
|----------|------|--------|---------|-------|-----|-----|
| **Not Included** | 3.71% | 0.00% | 2.885 | 3,630 | -99.7% | 12,920% |
| **Included** | 29.29% | 17.10% | 0.538 | 51 | -71.8% | 244.8% |

#### Key Findings

1. **S&P 500 included stocks dramatically outperform**
   - Mean: 29.29% vs 3.71% (7.9x higher)
   - Median: 17.10% vs 0.00%

2. **Included stocks show lower volatility**
   - Std dev: 0.538 vs 2.885 (5.4x lower)
   - Despite higher returns, more stable performance

3. **Highly selective process**
   - Only 51 out of 3,681 IPOs (1.4%) achieved inclusion
   - Strong quality signal

4. **Positive median for included stocks**
   - 17.10% median suggests consistent performance
   - Not driven by outliers

---

### 4.2 Russell 1000 Inclusion Impact

#### Methodology

```python
# Russell 1000 inclusion performance
russell_performance = stock_ipos.groupby('russell')[
    'sym_252day_ret'
].agg(['mean', 'median', 'std', 'count', 'min', 'max'])
```

#### Results

**Table 5: Russell 1000 Inclusion Performance (1-Year Returns)**

| Category | Mean | Median | Std Dev | Count | Min | Max |
|----------|------|--------|---------|-------|-----|-----|
| **Not Included** | 3.09% | -0.10% | 2.919 | 3,538 | -99.7% | 12,920% |
| **Included** | 28.16% | 13.38% | 0.738 | 143 | -88.5% | 441.4% |

#### Key Findings

1. **Russell 1000 included stocks also significantly outperform**
   - Mean: 28.16% vs 3.09% (9.1x higher)
   - Median: 13.38% vs -0.10%

2. **Lower volatility despite higher returns**
   - Std dev: 0.738 vs 2.919 (4.0x lower)
   - Similar pattern to S&P 500

3. **More inclusive than S&P 500**
   - 143 out of 3,681 IPOs (3.9%) achieved inclusion
   - 2.8x more inclusive than S&P 500

4. **Consistent positive performance**
   - Positive median (13.38%) indicates broad-based success
   - Not included group has negative median (-0.10%)

---

### 4.3 Comparative Analysis

**Table 6: Index Inclusion Comparison**

| Category | Count | % of Total | Mean 1Y Return | Median 1Y Return | Std Dev |
|----------|-------|------------|----------------|------------------|---------|
| **Not in Either Index** | 3,487 | 94.7% | 2.98% | -0.12% | 2.922 |
| **S&P 500** | 51 | 1.4% | 29.29% | 17.10% | 0.538 |
| **Russell 1000** | 143 | 3.9% | 28.16% | 13.38% | 0.738 |

#### Key Insights

1. **Index inclusion is a strong performance predictor**
   - Both indices show ~9x higher mean returns
   - Median returns are positive vs negative/zero for non-included

2. **S&P 500 is more selective and stable**
   - Fewer stocks (1.4% vs 3.9%)
   - Lower volatility (0.538 vs 0.738)
   - Slightly higher mean return (29.29% vs 28.16%)

3. **Non-included stocks struggle**
   - 94.7% of IPOs not in major indices
   - Negative median return (-0.12%)
   - High volatility (2.922)

---

## 5. Conclusions

### 5.1 SPAC vs Non-SPAC Performance (Question 5)

**Summary:**
- **SPACs underperform** across all time horizons (Day 0 through 1-year)
- **SPACs are more stable** with 3-19x lower volatility
- **Non-SPACs have extreme outcomes** (both positive and negative)
- **Median performance favors SPACs** at 1-year (3.73% vs -0.70%)

**Implications:**
- SPACs may appeal to risk-averse investors seeking stability
- Non-SPACs offer higher upside potential but with greater risk
- Abnormal Day 0 returns (≥100%) are exclusive to Non-SPACs

### 5.2 Index Inclusion Impact (Question 6)

**Summary:**
- **Index inclusion strongly predicts superior performance**
  - S&P 500: 29.29% vs 3.71% (7.9x)
  - Russell 1000: 28.16% vs 3.09% (9.1x)
- **Included stocks show lower volatility** despite higher returns
- **Highly selective process** (1.4% S&P, 3.9% Russell)
- **Consistent positive performance** (positive medians for included stocks)

**Implications:**
- Index inclusion serves as a quality signal
- Investors may benefit from focusing on IPOs with index potential
- The "index effect" appears robust across both S&P 500 and Russell 1000

### 5.3 Overall Insights

1. **Risk-Return Tradeoff:**
   - SPACs: Lower returns, lower risk
   - Non-SPACs: Higher returns, higher risk
   - Index-included: Highest returns, lowest risk (best risk-adjusted)

2. **Investment Strategy Implications:**
   - For stability: Consider SPACs
   - For upside potential: Consider Non-SPACs
   - For optimal risk-adjusted returns: Focus on index-inclusion candidates

3. **Market Efficiency:**
   - Index inclusion appears to identify quality IPOs
   - The market rewards index-included stocks with superior performance
   - Non-included stocks show negative median returns, suggesting selection matters

---

## 6. Limitations

1. **Survivorship Bias:** Dataset may not include delisted IPOs
2. **Time Period:** Analysis covers specific time period; results may vary across market cycles
3. **Causality:** Index inclusion correlation doesn't prove causation
4. **SPAC Structure:** Analysis doesn't account for SPAC merger timing and structure differences

---

## 7. References

**Data Sources:**
- `stock_ipos_20231004.csv` - IPO dataset (3,681 observations)
- `list_of_all_spacs.xlsx` - SPAC identification
- `sp500_202308.xlsx` - S&P 500 constituents (August 2023)
- `russ_1000_202308.xlsx` - Russell 1000 constituents (August 2023)

**Analysis Tools:**
- Python 3.x
- pandas - Data manipulation
- numpy - Numerical operations
- matplotlib & seaborn - Visualizations

---

## Appendix: Statistical Summary

**Dataset Composition:**
- Total IPOs: 3,681
- SPACs: 251 (6.8%)
- Non-SPACs: 3,430 (93.2%)
- S&P 500 Included: 51 (1.4%)
- Russell 1000 Included: 143 (3.9%)
- Not in Major Indices: 3,487 (94.7%)

**Return Windows Analyzed:**
- Day 0 (IPO date)
- 5-day
- 22-day (approximately 1 month)
- 91-day (approximately 3 months)
- 252-day (approximately 1 year)

---

**Report Generated:** December 4, 2025  
**Analysis Period:** IPO data through October 4, 2023  
**Total Pages:** 8
