from tethysts import Tethys
import pandas as pd
from pathlib import Path

DATA = Path(r"P:\My Documents\DATA309\extreme_rainfall\datasets")

ts = Tethys()

datasets = ts.datasets

#-------------------------
#Finding FENZ Dataset
#-------------------------

fenz_dataset = [
    ds for ds in datasets
    if ds["parameter"] == "precipitation"
    and ds["product_code"] == "raw_data"
    and ds["frequency_interval"] == "1H"
    and ds["owner"] == "FENZ"
][0]

fenz_dataset_id = fenz_dataset["dataset_id"]

print("\nFENZ dataset found:")
print(fenz_dataset_id)
print(fenz_dataset)

fenz_stations = ts.get_stations(fenz_dataset_id)

print("\nNumber of FENZ stations:")
print(len(fenz_stations))

fenz_station_ids = {
    "Early Valley": "26a6a359a4b6b7ce56d52927",
    "McLeans": "0854405926e3bc7e27602c86",
    "Bottle Lake Forest": "47feb204580757d31df499e7",
    "Rangiora": "66d18bb25c45e9098c0e53fc",
    "Diamond Harbour": "2f68c4bb65f8d832dfb10a92",
    "Motukarara": "1dd0e5e15552fce719028dbd",
    "Godley Head": "ed0e55004a0a9db0e74576f4",
    "Diamond Harbour Ews": "75be053664250d909eb1a545",
    "Lincoln": "1f6c8d6162818ba620783392",
    "Christchurch Aws": "932777fadc0490b29639d18c"
}

#----------------------
#download fenz data
#----------------------

for name, station_id in fenz_station_ids.items():

    print("----------------------------------------")
    print(f"Downloading: FENZ - {name}")

    results = ts.get_results(
        fenz_dataset_id,
        station_id
    )

    df = results.to_dataframe()

    # Turn the time index into a normal column
    df = df.reset_index()

    # Check timestamp
    if "time" in df.columns:

        df["time"] = pd.to_datetime(
            df["time"],
            errors="coerce"
        )

        print("Timestamp column found.")
        print("First timestamp:", df["time"].min())
        print("Last timestamp:", df["time"].max())

    else:

        print("WARNING: No time column found.")

    # Create filename
    filename = (
        "FENZ_"
        + name.replace(" ", "_")
        + ".csv"
    )

    filepath = DATA / filename

    df.to_csv(
        filepath,
        index=False
    )

    print(f"Saved: {filepath}")
    print(f"Rows: {len(df)}")
