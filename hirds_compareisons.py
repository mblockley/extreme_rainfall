"""
Compares a station's own extreme rainfall days against what hirds predicted


at the top u need to change STATION_NAME / PROVIDER / HIRDS_ZIP for each station that u want to run analysis on.
"""

import pandas as pd
import zipfile
import matplotlib.pyplot as plt

DATA = "datasets"
DURATION = "24h"   


#the filnames in hirds didnt match the ones in station_metadata hand to define them first
HIRDS_ZIP_LOOKUP = {
    ("Bottle Lake", "FENZ"): "Bottle Lake.zip",
    ("Christchurch Aws", "FENZ"): "Christchurch Aws.zip",
    ("Diamond Harbour", "FENZ"): "Diamond Harbour.zip",
    ("Diamond Harbour Ews", "FENZ"): "Diamond Harbour.zip",
    ("Early Valley", "FENZ"): "Early Valley.zip",
    ("Godley Head", "FENZ"): "Godley Head.zip",
    ("Lincoln", "FENZ"): "Lincoln.zip",
    ("McLeans", "FENZ"): "McLeans.zip",
    ("Motukarara", "FENZ"): "Motukarara.zip",
    ("Rangiora", "FENZ"): "Rangiora.zip",
    ("Banks Peninsula at Kaituna Valley", "ECAN"): "Banks Peninsula at Kaituna Valley.zip",
    ("Barrys Bay at Hilltop", "ECAN"): "Barrys Bay at Hilltop.zip",
    ("Christchurch Aero", "ECAN"): "Christchurch Aero.zip",
    ("Christchurch Gardens", "ECAN"): "Christchurch Gardens.zip",
    ("Christchurch, Kyle St EWS", "ECAN"): "Christchurch, Kyle St EWS.zip",
    ("Cust Main Drain at Threlkelds Road", "ECAN"): "Threlkelds Road.zip",
    ("Halswell at Coopers Knob", "ECAN"): "Halswell at Coopers Knop.zip",  
    ("Halswell at Ryans Bge", "ECAN"): "Halswell at Ryans Bge.zip",
    ("Halswell at Tai Tapu", "ECAN"): "Halswell at Tai tapu.zip",         
    ("Heathcote at Hoon Hay", "ECAN"): "Heathcote at Hoonhay.zip",
    ("Hukahuka at Summit", "ECAN"): "Hukahuka at Summit.zip",
    ("Kaituna at Kaituna Valley Rd", "ECAN"): "Kaituna at Kaituna valley Road.zip",
    ("Kaituna Valley at Tophouse", "ECAN"): "Kaituna Valley.zip",
    ("Lincoln, Broadfield Ews", "ECAN"): "Lincoln, Broadfield Ews.zip",
    ("McQueens Valley", "ECAN"): "McQueens Valley.zip",
    ("Waimakariri at Kainga Yard", "ECAN"): "Waimakiriri at Kainga Yard.zip",  
    ("Christchurch Aero", "NIWA"): "Christchurch Aero.zip",
    ("Christchurch Gardens", "NIWA"): "Christchurch Gardens(NIWA).zip",
    ("Akaroa EWS", "NIWA"): "Akaroa EWS.zip",
}

for (STATION_NAME, PROVIDER), HIRDS_ZIP in HIRDS_ZIP_LOOKUP.items():


    #get the thresholds 10 and 100 year rain thresholds for particualar station.
    def get_hirds_thresholds(hirds_zip_name, duration="24h"):
        zip_path = f"{DATA}/HIRDS/{hirds_zip_name}"
        with zipfile.ZipFile(zip_path) as z:
            with z.open("depth_report.csv") as f:
                lines = [line.decode("utf-8") for line in f.readlines()]

            
            start = next(i for i, line in enumerate(lines) if "Historical Data" in line) + 1
            header = lines[start].strip().split(",")
            dur_col = header.index(duration)
            ari_col = header.index("ARI")

        thresholds = {}
        for line in lines[start + 1: start + 13]:  
            parts = line.strip().split(",")
            if len(parts) < len(header):
                break
            thresholds[float(parts[ari_col])] = float(parts[dur_col])
        return thresholds


    thresholds = get_hirds_thresholds(HIRDS_ZIP, DURATION)
    threshold_10yr = thresholds[10.0]
    threshold_100yr = thresholds[100.0]


    print(f" HIRDS 24hr rainfall for  {STATION_NAME} : 10-yr ARI:  {threshold_10yr} mm, 100-yr ARI:  {threshold_100yr} mm")



    #get the stations own data
    metadata = pd.read_csv(f"{DATA}/station_metadata.csv")
    station_info = metadata[
        (metadata["station_name"] == STATION_NAME) & (metadata["provider"] == PROVIDER)
    ].iloc[0]
    file_path = f"{DATA}/{station_info['source_file']}"

      

    try:
        rain = pd.read_csv(file_path)
    except FileNotFoundError:
        print("coudlnt find the file")
        continue


    #differant files/stations have differant timestamps so change all 3 of the data prociders to a 24hr total
    if PROVIDER == "NIWA":
        rain["ts"] = pd.to_datetime(rain["Observation time UTC"])
        value_col = "Rainfall [mm]"
        boundary_shift_hours = 21
    else:
        rain["ts"] = pd.to_datetime(rain["time"])
        value_col = "precipitation"
        boundary_shift_hours = 9

    shifted = rain["ts"] - pd.Timedelta(hours=boundary_shift_hours)
    rain["date"] = shifted.dt.floor("D")
    daily = rain.groupby("date", as_index=False)[value_col].sum()
    daily = daily.rename(columns={value_col: "rain_mm"})



    #show what days exceeded the prediected 10/100 year predictions
    exceed_10yr = daily[daily["rain_mm"] >= threshold_10yr].sort_values("rain_mm", ascending=False)
    exceed_100yr = daily[daily["rain_mm"] >= threshold_100yr].sort_values("rain_mm", ascending=False)

    print(f"\nDays exceeding the 10-yr depth: {len(exceed_10yr)}")
    print(f"Days exceeding the 100-yr depth: {len(exceed_100yr)}")


    
    #plot
    plt.figure(figsize=(10, 4))
    plt.plot(daily["date"], daily["rain_mm"], color="blue", linewidth=0.7)
    plt.axhline(threshold_10yr, color="orange", linestyle="--", label=f"10-yr")
    plt.axhline(threshold_100yr, color="red", linestyle="--", label=f"100-yr")
    for _, r in exceed_10yr.iterrows():
        plt.annotate(r["date"].strftime("%d %b %Y"), (r["date"], r["rain_mm"]),
                    textcoords="offset points", xytext=(0, 8), ha="center",
                    fontsize=7, rotation=45)
    plt.title(f"{STATION_NAME} daily rainfall vs HIRDS return periods")
    plt.xlabel("Date")
    plt.ylabel("Daily rainfall (mm)")
    plt.legend()
    plt.tight_layout()
    plt.savefig(f"outputs/HIRDS/{PROVIDER}_hirds_{STATION_NAME.lower().replace(' ', '_')}.png")
    
    plt.close()
