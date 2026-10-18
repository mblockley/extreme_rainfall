import pandas as pd
import os

# ------------------------------------------------------------
# Load metadata
# ------------------------------------------------------------
meta = pd.read_csv("station_metadata.csv")

combined = []

# ------------------------------------------------------------
# Loop through each station in metadata
# ------------------------------------------------------------
for _, row in meta.iterrows():
    station = row["station_name"]
    provider = row["provider"]
    source_file = row["source_file"]
    zone = row["zone"]
    lat = row["lat"]
    lon = row["lon"]

    path = os.path.join("C:/Users/aiswa/OneDrive/ERA5/ERA5_rainfall/datasets", source_file)

    print(f"Loading {station} ({provider}) from {source_file}")

    # ------------------------------------------------------------
    # FENZ loader
    # ------------------------------------------------------------
    if provider == "FENZ":
        df = pd.read_csv(path)
        # FENZ rainfall column is usually 'precipitation'
        if "precipitation" in df.columns:
            df.rename(columns={"precipitation": "Rainfall"}, inplace=True)
        elif "rainfall" in df.columns:
            df.rename(columns={"rainfall": "Rainfall"}, inplace=True)
        # FENZ timestamp column is usually 'time'
        if "time" in df.columns:
            df.rename(columns={"time": "Date"}, inplace=True)
        elif "Date" not in df.columns:
            print(f"⚠️ No usable date column found in {source_file}")
            continue

    # ------------------------------------------------------------
    # ECAN loader
    # ------------------------------------------------------------
    elif provider == "ECAN":
        df = pd.read_csv(path)
        # Handle different ECAN formats
        if "time" in df.columns:
            df.rename(columns={"time": "Date", "rainfall": "Rainfall"}, inplace=True)
        elif "Date" in df.columns:
            df.rename(columns={"Date": "Date", "rainfall": "Rainfall"}, inplace=True)
        elif "date" in df.columns:
            df.rename(columns={"date": "Date", "rainfall": "Rainfall"}, inplace=True)
        elif "Value" in df.columns:
            df.rename(columns={"Value": "Rainfall"}, inplace=True)
        else:
            print(f"⚠️ No usable date column found in {source_file}")
            continue

    # ------------------------------------------------------------
    # NIWA loader
    # ------------------------------------------------------------
    elif provider == "NIWA":
        df = pd.read_csv(path)
        # Keep only hourly rows
        if "Frequency [D/H]" in df.columns:
            df = df[df["Frequency [D/H]"] == "H"]
        df.rename(columns={
            "Observation time UTC": "Date",
            "Rainfall [mm]": "Rainfall"
        }, inplace=True)

    else:
        print(f"⚠️ Unknown provider for {station}")
        continue

    # ------------------------------------------------------------
    # Standardize columns
    # ------------------------------------------------------------
    df["Station"] = station
    df["Zone"] = zone
    df["Latitude"] = lat
    df["Longitude"] = lon
    df["Provider"] = provider

    # Convert Date
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce", dayfirst=True)
    df = df.dropna(subset=["Date"])

    combined.append(df)

# ------------------------------------------------------------
# Combine all stations
# ------------------------------------------------------------
final = pd.concat(combined, ignore_index=True)

# ------------------------------------------------------------
# Save
# ------------------------------------------------------------
final.to_csv("combined_hourly_rainfall.csv", index=False)

print("✅ Hourly combined dataset saved successfully!")
print(final["Provider"].value_counts())

print("Merge complete!")
print(final["Provider"].value_counts())
