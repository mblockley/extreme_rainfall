import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import expon
import os


# CHANGE THESE THREE LINES FOR EACH STATION

file_name = "ECAN_McQueens_Valley.csv"
station_name = "ECAN – McQueens Valley"
rain_column = "precipitation"

#CHANGE THESE PATHS

data_dir = r"C:\Users\aiswa\OneDrive\ERA5\ECAN Stations" #That was just the paths on my system
plots_dir = r"C:\Users\aiswa\OneDrive\ERA5\ECAN Stations\plots"

os.makedirs(plots_dir, exist_ok=True)

file_path = os.path.join(data_dir, file_name)


# LOAD DATA

df = pd.read_csv(file_path, parse_dates=["time"], index_col="time")


# DAILY CONVERSION (IMPORTANT)

daily = df[rain_column].resample('D').sum()


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

season_labels = daily.index.month.map(nz_season)

# EXTREME THRESHOLD (DAILY)

threshold = daily.quantile(0.95)
extremes = daily[daily > threshold]
extreme_seasons = extremes.index.month.map(nz_season)

base = file_name.replace(".csv", "")

# 1. ANNUAL RAINFALL (LINE GRAPH)

annual = daily.resample('Y').sum()

plt.figure(figsize=(14,5))
plt.plot(annual.index.year, annual.values, color='#4C72B0', linewidth=2)
plt.title(f"Annual Rainfall – {station_name}", fontsize=16)
plt.xlabel("Year")
plt.ylabel("Total Rainfall (mm)")
plt.grid(alpha=0.25)
plt.tight_layout()
plt.savefig(os.path.join(plots_dir, f"{base}_annual_rainfall.png"))
plt.close()

# 2. EXTREME DAYS PER YEAR (LINE GRAPH)

extreme_counts = extremes.resample('Y').count()

plt.figure(figsize=(14,5))
plt.plot(extreme_counts.index.year, extreme_counts.values,
         color='#C44E52', linewidth=2, marker='o')
plt.title(f"Extreme Days per Year – {station_name}", fontsize=16)
plt.xlabel("Year")
plt.ylabel("Number of Extreme Days")
plt.grid(alpha=0.25)
plt.tight_layout()
plt.savefig(os.path.join(plots_dir, f"{base}_extreme_days_each_year.png"))
plt.close()

# 3. AVERAGE RAINFALL BY SEASON (NZ SEASONS)

season_df = pd.DataFrame({"rain": daily, "season": season_labels})
season_avg = season_df.groupby("season").mean()

plt.figure(figsize=(10,5))
plt.bar(season_avg.index, season_avg["rain"], color='#55A868', alpha=0.85)
plt.title(f"Average Rainfall by Season – {station_name}", fontsize=16)
plt.xlabel("Season")
plt.ylabel("Average Daily Rainfall (mm)")
plt.grid(axis='y', alpha=0.25)
plt.tight_layout()
plt.savefig(os.path.join(plots_dir, f"{base}_avg_rainfall_by_season.png"))
plt.close()

# 4. EXTREME DAYS BY SEASON (NZ SEASONS)

extreme_season_df = pd.DataFrame({"rain": extremes, "season": extreme_seasons})
extreme_season_counts = extreme_season_df.groupby("season").count()

plt.figure(figsize=(10,5))
plt.bar(extreme_season_counts.index, extreme_season_counts["rain"],
        color='#8172B2', alpha=0.85)
plt.title(f"Extreme Days by Season – {station_name}", fontsize=16)
plt.xlabel("Season")
plt.ylabel("Number of Extreme Days")
plt.grid(axis='y', alpha=0.25)
plt.tight_layout()
plt.savefig(os.path.join(plots_dir, f"{base}_extreme_days_by_season.png"))
plt.close()

# 5. HOW BIG WERE THE EXTREME RAINFALL DAYS?

plt.hist(extremes.values, bins=20, color='#E17C05', alpha=0.8, edgecolor='black')
plt.title(f"Extreme Rainfall Amounts – {station_name}", fontsize=16)
plt.xlabel("Extreme Rainfall (mm)")
plt.ylabel("Number of Extreme Days")
plt.grid(alpha=0.25)
plt.tight_layout()
plt.savefig(os.path.join(plots_dir, f"{base}_extreme_sizes.png"))
plt.close()

# 6. HOW COMMON IS RAINFALL ABOVE THE CUTOFF? (FITTED CURVE)

x = extremes.values
bins = np.linspace(min(x), max(x), 20)

loc, scale = expon.fit(x)
curve_x = np.linspace(min(x), max(x), 200)
curve_y = expon.pdf(curve_x, loc=loc, scale=scale)

plt.figure(figsize=(10,5))
plt.hist(x, bins=bins, density=True, alpha=0.6, color='#64B5CD', edgecolor='black')
plt.plot(curve_x, curve_y, color='#D1495B', linewidth=2)
plt.title(f"Rainfall Above Threshold – Real vs Fitted Curve\n{station_name}", fontsize=16)
plt.xlabel("Rainfall Above Threshold (mm)")
plt.ylabel("Probability Density (How Common)")
plt.grid(alpha=0.25)
plt.tight_layout()
plt.savefig(os.path.join(plots_dir, f"{base}_extreme_fitted_curve.png"))
plt.close()

# 7. TIMESERIES RAINFALL VS YEAR (DAILY)

plt.figure(figsize=(14,5))
plt.plot(daily.index, daily.values, color='#64B5CD', linewidth=1.2)
plt.axhline(threshold, color='#D1495B', linestyle='--', linewidth=1.5)
plt.title(f"Daily Rainfall – {station_name}", fontsize=16)
plt.xlabel("Year")
plt.ylabel("Rainfall (mm)")
plt.grid(alpha=0.25)
plt.tight_layout()
plt.savefig(os.path.join(plots_dir, f"{base}_timeseries.png"))
plt.close()

print(f"PLOTS GENERATED{station_name}")
