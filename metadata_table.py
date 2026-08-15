"""
METADATA TABLE
"""

import pandas as pd
from pathlib import Path

DATA = Path(__file__).parent / "datasets"


EXTRA = {
    "Bottle Lake":   {"elevation_m": 5,   "zone": "Plains"},
    "Christchurch Aws":     {"elevation_m": 30,  "zone": "Plains"},
    "Diamond Harbour":      {"elevation_m": 235, "zone": "Banks Peninsula"},
    "Diamond Harbour Ews":  {"elevation_m": 124, "zone": "Banks Peninsula"},
    "Early Valley":         {"elevation_m": 306, "zone": "Port Hills"},
    "Godley Head":        {"elevation_m": 141, "zone": "Banks Peninsula"},
    "Lincoln":         {"elevation_m": 16,  "zone": "Plains"},
    "McLeans":         {"elevation_m": 33,  "zone": "Plains"},
    "Motukarara":          {"elevation_m": 20,  "zone": "Plains"},
    "Rangiora":          {"elevation_m": 12,  "zone": "Plains"},
    "Christchurch Aero":    {"elevation_m": 31,  "zone": "Plains"},
    "Christchurch Gardens": {"elevation_m": 12,  "zone": "Plains"},
    "McQueens Valley": {"zone": "Banks Peninsula"},

    # ECAN__________________________________________
    "Banks Peninsula at Kaituna Valley": {"zone": "Banks Peninsula"},
    "Barrys Bay at Hilltop":              {"zone": "Banks Peninsula"},
    "Christchurch, Kyle St EWS":         {"zone": "Plains"},
    "Cust Main Drain at Threlkelds Road": {"zone": "Plains"},
    "Halswell at Coopers Knob":        {"zone": "Port Hills"},
    "Halswell at Ryans Bge":             {"zone": "Plains"},
    "Halswell at Tai Tapu":           {"zone": "Plains"},
    "Heathcote at Hoon Hay":         {"zone": "Port Hills"},  
    "Hukahuka at Summit":            {"zone": "Port Hills"},
    "Kaituna Valley at Tophouse":     {"zone": "Banks Peninsula"},
    "Kaituna at Kaituna Valley Rd":    {"zone": "Banks Peninsula"},
    "Lincoln, Broadfield Ews":      {"zone": "Plains"},
    "Waimakariri at Kainga Yard":     {"zone": "Plains"},
}

DUPLICATE_WATCH = [
    ("Lincoln", "Lincoln, Broadfield Ews"),      # FENZ vs ECAN, ~100 m apart
    ("Christchurch Aws", "Christchurch Aero"),   # FENZ vs NIWA/ECAN, flagged previously
]




NIWA = {
    "chch_aero_rain_daily.csv":    {"name": "Christchurch Aero",    "id": "?????",
                                    "lat": -43.4894, "lon": 172.5325},
    "chch_gardens_rain_daily.csv": {"name": "Christchurch Gardens", "id": "????",
                                    "lat": -43.5310, "lon": 172.6200},
}



def time_span(df):
    """returns first and last observation dates"""
    candidates = [
        c for c in df.columns
        if ("time" in c.lower() or "date" in c.lower())
        and c.lower() != "modified_date"
    ]
    if not candidates:
        return "", ""
    t = pd.to_datetime(df[candidates[0]], errors="coerce").dropna()
    if t.empty:
        return "", ""
    return t.min().date(), t.max().date()


rows = []

# ---- FENZ files ----------------------------------------------------------
for path in sorted(DATA.glob("FENZ_*.csv")):
    df = pd.read_csv(path)
    first = df.iloc[0]
    start, end = time_span(df)
    has_time = start != ""   
    rows.append({
        "station_name": first["name"],
        "provider": "FENZ",
        "station_id": first["ref"],
        "lat": first["lat"],
        "lon": first["lon"],
        "resolution": "sub-daily" if has_time else "unknown",
        "record_start": start,
        "record_end": end,
        "n_records": len(df),
        "source_file": path.name,
        "notes": "" if has_time else "no timestamp column - needs re-export",
    })


# ---- ECAN files -----------------------------------------------------------
for path in sorted(DATA.glob("ECAN_*.csv")):
    df = pd.read_csv(path)
    first = df.iloc[0]
    start, end = time_span(df)
    has_time = start != ""
    rows.append({
        "station_name": first["name"],
        "provider": "ECAN",
        "station_id": first["ref"],
        "lat": first["lat"],
        "lon": first["lon"],
        "elevation_m": first["altitude"],
        "resolution": "sub-daily" if has_time else "unknown",
        "record_start": start,
        "record_end": end,
        "n_records": len(df),
        "source_file": path.name,
        "notes": "" if has_time else "no timestamp column - needs re-export",
    })


# ---- NIWA files ----------------------------------------------------------
for filename, info in NIWA.items():
    path = DATA / filename
    if not path.exists():
        continue
    df = pd.read_csv(path)
    time = pd.to_datetime(df["Observation time UTC"], errors="coerce")
    rows.append({
        "station_name": info["name"],
        "provider": "NIWA",
        "station_id": info["id"],
        "lat": info["lat"],
        "lon": info["lon"],
        "resolution": "daily",
        "record_start": time.min().date(),
        "record_end": time.max().date(),
        "n_records": len(df),
        "source_file": path.name,
        "notes": "daily total is the 24 h to 09:00 NZST",
    })

# ---- add elevation _________________
out = pd.DataFrame(rows)

out["zone"] = out["station_name"].map(lambda n: EXTRA.get(n, {}).get("zone"))

if "elevation_m" not in out.columns:
    out["elevation_m"] = pd.NA

out["elevation_m"] = out.apply(
    lambda r: r["elevation_m"] if pd.notna(r["elevation_m"])
    else EXTRA.get(r["station_name"], {}).get("elevation_m"),
    axis=1,
)

out = out[["station_name", "provider", "station_id", "lat", "lon", "elevation_m",
           "zone", "resolution", "record_start", "record_end", "n_records",
           "source_file", "notes"]]

out.to_csv(DATA / "station_metadata.csv", index=False)
print(out.to_string(index=False))
print(f"\nSaved {len(out)} stations to {DATA / 'station_metadata.csv'}")