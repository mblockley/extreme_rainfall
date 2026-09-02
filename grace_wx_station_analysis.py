import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

station_name = "Christchurch Gardens"


## 1. Load Station metadata
metadata = pd.read_csv("datasets/station_metadata.csv")

station_info = metadata[
    (metadata["station_name"] == station_name) &
    (metadata["provider"] == "NIWA")
].iloc[0]

file_path = "datasets/" + station_info["source_file"]


## 2. Load dataset
rain = pd.read_csv(file_path)
rain["Observation time UTC"] = pd.to_datetime(rain["Observation time UTC"])

# How much data do we have, and over what time period?
print("Station                :", station_name)
print("DateTime column type   :", rain["Observation time UTC"].dtype)
print("Number of observations :", len(rain))
print("First observation      :", rain["Observation time UTC"].min().date())
print("Last observation       :", rain["Observation time UTC"].max().date())


## 3. Select station data
df = rain.copy()

# Add a "year" column — we'll use it later to look at trends over Observation time UTC.
df["year"] = df["Observation time UTC"].dt.year


## 4. Plot hourly rainfall

# Draw the rainfall over the whole period, so we can SEE the spiky big hours.
plt.figure(figsize=(10, 4))

plt.plot(
    df["Observation time UTC"],
    df["Rainfall [mm]"]
)

plt.title(f"Hourly rainfall at {station_name}")
plt.xlabel("Year")
plt.ylabel("Rainfall (mm)")

plt.savefig("outputs/NIWA_chch_gardens/chch_gardens_timeseries.png")
plt.show()
plt.close()


## 5. Calculate daily rainfall

df["date"] = df["Observation time UTC"].dt.date

# create daily rainfall totals
daily = (
    df
    .groupby("date")["Rainfall [mm]"]
    .sum()
    .reset_index()
)

daily["date"] = pd.to_datetime(daily["date"])
daily["year"] = daily["date"].dt.year
daily["month"] = daily["date"].dt.month

## 6. Plot annual rainfall

annual_rainfall = (
    daily
    .groupby("year")["Rainfall [mm]"]
    .sum()
)

plt.figure(figsize=(10, 4))

plt.plot(
    annual_rainfall.index,
    annual_rainfall.values
)

plt.title(f"Annual rainfall at {station_name}")
plt.xlabel("Year")
plt.ylabel("Annual rainfall (mm)")
plt.grid(True)

plt.savefig("outputs/NIWA_chch_gardens/chch_gardens_annual_rainfall.png")

plt.show()
plt.close()


## 7. Find exteme rainfall days

# Keeping only the days where it actually rained (1mm or more).
rainy_days = daily[daily["Rainfall [mm]"] >= 1.0]["Rainfall [mm]"]

# The cut-off ("threshold") is the 95th percentile of those rainy days 
threshold = np.percentile(rainy_days, 95)

print(f"There were {len(rainy_days)} rainy days.")
print(f"Our 'extreme' cut-off is {threshold:.1f} mm.")
print(f"So any day with more than {threshold:.1f} mm of rain counts as extreme.")

# Pull out the extreme days - the ones above our cut-off.
extreme = daily[daily["Rainfall [mm]"] > threshold]

print(f"We found {len(extreme)} extreme days out of {len(daily)} total days.")
extreme[["date", "Rainfall [mm]"]].head()


## 8. Plot extreme rainfall days
plt.figure(figsize=(10, 4))

plt.hist(
    extreme["Rainfall [mm]"],
    bins=20,
    color="tomato",
    edgecolor="white"
)

plt.title("How big were the extreme rainfall days?")
plt.xlabel("Rainfall (mm)")
plt.ylabel("Number of days")

plt.savefig("outputs/NIWA_chch_gardens/chch_gardens_extreme_histogram.png")
plt.show()
plt.close()
# Most extreme days are just above the cut-off, and a few are MUCH bigger.
# That long tail to the right is what we want to describe with a curve.

## 9. Fit the Generalised Pareto Distribution

# We fit the curve to how far each extreme day is ABOVE the cut-off.
# (This "amount above the cut-off" is what the GPD describes.)
amount_above = extreme["Rainfall [mm]"] - threshold

