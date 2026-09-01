import pandas as pd
import matplotlib.pyplot as plt

# ECAN station 

file_path = r"C:\Users\aiswa\OneDrive\ERA5\ECAN Stations\ECAN_Banks_Peninsula_at_Kaituna_Valley.csv"
station_name = "ECAN Banks Peninsula at Kaituna Valley" #Change for different station names
rain_column = "precipitation"

# 1. Load dataset
df = pd.read_csv(file_path, parse_dates=["time"], index_col="time")

# 2. Clean rainfall (remove negatives)
daily = df[rain_column].copy()
daily = daily[daily >= 0]

# 3. Compute 95th percentile threshold
threshold = daily.quantile(0.95)

# 4. Extract extreme days
extremes = daily[daily > threshold]

# 5. Return period calculation
start_date = daily.index[0]
end_date = daily.index[-1]

years = (end_date - start_date).days / 365
n_extreme = len(extremes)

rp_years = years / n_extreme
rp_days = rp_years * 365

print("Station:", station_name)
print("95th percentile threshold:", threshold)
print("Years of data:", years)
print("Number of extreme days:", n_extreme)
print("Return period (years):", rp_years)
print("Return period (days):", rp_days)


# 6. PLOT 1: Daily Rainfall Time Series

plt.figure(figsize=(14,5))
plt.plot(daily.index, daily.values, color='steelblue')
plt.axhline(threshold, color='red', linestyle='--', label='95th percentile threshold')
plt.title(f"Daily Rainfall with Extreme Threshold – {station_name}", fontsize=16)
plt.xlabel("Year")
plt.ylabel("Rainfall (mm)")
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()
plt.show()


# 7. PLOT 2: Extreme Days Per Year (bar chart)

extreme_counts = extremes.resample('Y').count()

plt.figure(figsize=(14,5))
plt.bar(extreme_counts.index.year, extreme_counts.values, color='darkred')
plt.title(f"Number of Extreme Rainfall Days per Year – {station_name}", fontsize=16)
plt.xlabel("Year")
plt.ylabel("Extreme Day Count")
plt.xticks(extreme_counts.index.year, rotation=90)
plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.show()


# 8. PLOT 3: Histogram of Extreme Intensities

plt.figure(figsize=(10,5))
plt.hist(extremes.values, bins=20, color='purple', alpha=0.7)
plt.title(f"Distribution of Extreme Rainfall Intensities – {station_name}", fontsize=16)
plt.xlabel("Rainfall (mm)")
plt.ylabel("Frequency")
plt.grid(alpha=0.3)
plt.tight_layout()
plt.show()
