# Download ECAN Rainfall - extreme_rainfall

from tethysts import Tethys
import pandas as pd
from pathlib import Path

DATA = Path(r"P:\My Documents\DATA309\extreme_rainfall\datasets")

remotes = [
    {
        "bucket": "ecan-env-monitoring",
        "public_url": "https://b2.tethys-ts.xyz/file/",
        "version": 4
    }
]

ts = Tethys(remotes)

datasets = ts.datasets

#------------------------
#FINDING ECAN DATASET
#------------------------

ecan_dataset = [
    ds for ds in datasets
    if ds["parameter"] == "precipitation"
    and ds["product_code"] == "quality_controlled_data"
    and ds["frequency_interval"] == "1H"
    and ds["owner"] == "Environment Canterbury"
][0]

ecan_dataset_id = ecan_dataset["dataset_id"]

print("ECan dataset found:")
print(ecan_dataset_id)

ecan_stations = ts.get_stations(ecan_dataset_id)


ecan_names = [
    "Halswell at Tai Tapu",
    "Kaituna Valley at Tophouse",
    "Cust Main Drain at Threlkelds Road",
    "Kaituna at Kaituna Valley Rd",
    "Christchurch Aero",
    "Hukahuka at Summit",
    "Lincoln, Broadfield Ews",
    "Heathcote at Hoon Hay",
    "Christchurch, Kyle St EWS",
    "Waimakariri at Kainga Yard",
    "Banks Peninsula at Kaituna Valley",
    "Barrys Bay at Hilltop",
    "Halswell at Coopers Knob",
    "Christchurch Gardens",
    "Halswell at Ryans Bge",
    "McQueens Valley"
]

#-------------------------
#Downloading Ecan datasets
#--------------------------

def download_station(ts, dataset_id, station, provider):

    name = station["name"]

    print("----------------------------------------")
    print(f"Downloading: {provider} - {name}")

    results = ts.get_results(
        dataset_id,
        station["station_id"]
    )

    df = results.to_dataframe()

    # Turn the time index a normal column
    df = df.reset_index()

    # Create safe filename
    filename = (
        provider
        + "_"
        + name.replace(" ", "_")
        .replace(",", "")
        .replace("/", "_")
        + ".csv"
    )

    filepath = DATA / filename

    df.to_csv(
        filepath,
        index=False
    )

    print(f"Saved: {filepath}")
    print(f"Rows: {len(df)}")
    
for name in ecan_names:

    station = next(
        s for s in ecan_stations
        if s["name"] == name
    )

    download_station(
        ts,
        ecan_dataset_id,
        station,
        "ECAN"
    )


print("\nECan download complete.")
