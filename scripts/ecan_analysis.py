"""
Basic Rainfall Analysis Script
Purpose:
    - Load hourly + daily rainfall data
    - Extra hourly plot included when hourly data exists
Notes:
    - Make sure the CSV has columns:
        "Observation time UTC"  → timestamp
        "Rainfall [mm]"         → rainfall values
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import expon
import os


# USER SETTINGS (CHANGE THESE)

station_name = "Christchurch Gardens"

hourly_file = r"C:\Users\aiswa\OneDrive\ERA5\ECAN Stations\chch_aero_rain_hourly.csv"
daily_file  = r"C:\Users\aiswa\OneDrive\ERA5\ECAN Stations\chch_gardens_rain_daily.csv"

time_column = "Observation time UTC"
rain_column = "Rainfall [mm]"

# Output folder
output_dir = f"outputs/{station_name}"
os.makedirs(output_dir, exist_ok=True)


# LOAD DATA
# Hourly data (if available)
try:
    df_hourly = pd.read_csv(hourly_file, parse_dates=[time_column])
    df_hourly = df_hourly.set_index(time_column)
    hourly_available = True
except Exception:
    print("Hourly file not found or unreadable → skipping hourly plot.")
    hourly_available = False

# Daily data (main dataset)
df_daily = pd.read_csv(daily_file, parse_dates=[time_column])
df_daily = df_daily.set_index(time_column)

daily = df_daily[rain_column]


# EXTRA: HOURLY TIME SERIES

if hourly_available:
    plt.figure(figsize=(12,4))
    plt.plot(df_hourly.index, df_hourly[rain_column], color="#4C72B0")
    plt.title(f"{station_name} – Hourly Rainfall")
    plt.xlabel("Time")
    plt.ylabel("Rainfall (mm)")
    plt.tight_layout()
    plt.savefig(f"{output_dir}/hourly_timeseries.png")
    plt.close()


# PLOT 1: DAILY TIME SERIES

plt.figure(figsize=(12,4))
plt.plot(daily.index, daily, color="#4C72B0")
plt.title(f"{station_name} – Daily Rainfall")
plt.xlabel("Date")
plt.ylabel("Rainfall (mm)")
plt.tight_layout()
plt.savefig(f"{output_dir}/daily_timeseries.png")
plt.close()


# PLOT 2: DAILY HISTOGRAM

plt.figure(figsize=(6,4))
plt.hist(daily, bins=50, color="#55A868")
plt.title(f"{station_name} – Daily Rainfall Distribution")
plt.xlabel("Rainfall (mm)")
plt.ylabel("Frequency")
plt.tight_layout()
plt.savefig(f"{output_dir}/daily_histogram.png")
plt.close()


# EXTREME EVENTS (95th percentile)

threshold = daily.quantile(0.95)
extremes = daily[daily > threshold]


# PLOT 3: EXTREME HISTOGRAM

plt.figure(figsize=(6,4))
plt.hist(extremes, bins=30, color="#C44E52")
plt.title(f"{station_name} – Extreme Rainfall Days")
plt.xlabel("Rainfall (mm)")
plt.ylabel("Count")
plt.tight_layout()
plt.savefig(f"{output_dir}/extreme_histogram.png")
plt.close()


# PLOT 4: EXTREME FITTED CURVE

plt.figure(figsize=(6,4))
plt.hist(extremes, bins=30, density=True, color="#C44E52")

try:
    loc, scale = expon.fit(extremes)
    curve_x = np.linspace(min(extremes), max(extremes), 200)
    curve_y = expon.pdf(curve_x, loc=loc, scale=scale)
    plt.plot(curve_x, curve_y, color="#D1495B", linewidth=2)
except Exception:
    print("Not enough extreme data to fit curve.")

plt.title(f"{station_name} – Extreme Rainfall (Fitted Curve)")
plt.xlabel("Rainfall (mm)")
plt.ylabel("Density")
plt.tight_layout()
plt.savefig(f"{output_dir}/extreme_curve.png")
plt.close()


# NZ SEASONS

def nz_season(month):
    if month in [12, 1, 2]:
        return "Summer"
    elif month in [3, 4, 5]:
        return "Autumn"
    elif month in [6, 7, 8]:
        return "Winter"
    else:
        return "Spring"


# PLOT 5: SEASONAL TOTALS

season_labels = daily.index.month.map(nz_season)
season_df = pd.DataFrame({"rain": daily, "season": season_labels})
season_totals = season_df.groupby("season").sum()

plt.figure(figsize=(6,4))
plt.bar(season_totals.index, season_totals["rain"], color="#4C72B0")
plt.title(f"{station_name} – Seasonal Rainfall Totals")
plt.ylabel("Total Rainfall (mm)")
plt.tight_layout()
plt.savefig(f"{output_dir}/season_totals.png")
plt.close()


# PLOT 6: ANNUAL TOTALS

annual_totals = daily.resample("Y").sum()

plt.figure(figsize=(12,4))
plt.plot(annual_totals.index.year, annual_totals.values, color="#4C72B0")
plt.title(f"{station_name} – Annual Rainfall Totals")
plt.xlabel("Year")
plt.ylabel("Total Rainfall (mm)")
plt.tight_layout()
plt.savefig(f"{output_dir}/annual_totals.png")
plt.close()


# PLOT 7: TREND LINE

years = annual_totals.index.year
values = annual_totals.values

coef = np.polyfit(years, values, 1)
trend = np.poly1d(coef)

plt.figure(figsize=(12,4))
plt.plot(years, values, color="#4C72B0", label="Annual Rainfall")
plt.plot(years, trend(years), color="#D1495B", linewidth=2, label="Trend")
plt.title(f"{station_name} – Rainfall Trend")
plt.xlabel("Year")
plt.ylabel("Total Rainfall (mm)")
plt.legend()
plt.tight_layout()
plt.savefig(f"{output_dir}/trend.png")
plt.close()

print("plots generated for", station_name)