# scipy fits the curve and gives us the shape and scale numbers.
# (floc=0 just tells it to measure from the cut-off, which is what we want.)
shape, loc, scale = stats.genpareto.fit(amount_above, floc=0)

print(f"shape number : {shape:.2f}")
print(f"scale number : {scale:.2f}")
if shape < 0:
    print("The shape is negative, suggesting a natural upper limit to daily rain here.")
else:
    print("The shape is positive, suggesting very large storms are possible.")
  
    
## Plot the GPD fit

# Let's check the curve actually fits our data.
# We draw the real extreme days (histogram) and the fitted curve on top.
plt.figure(figsize=(10, 4))
plt.hist(amount_above, bins=20, density=True, color="lightblue",
         edgecolor="white", label="real extreme days")

# the fitted GPD curve
x = np.linspace(0, amount_above.max(), 200)
plt.plot(x, stats.genpareto.pdf(x, shape, loc, scale),
         "r-", linewidth=2, label="fitted curve")

plt.title("Does our curve fit the data?")
plt.xlabel("Rainfall above the cut-off (mm)")
plt.ylabel("How common")
plt.legend()

plt.savefig("outputs/NIWA_chch_gardens/chch_gardens_real_extreme_hours.png")
plt.show()
plt.close()

## 10. Calculating extreme days per year

n_years = df["year"].nunique()
events_per_year = len(extreme) / n_years
print(f"On average, {events_per_year:.1f} extreme days per year.\n")


## 11. Calculate return periods

# For a few return periods, estimate the rainfall amount using the fitted curve.
for years in [2, 5, 10, 20, 50, 100]:
    # how many extreme events we'd expect in this many years
    n_events = years * events_per_year
    # ask the fitted curve for the size that's exceeded once in that many events
    size = threshold + stats.genpareto.ppf(1 - 1/n_events, shape, loc, scale)
    print(f"1-in-{years:>3}-year storm: about {size:.0f} mm of rain in a day")
    

## 12. Plot number of extreme days per year

# Count the extreme days in each year.
per_year = extreme.groupby("year").size()

# Draw those counts as bars.
plt.bar(per_year.index, per_year.values, color="steelblue")

plt.title("Number of extreme rainfall days each year")
plt.xlabel("Year")
plt.ylabel("Number of extreme days")
plt.legend()

plt.savefig("outputs/NIWA_chch_gardens/chch_gardens_extreme_days_each_year.png")
plt.show()  
plt.close()


## 13. Fitting seasonal Patterns

daily["season"] = daily["month"].map({
  12: "Summer",
  1: "Summer",
  2: "Summer",
  3: "Autumn",
  4: "Autumn",
  5: "Autumn",
  6: "Winter",
  7: "Winter",
  8: "Winter",
  9: "Spring",
  10: "Spring",
  11: "Spring"
})

extreme = daily[daily["Rainfall [mm]"] > threshold].copy()

seasonal_rainfall = (
    daily
    .groupby("season")["Rainfall [mm]"]
    .mean()
)

print("\nAverage daily rainfall by season:")
print(seasonal_rainfall)


extreme_seasonal_rainfall = (
    extreme
    .groupby("season")
    .size()
)

print("\nExtreme rainfall days by season:")
print(extreme_seasonal_rainfall)


# 14. Plotting seasonal Patterns

# Avg Daily Rainfall
plt.figure(figsize=(10, 4))

plt.bar(seasonal_rainfall.index,seasonal_rainfall.values,color="steelblue")

plt.title(f"Average daily rainfall by season at {station_name}")
plt.xlabel("Season")
plt.ylabel("Average daily rainfall (mm)")

plt.savefig("outputs/NIWA_chch_gardens/chch_gardens_seasonal_rainfall.png")
plt.show()
plt.close()

# Extreme rainfall

plt.figure(figsize=(10, 4))

plt.bar(extreme_seasonal_rainfall.index,extreme_seasonal_rainfall.values,
        color="steelblue")

plt.title(f"Extreme rainfall days by season at {station_name}")
plt.xlabel("Season")
plt.ylabel("Number of extreme days")

plt.savefig("outputs/NIWA_chch_gardens/chch_gardens_extreme_days_by_season.png")
plt.show()
plt.close()

