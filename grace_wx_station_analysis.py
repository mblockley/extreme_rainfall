import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

rain = pd.read_csv("datasets/all_rain.csv")
metadata = pd.read_csv("datasets/station_metadata.csv")

rain["time"] = pd.to_datetime(rain["time"], utc = True)

print("DateTime column type:", rain["time"].dtype)

rain.head()


## Selecting Coopers Knob
coopers = rain[
    rain["station"] == "Halswell at Coopers Knob"
].copy()

# How much data do we have, and over what time period?
print("Number of days :", len(coopers))
print("First day      :", coopers["time"].min().date())
print("Last day       :", coopers["time"].max().date())

# Add a "year" column — we'll use it later to look at trends over time.
coopers["year"] = coopers["time"].dt.year

# Draw the rainfall over the whole period, so we can SEE the spiky big hours.
plt.figure(figsize=(10, 4))

plt.plot(
    coopers["time"],
    coopers["rainfall"]
)

plt.title("Hourly rainfall at Halswell at Coopers Knob")
plt.xlabel("Year")
plt.ylabel("Rainfall (mm)")

plt.savefig("outputs/ECAN_coopers/coopers_timeseries.png")
plt.show()
plt.close()


## Extreme daily rainfall
coopers["date"] = coopers["time"].dt.date

# create daily rainfall totals
daily = (
    coopers
    .groupby("date")["rainfall"]
    .sum()
    .reset_index()
)

daily["year"] = pd.to_datetime(daily["date"]).dt.year


# Keeping only the days where it actually rained (1mm or more).
rainy_days = daily[daily["rainfall"] >= 1.0]["rainfall"]

# The cut-off ("threshold") is the 95th percentile of those rainy days 
threshold = np.percentile(rainy_days, 95)

print(f"There were {len(rainy_days)} rainy days.")
print(f"Our 'extreme' cut-off is {threshold:.1f} mm.")
print(f"So any day with more than {threshold:.1f} mm of rain counts as extreme.")

# Pull out the extreme days - the ones above our cut-off.
extreme = daily[daily["rainfall"] > threshold]

print(f"We found {len(extreme)} extreme days out of {len(coopers)} total days.")
extreme[["date", "rainfall"]].head()

# Second Figure
plt.figure(figsize=(10, 4))

plt.hist(
    extreme["rainfall"],
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

# Most extreme days are just above the cut-off, and a few are MUCH bigger.
# That long tail to the right is what we want to describe with a curve.


# We fit the curve to how far each extreme day is ABOVE the cut-off.
# (This "amount above the cut-off" is what the GPD describes.)
amount_above = extreme["rainfall"] - threshold

# scipy fits the curve and gives us the shape and scale numbers.
# (floc=0 just tells it to measure from the cut-off, which is what we want.)
shape, loc, scale = stats.genpareto.fit(amount_above, floc=0)

print(f"shape number : {shape:.2f}")
print(f"scale number : {scale:.2f}")
if shape < 0:
    print("The shape is negative, suggesting a natural upper limit to daily rain here.")
else:
    print("The shape is positive, suggesting very large storms are possible.")
    
## Figure 3

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

# How often do extreme days happen, on average per year?
n_years = coopers["year"].nunique()
events_per_year = len(extreme) / n_years
print(f"On average, {events_per_year:.1f} extreme days per year.\n")

# For a few return periods, estimate the rainfall amount using the fitted curve.
for years in [2, 5, 10, 20, 50, 100]:
    # how many extreme events we'd expect in this many years
    n_events = years * events_per_year
    # ask the fitted curve for the size that's exceeded once in that many events
    size = threshold + stats.genpareto.ppf(1 - 1/n_events, shape, loc, scale)
    print(f"1-in-{years:>3}-year storm: about {size:.0f} mm of rain in a day")
    
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
