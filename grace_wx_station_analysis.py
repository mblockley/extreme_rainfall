import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

station_name = "Halswell at Coopers Knob"


## 1. Load Station metadata
metadata = pd.read_csv("datasets/station_metadata.csv")

station_info = metadata[
    (metadata["station_name"] == station_name) &
    (metadata["provider"] == "ECAN")
].iloc[0]

file_path = "datasets/" + station_info["source_file"]


## 2. Load dataset
rain = pd.read_csv(file_path)
rain["time"] = pd.to_datetime(rain["time"])

# How much data do we have, and over what time period?
print("Station                :", station_name)
print("DateTime column type   :", rain["time"].dtype)
print("Number of observations :", len(rain))
print("First observation      :", rain["time"].min().date())
print("Last observation       :", rain["time"].max().date())

## 3. Select station data
coopers = rain.copy()
print("Number of observations :", len(rain))
print("First day      :", rain["time"].min().date())
print("Last day       :", rain["time"].max().date())

# Add a "year" column — we'll use it later to look at trends over time.
coopers["year"] = coopers["time"].dt.year


## 4. Plot hourly rainfall

# Draw the rainfall over the whole period, so we can SEE the spiky big hours.
plt.figure(figsize=(10, 4))

plt.plot(
    coopers["time"],
    coopers["precipitation"]
)

plt.title("Hourly rainfall at Halswell at Coopers Knob")
plt.xlabel("Year")
plt.ylabel("Rainfall (mm)")

plt.savefig("outputs/ECAN_coopers/coopers_timeseries.png")
plt.show()
plt.close()


## 5. Calculate daily rainfall

coopers["date"] = coopers["time"].dt.date

# create daily rainfall totals
daily = (
    coopers
    .groupby("date")["precipitation"]
    .sum()
    .reset_index()
)

daily["year"] = pd.to_datetime(daily["date"]).dt.year


## 6. Find exteme rainfall days

# Keeping only the days where it actually rained (1mm or more).
rainy_days = daily[daily["precipitation"] >= 1.0]["precipitation"]

# The cut-off ("threshold") is the 95th percentile of those rainy days 
threshold = np.percentile(rainy_days, 95)

print(f"There were {len(rainy_days)} rainy days.")
print(f"Our 'extreme' cut-off is {threshold:.1f} mm.")
print(f"So any day with more than {threshold:.1f} mm of rain counts as extreme.")

# Pull out the extreme days - the ones above our cut-off.
extreme = daily[daily["precipitation"] > threshold]

print(f"We found {len(extreme)} extreme days out of {len(coopers)} total days.")
extreme[["date", "precipitation"]].head()


## 7. Plot extreme rainfall days
plt.figure(figsize=(10, 4))

plt.hist(
    extreme["precipitation"],
    bins=20,
    color="tomato",
    edgecolor="white"
)

plt.title("How big were the extreme rainfall days?")
plt.xlabel("Rainfall (mm)")
plt.ylabel("Number of days")

plt.savefig("outputs/ECAN_coopers/coopers_extreme_histogram.png")
plt.show()
plt.close()

## 7. Fit the Generalised Pareto Distribution

# Most extreme days are just above the cut-off, and a few are MUCH bigger.
# That long tail to the right is what we want to describe with a curve.


# We fit the curve to how far each extreme day is ABOVE the cut-off.
# (This "amount above the cut-off" is what the GPD describes.)
amount_above = extreme["precipitation"] - threshold

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

plt.savefig("outputs/ECAN_coopers/coopers_real_extreme_hours.png")
plt.show()
plt.close()

## 10. Plot how often extreme days occur

n_years = coopers["year"].nunique()
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

plt.savefig("outputs/ECAN_coopers/coopers_extreme_days_each_year.png")
plt.show()  
plt.close()
