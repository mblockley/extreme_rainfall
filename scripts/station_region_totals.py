import pandas as pd
import matplotlib.pyplot as plt

# ---------------------------------------------------------
# Load dataset
# ---------------------------------------------------------
df = pd.read_csv("combined_hourly_rainfall.csv")
df["Date"] = pd.to_datetime(df["Date"])

# ---------------------------------------------------------
# Select event date
# ---------------------------------------------------------
event_date = "2026-02-16"
event = df[df["Date"].dt.date == pd.to_datetime(event_date).date()]

# Extract hour
event["Hour"] = event["Date"].dt.hour

# ---------------------------------------------------------
# 1. DAILY TOTALS — STATION
# ---------------------------------------------------------
daily_station = (
    event.groupby("Station")["Rainfall"]
    .sum()
    .reset_index()
)

plt.figure(figsize=(12, 6))
plt.bar(daily_station["Station"], daily_station["Rainfall"], color="steelblue")
plt.title(f"Daily Total Rainfall by Station — {event_date}")
plt.ylabel("Rainfall (mm)")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig("daily_station_totals.png", dpi=200)
plt.show()

# ---------------------------------------------------------
# 2. DAILY TOTALS — REGION
# ---------------------------------------------------------
daily_region = (
    event.groupby("Region")["Rainfall"]
    .sum()
    .reset_index()
)

plt.figure(figsize=(12, 6))
plt.bar(daily_region["Region"], daily_region["Rainfall"], color="seagreen")
plt.title(f"Daily Total Rainfall by Region — {event_date}")
plt.ylabel("Rainfall (mm)")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig("daily_region_totals.png", dpi=200)
plt.show()

# ---------------------------------------------------------
# 3. PEAK HOUR — FIND PEAK HOUR FIRST
# ---------------------------------------------------------
hour_totals = event.groupby("Hour")["Rainfall"].sum()
peak_hour = hour_totals.idxmax()

peak_event = event[event["Hour"] == peak_hour]

# ---------------------------------------------------------
# 4. PEAK HOUR — STATION
# ---------------------------------------------------------
peak_station = (
    peak_event.groupby("Station")["Rainfall"]
    .sum()
    .reset_index()
)

plt.figure(figsize=(12, 6))
plt.bar(peak_station["Station"], peak_station["Rainfall"], color="darkorange")
plt.title(f"Peak Hour Rainfall by Station — {event_date} (Hour {peak_hour}:00)")
plt.ylabel("Rainfall (mm)")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig("peak_station_totals.png", dpi=200)
plt.show()

# ---------------------------------------------------------
# 5. PEAK HOUR — REGION
# ---------------------------------------------------------
peak_region = (
    peak_event.groupby("Region")["Rainfall"]
    .sum()
    .reset_index()
)

plt.figure(figsize=(12, 6))
plt.bar(peak_region["Region"], peak_region["Rainfall"], color="firebrick")
plt.title(f"Peak Hour Rainfall by Region — {event_date} (Hour {peak_hour}:00)")
plt.ylabel("Rainfall (mm)")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig("peak_region_totals.png", dpi=200)
plt.show()
