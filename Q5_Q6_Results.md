# Questions 5 & 6: Analysis Results

## Question 5: SPACs vs Non-SPACs Return Analysis

### 5(i) Day 0 Return Analysis

**Code:**
```python
# Flag abnormal returns (returns >= 1 or 100% are considered abnormal)
stock_ipos['day0_lvl'] = np.where(stock_ipos['sym_day0_OTC'] < 1, 'normal', 'abnormal')

# Summarize day0 return by SPACs
stock_ipos.groupby(['day0_lvl', 'spac'])['sym_day0_OTC'].agg(['mean', 'median', 'std', 'count', 'min', 'max'])
```

**Output:**
```
Day 0 Return Statistics by Level and SPAC Status:
                   mean    median       std  count       min        max
day0_lvl spac                                                          
abnormal no    2.917992  2.244721  3.009960     30  1.017391  17.750000
normal   no   -0.004677  0.000000  0.126626   3400 -0.851190   0.973500
         yes  -0.008804  0.000000  0.070245    251 -0.550420   0.428571

Overall Day 0 Return by SPAC Status:
          mean  median       std  count
spac                                   
no    0.020885     0.0  0.408161   3430
yes  -0.008804     0.0  0.070245    251
```

**Comments on SPACs vs Non-SPACs Day 0 Returns:**

1. **SPACs have lower and negative mean returns on Day 0** (-0.88% for SPACs vs +2.09% for Non-SPACs)
2. **Both have median returns of 0%**, suggesting many IPOs trade at their offer price
3. **SPACs show much lower volatility** (std = 0.070 vs 0.408 for Non-SPACs)
4. **SPACs have a narrower range** (min: -55%, max: +43%) compared to Non-SPACs (min: -85%, max: +1775%)
5. **Abnormal returns (≥100%) only occur in Non-SPACs** (30 cases with mean return of 292%)
6. **SPACs appear to have more stable, but slightly negative, Day 0 performance**

---

### 5(ii) Analysis for Other Return Windows

**Code:**
```python
windows = ['sym_5day_ret', 'sym_22day_ret', 'sym_91day_ret', 'sym_252day_ret']
for w in windows:
    print(stock_ipos.groupby('spac')[w].agg(['mean', 'median', 'std', 'count', 'min', 'max']))
```

**Output:**

**5-day Return Statistics:**
```
          mean    median       std  count       min        max
spac                                                          
no    0.034031  0.000000  1.252358   3430 -1.000000  61.381819
yes   0.021284  0.001029  0.276315    251 -0.683117   4.100000
```

**22-day (1-month) Return Statistics:**
```
          mean    median       std  count       min        max
spac                                                          
no    0.047191  0.002239  1.344239   3430 -0.951674  57.981814
yes   0.030329  0.003061  0.376508    251 -0.680844   5.809045
```

**91-day (3-month) Return Statistics:**
```
          mean    median       std  count      min        max
spac                                                         
no    0.060706  0.001021  2.007227   3430 -0.98368  89.200000
yes   0.030150  0.009231  0.477305    251 -0.67987   7.498492
```

**252-day (1-year) Return Statistics:**
```
          mean    median       std  count       min         max
spac                                                           
no    0.042634 -0.006979  2.968079   3430 -0.997339  129.200000
yes   0.013135  0.037302  0.157165    251 -0.775701    0.635176
```

**Key Findings:**
- **Non-SPACs consistently have higher mean returns** across all time windows
- **SPACs show consistently lower volatility** (much smaller standard deviations)
- **Non-SPACs have extreme outliers** (max returns of 6138%, 5798%, 8920%, and 12920% for each window)
- **SPACs have more modest maximum returns** (410%, 581%, 750%, and 64% respectively)
- **Median returns are near zero or slightly positive** for both groups across all windows
- **At 1-year, Non-SPACs have negative median return** (-0.70%) while SPACs have positive median (3.73%)

---

## Question 6: IPO Return Performance - Index Inclusion Analysis

### 6. S&P 500 Inclusion Performance (1-year return)

**Code:**
```python
stock_ipos.groupby('sp')['sym_252day_ret'].agg(['mean', 'median', 'std', 'count', 'min', 'max'])
```

**Output:**
```
         mean    median       std  count       min         max
sp                                                            
no   0.037079  0.000000  2.884588   3630 -0.997339  129.200000
yes  0.292900  0.171014  0.538144     51 -0.718000    2.448239
```

**Key Findings:**
- **S&P 500 included stocks significantly outperform** (mean: 29.29% vs 3.71%)
- **S&P 500 stocks have positive median returns** (17.10% vs 0.00%)
- **S&P 500 stocks show lower volatility** (std: 0.538 vs 2.885)
- **Only 51 out of 3,681 IPOs** (1.4%) made it into the S&P 500
- **S&P inclusion appears to be a strong positive signal** for IPO performance

---

### 6(i) Russell 1000 Inclusion Performance (1-year return)

**Code:**
```python
stock_ipos.groupby('russell')['sym_252day_ret'].agg(['mean', 'median', 'std', 'count', 'min', 'max'])
```

**Output:**
```
             mean    median       std  count       min         max
russell                                                           
no       0.030883 -0.001020  2.918564   3538 -0.997339  129.200000
yes      0.281593  0.133805  0.737627    143 -0.885246    4.414086
```

**Key Findings:**
- **Russell 1000 included stocks also significantly outperform** (mean: 28.16% vs 3.09%)
- **Russell 1000 stocks have positive median returns** (13.38% vs -0.10%)
- **Russell 1000 stocks show lower volatility** (std: 0.738 vs 2.919)
- **143 out of 3,681 IPOs** (3.9%) made it into the Russell 1000
- **Russell 1000 inclusion shows similar positive signal** as S&P 500, though with slightly more volatility

---

## Summary

### Question 5 Conclusions:
- SPACs underperform Non-SPACs across all time horizons
- SPACs are more stable with lower volatility
- Non-SPACs have more extreme outcomes (both positive and negative)

### Question 6 Conclusions:
- Index inclusion (both S&P 500 and Russell 1000) is strongly associated with superior IPO performance
- Included stocks have ~8-9x higher mean returns at 1-year
- Included stocks show lower volatility despite higher returns
- Very few IPOs achieve index inclusion (1.4% for S&P 500, 3.9% for Russell 1000)
