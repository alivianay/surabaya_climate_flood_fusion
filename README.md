# Surabaya Climate-Flood Fusion
## Comprehensive Technical Report

**Project Name:** Surabaya Climate-Flood Fusion  
**Author:** NIM 22031554041  
**Period:** January - December 2023  
**Date:** 2024

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Project Overview](#project-overview)
3. [Data Sources](#data-sources)
4. [Data Normalization Pipeline](#data-normalization-pipeline)
5. [Data Cleaning & Preprocessing](#data-cleaning--preprocessing)
6. [Feature Engineering](#feature-engineering)
7. [Data Integration](#data-integration)
8. [Exploratory Data Analysis](#exploratory-data-analysis)
9. [Visualizations](#visualizations)
10. [Key Findings & Insights](#key-findings--insights)
11. [Technical Implementation](#technical-implementation)
12. [Project Structure](#project-structure)
13. [Dependencies & Tools](#dependencies--tools)

---

## Executive Summary

This project integrates climate data from Tanjung Perak weather station in Surabaya with social media (X/Twitter) data to analyze the relationship between weather conditions and public discourse about rain, floods, and traffic congestion. The project demonstrates a complete data wrangling pipeline from raw data collection through normalization, cleaning, feature engineering, integration, and analysis.

**Key Achievements:**
- Processed 12 months of climate data (270 days)
- Integrated 106 social media posts
- Created 23 engineered features
- Generated comprehensive visualizations
- Identified correlations between weather patterns and social media activity

---

## Project Overview

### Objective

To create an integrated dataset combining meteorological data with social media sentiment to understand how weather conditions, particularly rainfall, correlate with public discussions about flooding and traffic issues in Surabaya.

### Methodology

1. **Data Collection**: Climate data from Excel files and social media data from X/Twitter
2. **Data Normalization**: Standardize file formats and data structures
3. **Data Cleaning**: Handle missing values, outliers, and inconsistencies
4. **Feature Engineering**: Create derived features for enhanced analysis
5. **Data Integration**: Merge climate and social media datasets
6. **Analysis**: Statistical analysis and visualization

---

## Data Sources

### 1. Climate Data (Meteorological Data)

**Source:** Tanjung Perak Weather Station, Surabaya  
**Format:** Excel files (.xlsx)  
**Period:** January - December 2023  
**Files:** 12 monthly files (one per month)

**Original Files:**
- `tanjung_perak_1_januari_2023.xlsx`
- `tanjung_perak_1_februari_2023.xlsx`
- `tanjung_perak_1_maret_2023.xlsx`
- `tanjung_perak_1_april_2023.xlsx`
- `tanjung_perak_1_mei_2023.xlsx`
- `tanjung_perak_1_juni_2023.xlsx`
- `tanjung_perak_1_juli_2023.xlsx`
- `tanjung_perak_1_agustus_2023.xlsx`
- `tanjung_perak_1_september_2023.xlsx`
- `tanjung_perak_1_oktober_2023.xlsx`
- `tanjung_perak_1_november_2023.xlsx`
- `tanjung_perak_1_desember_2023.xlsx`

**Variables Collected:**
- **TANGGAL**: Date (DD-MM-YYYY format)
- **TN**: Minimum Temperature (°C)
- **TX**: Maximum Temperature (°C)
- **TAVG**: Average Temperature (°C)
- **RH_AVG**: Average Relative Humidity (%)
- **RR**: Rainfall (mm)
- **SS**: Sunshine Duration (hours)
- **FF_X**: Maximum Wind Speed (m/s)
- **DDD_X**: Wind Direction at Maximum Speed (degrees)
- **FF_AVG**: Average Wind Speed (m/s)
- **DDD_CAR**: Wind Direction Category (C, E, N, S, W, etc.)

### 2. Social Media Data (X/Twitter)

**Source:** X/Twitter scraping  
**Format:** Excel file (.xlsx)  
**File:** `data_sraping_x_2023.xlsx`  
**Period:** January - December 2023

**Structure:**
- Date column (TANGGAL)
- Multiple tweet columns (tweet1, tweet2, tweet3, tweet4, tweet5, etc.)
- Each row represents a date with multiple tweets

**Content:** Indonesian language tweets about:
- Rain (hujan)
- Floods (banjir)
- Traffic congestion (macet)
- Weather-related events in Surabaya

---

## Data Normalization Pipeline

### Step 1: File Name Standardization

**Purpose:** Standardize file naming conventions for easier processing

**Process:**
```python
def simplify_filename(data_folder):
    # Convert to lowercase
    # Replace spaces and hyphens with underscores
    # Remove multiple consecutive underscores
    # Strip leading/trailing underscores
    # Normalize file extensions
```

**Result:** All files follow consistent naming: `tanjung_perak_1_[month]_2023.xlsx`

### Step 2: Climate Data Extraction

**Location:** `src/data_normalize/normalize_data.ipynb`

**Process:**
1. **Read Excel files** with `header=None` to handle inconsistent headers
2. **Locate header row** by searching for "TANGGAL" string
3. **Extract data** starting from header row
4. **Remove metadata** by finding "KETERANGAN:" row and truncating
5. **Clean data** by removing rows before header
6. **Save cleaned data** as CSV files with `_clean` suffix

**Code Logic:**
```python
for file in tanjung_perak_files:
    df_raw = pd.read_excel(file, header=None)
    header_row = df_raw[df_raw.eq("TANGGAL").any(axis=1)].index[0]
    df = pd.read_excel(file, header=header_row)
    df = df.drop(range(0, header_row + 1))
    
    # Remove metadata section
    ket_row = df[df.eq("KETERANGAN:").any(axis=1)].index
    if len(ket_row) > 0:
        stop_at = ket_row[0]
        df = df.loc[:stop_at - 1]
    
    df = df.reset_index(drop=True)
    df.to_csv(output_path + "_clean.csv", index=False)
```

**Output:** 12 cleaned CSV files in `data/normalize/` directory

### Step 3: Climate Data Merging

**Location:** `src/data_normalize/merge.py`

**Process:**
1. **Find all cleaned files** matching pattern `*tanjung*.csv`
2. **Read each CSV file** individually
3. **Convert date column** to datetime format (handling DD-MM-YYYY)
4. **Concatenate all dataframes** using `pd.concat()`
5. **Remove duplicates** to ensure data quality
6. **Save merged file** as `iklim_surabaya_2023.csv`

**Key Features:**
- Handles date conversion errors gracefully
- Reports number of rows from each file
- Removes duplicate entries
- Validates date conversions

**Output:** Single merged file `iklim_surabaya_2023.csv` with 270 rows

### Step 4: Social Media Data Transformation

**Location:** `src/data_normalize/normalize_data.ipynb`

**Process:**
1. **Load Excel file** containing tweets
2. **Identify tweet columns** (columns starting with "tweet")
3. **Transform from wide to long format** using `pd.melt()`
   - `id_vars`: TANGGAL (date)
   - `value_vars`: All tweet columns
   - `var_name`: tweet_id
   - `value_name`: tweet_text
4. **Remove empty rows** (NaN and empty strings)
5. **Sort by date** chronologically
6. **Save normalized data** as `tweets_normalized.csv`

**Transformation:**
- **Before:** Wide format (one row per date, multiple tweet columns)
- **After:** Long format (one row per tweet, date and tweet text)

**Output:** `tweets_normalized.csv` with 106 tweet records

---

## Data Cleaning & Preprocessing

### Climate Data Cleaning

**Location:** `src/processing/live_code_quests.ipynb`

#### 1. Date Conversion

**Issue:** Dates in DD-MM-YYYY format (e.g., "09-08-2023")  
**Solution:**
```python
df_iklim['TANGGAL'] = pd.to_datetime(df_iklim['TANGGAL'], format='%d-%m-%Y')
```

#### 2. Missing Value Handling

**Strategy:** Time-series aware imputation for climate data

**Process:**
1. **Forward Fill (ffill)**: Use previous day's value (weather is continuous)
2. **Backward Fill (bfill)**: Handle missing values at start of dataset
3. **Linear Interpolation**: Fill gaps between known values
4. **Median Imputation**: Last resort for remaining missing values

**Implementation:**
```python
numeric_cols = ['TN', 'TX', 'TAVG', 'RH_AVG', 'RR', 'SS', 'FF_X', 'FF_AVG', 'DDD_X']

for col in numeric_cols:
    df_iklim[col] = pd.to_numeric(df_iklim[col], errors='coerce')
    df_iklim[col] = df_iklim[col].ffill()  # Forward fill
    df_iklim[col] = df_iklim[col].bfill()  # Backward fill
    df_iklim[col] = df_iklim[col].interpolate(method='linear')  # Interpolation
    if df_iklim[col].isnull().sum() > 0:
        df_iklim[col].fillna(df_iklim[col].median(), inplace=True)  # Median
```

**Categorical Variables:**
- **DDD_CAR**: Mode imputation (most frequent wind direction)

**Result:** Reduced missing values from 11 to 0

#### 3. Data Type Conversion

**Process:**
- Convert numeric columns from string to numeric (handles "-" and other non-numeric values)
- Use `errors='coerce'` to convert invalid values to NaN

#### 4. Row Removal

**Process:** Remove rows with any remaining missing values after imputation
```python
df_iklim = df_iklim.dropna()
```

**Result:** Clean dataset with 269 complete rows

### Social Media Data Cleaning

**Location:** `src/processing/live_code_quests.ipynb`

#### 1. Date Conversion

**Issue:** Dates in YYYY-MM-DD format (ISO 8601)  
**Solution:**
```python
df_tweets['TANGGAL'] = pd.to_datetime(df_tweets['TANGGAL'], format='%Y-%m-%d')
```

#### 2. Text Normalization

**Process:**
- Convert to lowercase: `df_tweets['tweet_text'].str.lower()`
- Remove leading/trailing whitespace: `df_tweets['tweet_text'].str.strip()`

#### 3. Date Filtering (Optional)

**Process:** Filter to specific months (January-February 2023)
```python
df_tweets = df_tweets[(df_tweets['TANGGAL'].dt.month >= 1) & 
                       (df_tweets['TANGGAL'].dt.month <= 2)]
```

**Result:** 48 tweets for January-February period

---

## Feature Engineering

### Temporal Features

**Location:** `src/processing/take_home_quests.ipynb`

#### 1. Month
```python
df['Month'] = df['TANGGAL'].dt.month_name()
```
**Purpose:** Categorical month for seasonal analysis

#### 2. Day of Week
```python
df['day_of_week'] = df['TANGGAL'].dt.dayofweek  # 0=Monday, 6=Sunday
```
**Purpose:** Numeric day (0-6) for weekday/weekend analysis

#### 3. Day Name
```python
df['day_name'] = df['TANGGAL'].dt.day_name()
```
**Purpose:** Categorical day name (Monday, Tuesday, etc.)

#### 4. Week of Year
```python
df['week_of_year'] = df['TANGGAL'].dt.isocalendar().week
```
**Purpose:** Week number (1-52) for weekly patterns

#### 5. Is Weekend
```python
df['is_weekend'] = (df['day_of_week'] >= 5).astype(int)
```
**Purpose:** Binary indicator (0=weekday, 1=weekend)

### Weather-Derived Features

#### 6. Temperature Range
```python
df['temp_range'] = df['TX'] - df['TN']
```
**Purpose:** Daily temperature variation indicator

#### 7. Heat Index
```python
# Simplified heat index calculation
df['heat_index'] = 0.5 * (df['TAVG'] + df['RH_AVG'] / 100 * df['TAVG'])
```
**Purpose:** Perceived temperature considering humidity

#### 8. Rain Category
```python
df['rain_category'] = pd.cut(df['RR'], 
                             bins=[-1, 0, 5, 20, float('inf')],
                             labels=['No Rain', 'Light', 'Moderate', 'Heavy'])
```
**Purpose:** Categorical rainfall classification

#### 9. Rainfall Rolling Windows
```python
df['rainfall_3day'] = df['RR'].rolling(window=3, min_periods=1).sum()
df['rainfall_7day'] = df['RR'].rolling(window=7, min_periods=1).sum()
```
**Purpose:** Cumulative rainfall over 3 and 7 days

#### 10. Weather Condition
```python
df['weather_condition'] = df.apply(lambda x: 
    'Rainy' if x['RR'] > 0 else 
    'Cloudy' if x['SS'] < 5 else 'Sunny', axis=1)
```
**Purpose:** Simplified weather classification

#### 11. Wind Category
```python
df['wind_category'] = pd.cut(df['FF_AVG'], 
                             bins=[0, 2, 5, 10, float('inf')],
                             labels=['Calm', 'Light', 'Moderate', 'Strong'])
```
**Purpose:** Wind speed classification

#### 12. Wind Direction Simplification
```python
df['wind_direction_simple'] = df['DDD_CAR'].map({
    'N': 'North', 'S': 'South', 'E': 'East', 'W': 'West',
    'C': 'Calm', 'NE': 'Northeast', 'NW': 'Northwest',
    'SE': 'Southeast', 'SW': 'Southwest'
})
```
**Purpose:** Human-readable wind directions

### Social Media Features

#### 13. Engagement Rate
```python
df['engagement_rate'] = df['hujan_mention'] / (df['tweet_count'] + 1)
```
**Purpose:** Ratio of rain mentions to total tweets

#### 14. Flood Risk Score
```python
df['flood_risk_score'] = (
    (df['RR'] > 20).astype(int) * 3 +
    (df['rainfall_3day'] > 50).astype(int) * 2 +
    (df['banjir_mention'] > 0).astype(int) * 1
)
```
**Purpose:** Composite score indicating flood risk (0-6 scale)

#### 15. Social Activity Level
```python
df['social_activity_level'] = pd.cut(df['tweet_count'],
                                     bins=[-1, 0, 5, 10, float('inf')],
                                     labels=['None', 'Low', 'Medium', 'High'])
```
**Purpose:** Categorical social media activity classification

#### 16. Weather Awareness
```python
df['weather_awareness'] = (df['hujan_mention'] > 0).astype(int)
```
**Purpose:** Binary indicator of weather-related social media activity

### Interaction Features

#### 17. Rain-Humidity Interaction
```python
df['rain_humidity_interaction'] = df['RR'] * df['RH_AVG']
```
**Purpose:** Combined effect of rainfall and humidity

#### 18. Temperature-Sunlight Interaction
```python
df['temp_sunlight_interaction'] = df['TAVG'] * df['SS']
```
**Purpose:** Combined effect of temperature and sunshine

#### 19. Rain-Social Interaction
```python
df['rain_social_interaction'] = df['RR'] * df['tweet_count']
```
**Purpose:** Interaction between rainfall and social media activity

### Lag Features

#### 20-22. Lagged Variables
```python
df['RR_lag1'] = df['RR'].shift(1)
df['TAVG_lag1'] = df['TAVG'].shift(1)
df['tweet_count_lag1'] = df['tweet_count'].shift(1)
```
**Purpose:** Previous day's values for time-series analysis

**Total Engineered Features:** 23 new features from 15 original features

---

## Data Integration

### Process

**Location:** `src/processing/live_code_quests.ipynb`

#### Step 1: Tweet Aggregation

**Purpose:** Aggregate multiple tweets per day into daily statistics

**Process:**
```python
tweet_agg = df_tweets.groupby('TANGGAL').agg({
    'tweet_id': 'count',
    'tweet_text': lambda x: ' '.join(x)
}).reset_index()
tweet_agg.columns = ['TANGGAL', 'tweet_count', 'tweet_combined']
```

**Result:** One row per date with:
- `tweet_count`: Number of tweets on that date
- `tweet_combined`: Concatenated text of all tweets

#### Step 2: Feature Extraction from Tweets

**Purpose:** Extract keyword mentions from aggregated tweets

**Process:**
```python
tweet_agg['hujan_mention'] = tweet_agg['tweet_combined'].str.count('hujan')
tweet_agg['banjir_mention'] = tweet_agg['tweet_combined'].str.count('banjir')
tweet_agg['macet_mention'] = tweet_agg['tweet_combined'].str.count('macet')
tweet_agg['deras_mention'] = (tweet_agg['tweet_combined'].str.count('deres') + 
                               tweet_agg['tweet_combined'].str.count('deras'))
```

**Keywords Extracted:**
- `hujan`: Rain
- `banjir`: Flood
- `macet`: Traffic congestion
- `deras/deres`: Heavy/intense (rain)

#### Step 3: Data Merging

**Process:**
```python
df_integrated = pd.merge(df_iklim, 
                        tweet_agg[['TANGGAL', 'tweet_count', 'hujan_mention',
                                   'banjir_mention', 'macet_mention']], 
                        on='TANGGAL', 
                        how='left')
```

**Merge Type:** Left join (preserves all climate data)

#### Step 4: Missing Value Handling for Tweets

**Process:** Fill NaN values for days without tweets
```python
df_integrated[['tweet_count', 'hujan_mention', 'banjir_mention', 'macet_mention']] = \
    df_integrated[['tweet_count', 'hujan_mention', 'banjir_mention', 'macet_mention']].fillna(0)
```

**Result:** Complete integrated dataset with 269 rows

---

## Exploratory Data Analysis

### Descriptive Statistics

**Location:** `summary/summary_statistics.txt`

#### Climate Variables

| Variable | Mean | Min | Max | Std Dev |
|----------|------|-----|-----|---------|
| TN (Min Temp) | 25.23°C | 22.2°C | 28.4°C | 1.23 |
| TX (Max Temp) | 33.66°C | 29.6°C | 37.4°C | 1.45 |
| TAVG (Avg Temp) | 29.01°C | 25.9°C | 32.3°C | 1.18 |
| RH_AVG (Humidity) | 71.76% | 58% | 90% | 7.50 |
| RR (Rainfall) | 500.18 mm | 0 mm | 8,888 mm | 2,042.19 |
| SS (Sunshine) | 6.80 hours | 0 hours | 9.9 hours | 2.60 |
| FF_X (Max Wind) | 6.17 m/s | 3 m/s | 14 m/s | 1.63 |
| FF_AVG (Avg Wind) | 2.13 m/s | 1 m/s | 5 m/s | 0.85 |

#### Social Media Variables

| Variable | Mean | Min | Max | Std Dev |
|----------|------|-----|-----|---------|
| tweet_count | 0.18 | 0 | 17 | 1.29 |
| hujan_mention | 0.11 | 0 | 6 | 0.70 |
| banjir_mention | 0.10 | 0 | 19 | 1.19 |
| macet_mention | 0.02 | 0 | 3 | 0.22 |

### Monthly Aggregation

**Key Findings:**
- **Highest Rainfall:** December (35,652 mm), June (26,664 mm)
- **Highest Temperature:** October (30.84°C), November (30.58°C)
- **Most Tweets:** February (38 tweets), January (10 tweets)
- **Rain Mentions:** February (20), January (9)

### Correlation Analysis

**Location:** `src/processing/live_code_quests.ipynb`

**Key Correlation:**
- RR (Rainfall) vs hujan_mention: -0.036 (weak negative correlation)

**Interpretation:** Slight negative correlation suggests tweets about rain may not directly correlate with actual rainfall amounts, possibly due to timing or other factors.

---

## Visualizations

### Generated Visualizations

**Location:** `visualization/` directory

#### 1. Live Code Analysis (`live_code_analysis.png`)

**Components:**
1. **Time Series - Daily Rainfall (RR)**
   - Line plot showing rainfall over time
   - X-axis: Date
   - Y-axis: Rainfall (mm)
   - Markers indicate data points

2. **Bar Chart - Daily Tweet Activity**
   - Bar plot showing number of tweets per day
   - X-axis: Date
   - Y-axis: Tweet count
   - Orange bars with transparency

3. **Scatter Plot - Rainfall vs Rain Mentions**
   - Scatter plot with color mapping
   - X-axis: Rainfall (mm)
   - Y-axis: Rain mentions in tweets
   - Color: Average temperature (coolwarm colormap)
   - Size: Fixed (100)

4. **Box Plot - Temperature Distribution**
   - Three box plots side by side
   - Variables: Minimum Temp, Average Temp, Maximum Temp
   - Shows distribution, quartiles, and outliers

#### 2. Take Home Analysis (`take_home_analysis.png`)

**Components:** (Similar structure with additional features from feature engineering)

### Visualization Code Structure

```python
fig, axes = plt.subplots(2, 2, figsize=(15, 10))
fig.suptitle('Analisis Data Iklim dan Tweet Jan-Feb 2023', 
             fontsize=16, fontweight='bold')

# Plot 1: Time Series Rainfall
axes[0, 0].plot(df_integrated['TANGGAL'], df_integrated['RR'], 
                marker='o', linewidth=2, color='blue')
axes[0, 0].set_title('Curah Hujan Harian (RR)', fontweight='bold')
axes[0, 0].set_xlabel('Tanggal')
axes[0, 0].set_ylabel('Curah Hujan (mm)')
axes[0, 0].grid(True, alpha=0.3)
axes[0, 0].tick_params(axis='x', rotation=45)

# Plot 2: Tweet Activity
axes[0, 1].bar(df_integrated['TANGGAL'], df_integrated['tweet_count'], 
               color='orange', alpha=0.7)
axes[0, 1].set_title('Aktivitas Tweet Harian', fontweight='bold')
axes[0, 1].set_xlabel('Tanggal')
axes[0, 1].set_ylabel('Jumlah Tweet')
axes[0, 1].tick_params(axis='x', rotation=45)

# Plot 3: Scatter - Rainfall vs Tweets
axes[1, 0].scatter(df_integrated['RR'], df_integrated['hujan_mention'], 
                   s=100, alpha=0.6, c=df_integrated['TAVG'], cmap='coolwarm')
axes[1, 0].set_title('Curah Hujan vs Mention "Hujan"', fontweight='bold')
axes[1, 0].set_xlabel('Curah Hujan (mm)')
axes[1, 0].set_ylabel('Mention "Hujan" di Tweet')
axes[1, 0].grid(True, alpha=0.3)

# Plot 4: Boxplot Temperature
temp_data = [df_integrated['TN'], df_integrated['TAVG'], df_integrated['TX']]
axes[1, 1].boxplot(temp_data, labels=['Min Temp', 'Avg Temp', 'Max Temp'])
axes[1, 1].set_title('Distribusi Temperatur', fontweight='bold')
axes[1, 1].set_ylabel('Temperatur (°C)')
axes[1, 1].grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig('../../visualization/live_code_analysis.png', dpi=300, bbox_inches='tight')
```

---

## Key Findings & Insights

### 1. Data Quality

- **Initial Missing Values:** 11
- **Final Missing Values:** 0
- **Data Completeness:** 100% after cleaning
- **Total Records:** 269 days of climate data, 106 tweets

### 2. Weather Patterns

- **Average Temperature:** 29.01°C (tropical climate)
- **Temperature Range:** 22.2°C - 37.4°C
- **Total Rainfall:** 134,549 mm over 269 days
- **Rainy Days:** 87 days (32.3% of period)
- **Highest Single Day Rainfall:** 8,888 mm

### 3. Social Media Activity

- **Total Tweets:** 48 tweets (Jan-Feb period)
- **Most Active Month:** February (38 tweets)
- **Rain Mentions:** 29 total mentions
- **Flood Mentions:** 19 total mentions
- **Traffic Mentions:** 3 total mentions

### 4. Correlations

- **Rainfall vs Rain Mentions:** Weak negative correlation (-0.036)
  - **Interpretation:** Social media activity about rain doesn't directly correlate with rainfall amount
  - **Possible Reasons:** 
    - Timing differences (tweets may occur before/during/after rain)
    - Perception vs reality
    - Other factors influencing social media activity

### 5. Feature Engineering Impact

- **Original Features:** 15
- **Engineered Features:** 23
- **Total Features:** 38
- **Feature Categories:**
  - Temporal: 5 features
  - Weather-derived: 7 features
  - Social media: 4 features
  - Interactions: 3 features
  - Lag features: 3 features

### 6. Flood Risk Analysis

- **High Flood Risk Days:** 7 days identified
- **Risk Factors:**
  - Heavy rainfall (>20mm)
  - Cumulative rainfall (>50mm over 3 days)
  - Social media mentions of floods

### 7. Weather Awareness

- **Weather Awareness Rate:** 2.2%
- **Definition:** Percentage of days with weather-related social media activity
- **Implication:** Low but meaningful social media engagement with weather events

---

## Technical Implementation

### Project Structure

```
surabaya_climate_flood_fusion/
├── data/
│   ├── data_iklim_2023/          # Raw climate data (Excel files)
│   └── normalize/                 # Normalized and cleaned data (CSV files)
│       ├── iklim_surabaya_2023.csv
│       ├── tweets_normalized.csv
│       ├── integrated_data.csv
│       └── tanjung_perak_*_clean.csv (12 files)
├── src/
│   ├── data_normalize/
│   │   ├── normalize_data.ipynb  # Data normalization pipeline
│   │   └── merge.py               # Climate data merging script
│   └── processing/
│       ├── live_code_quests.ipynb # Live coding analysis
│       └── take_home_quests.ipynb # Take-home assignment analysis
├── visualization/
│   ├── live_code_analysis.png     # Live code visualizations
│   └── take_home_analysis.png     # Take-home visualizations
├── summary/
│   ├── feature_engineering_report.txt
│   └── summary_statistics.txt
├── main.py                        # Entry point (placeholder)
├── pyproject.toml                # Project dependencies
└── README.md                      # Project documentation
```

### Data Flow

```
Raw Data (Excel)
    ↓
[File Name Standardization]
    ↓
[Data Extraction & Cleaning]
    ↓
Normalized CSV Files
    ↓
[Data Merging]
    ↓
Integrated Climate Data (iklim_surabaya_2023.csv)
    ↓
[Data Cleaning & Preprocessing]
    ↓
[Feature Engineering]
    ↓
[Data Integration with Social Media]
    ↓
Final Integrated Dataset
    ↓
[Exploratory Data Analysis]
    ↓
[Visualization]
    ↓
Reports & Insights
```

### Key Scripts & Functions

#### 1. File Name Standardization
- **Function:** `simplify_filename(data_folder)`
- **Purpose:** Normalize file names for consistency
- **Operations:** Lowercase, replace spaces/hyphens, remove duplicates

#### 2. Climate Data Extraction
- **Process:** Extract data from Excel files with inconsistent headers
- **Key Steps:**
  - Find header row dynamically
  - Remove metadata sections
  - Save as clean CSV

#### 3. Data Merging
- **Script:** `merge.py`
- **Process:** Concatenate multiple CSV files
- **Features:** Duplicate removal, date validation

#### 4. Social Media Transformation
- **Process:** Wide to long format transformation
- **Method:** `pd.melt()`
- **Result:** One row per tweet

#### 5. Missing Value Imputation
- **Strategy:** Time-series aware (forward fill, backward fill, interpolation)
- **Fallback:** Median imputation

#### 6. Feature Engineering
- **Categories:** Temporal, weather-derived, social, interactions, lags
- **Total:** 23 new features

#### 7. Data Integration
- **Method:** Left join on date
- **Aggregation:** Daily tweet statistics
- **Feature Extraction:** Keyword counting

---

## Dependencies & Tools

### Python Packages

**Core Data Processing:**
- `pandas>=2.3.3`: Data manipulation and analysis
- `numpy>=2.3.4`: Numerical computing

**File Handling:**
- `openpyxl>=3.1.5`: Excel file reading/writing

**Visualization:**
- `matplotlib>=3.10.7`: Plotting and visualization
- `seaborn>=0.13.2`: Statistical visualization

**Machine Learning:**
- `scikit-learn>=1.7.2`: Machine learning utilities (StandardScaler)
- `scipy>=1.16.3`: Scientific computing and statistics

**Development:**
- `jupyter>=1.1.1`: Interactive notebook environment
- `ipykernel>=7.1.0`: Jupyter kernel

**Utilities:**
- `requests>=2.32.5`: HTTP library (if needed for API calls)

### Development Environment

- **Python Version:** >=3.12
- **Package Manager:** uv (based on `uv.lock` file)
- **Notebook Environment:** Jupyter

### Tools Used

1. **Jupyter Notebooks:** Interactive development and analysis
2. **Pandas:** Data manipulation and analysis
3. **Matplotlib/Seaborn:** Visualization
4. **Excel Files:** Raw data source
5. **CSV Files:** Normalized data format

---

## Conclusion

This project successfully demonstrates a complete data wrangling pipeline for integrating climate and social media data. Key achievements include:

1. **Robust Data Processing:** Handled inconsistent file formats and structures
2. **Comprehensive Cleaning:** Reduced missing values from 11 to 0 using time-series aware methods
3. **Advanced Feature Engineering:** Created 23 new features from 15 original features
4. **Successful Integration:** Merged climate and social media data on temporal basis
5. **Insightful Analysis:** Identified patterns and correlations between weather and social discourse

The project provides a foundation for further analysis, including:
- Predictive modeling for flood risk
- Social media sentiment analysis
- Weather pattern forecasting
- Public awareness studies

### Future Enhancements

1. **Extended Time Period:** Include full year data (currently focused on Jan-Feb)
2. **Advanced NLP:** Sentiment analysis of tweets
3. **Machine Learning Models:** Predict flood risk or social media activity
4. **Real-time Integration:** Automated data collection pipeline
5. **Geographic Analysis:** Include location data from tweets
6. **Weather Forecasting:** Integrate forecast data for predictive analysis

---

## Appendix

### Data Dictionary

#### Climate Variables

| Variable | Description | Unit | Type |
|----------|-------------|------|------|
| TANGGAL | Date | DD-MM-YYYY | Date |
| TN | Minimum Temperature | °C | Numeric |
| TX | Maximum Temperature | °C | Numeric |
| TAVG | Average Temperature | °C | Numeric |
| RH_AVG | Average Relative Humidity | % | Numeric |
| RR | Rainfall | mm | Numeric |
| SS | Sunshine Duration | hours | Numeric |
| FF_X | Maximum Wind Speed | m/s | Numeric |
| DDD_X | Wind Direction (Max) | degrees | Numeric |
| FF_AVG | Average Wind Speed | m/s | Numeric |
| DDD_CAR | Wind Direction Category | C/E/N/S/W | Categorical |

#### Social Media Variables

| Variable | Description | Type |
|----------|-------------|------|
| TANGGAL | Date | Date |
| tweet_id | Tweet identifier | String |
| tweet_text | Tweet content | String |
| tweet_count | Number of tweets per day | Numeric |
| hujan_mention | Count of "hujan" mentions | Numeric |
| banjir_mention | Count of "banjir" mentions | Numeric |
| macet_mention | Count of "macet" mentions | Numeric |

### Code Snippets

#### Data Loading
```python
# Climate data
df_iklim = pd.read_csv('../../data/normalize/iklim_surabaya_2023.csv')
df_iklim['TANGGAL'] = pd.to_datetime(df_iklim['TANGGAL'], format='%d-%m-%Y')

# Social media data
df_tweets = pd.read_csv('../../data/normalize/tweets_normalized.csv')
df_tweets['TANGGAL'] = pd.to_datetime(df_tweets['TANGGAL'], format='%Y-%m-%d')
```

#### Missing Value Handling
```python
# Time-series aware imputation
for col in numeric_cols:
    df[col] = df[col].ffill().bfill().interpolate(method='linear')
    if df[col].isnull().sum() > 0:
        df[col].fillna(df[col].median(), inplace=True)
```

#### Feature Engineering Example
```python
# Temperature range
df['temp_range'] = df['TX'] - df['TN']

# Flood risk score
df['flood_risk_score'] = (
    (df['RR'] > 20).astype(int) * 3 +
    (df['rainfall_3day'] > 50).astype(int) * 2 +
    (df['banjir_mention'] > 0).astype(int) * 1
)
```

---
