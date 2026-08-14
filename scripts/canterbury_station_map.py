"""
Canterbury weather station spatial map
Reads datasets/station_metadata.csv and produces a basemap plot
of all station locations, coloured by zone.
"""

import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import contextily as cx
from pathlib import Path

DATA = Path("datasets")
OUT = Path("outputs")
OUT.mkdir(exist_ok=True)

# load metadata
df = pd.read_csv(DATA / "station_metadata.csv")

# Build GeoDataFrame from latitude and longitude
gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df["lon"], df["lat"]), crs="EPSG:4326",)

# Convert to Web Mercator as expected by contextily
gdf_web = gdf.to_crs(epsg=3857)

# Plot
fig, ax = plt.subplots(figsize=(9, 9))

zones = gdf_web["zone"].unique()
colors = plt.cm.Set1(range(len(zones)))
zone_color = dict(zip(zones, colors))

for zone in zones:
    subset = gdf_web[gdf_web["zone"] == zone]
    ax.scatter(subset.geometry.x, subset.geometry.y, label=zone, s=80, color=zone_color[zone], edgecolor="black", linewidth=0.6, zorder=3,)

# Label each station
for _, row in gdf_web.iterrows():
    ax.annotate(row["station_name"], (row.geometry.x, row.geometry.y), xytext=(5, 5), textcoords="offset points", fontsize=7, zorder=4,)

# Basemap tiles
cx.add_basemap(ax, source=cx.providers.CartoDB.Positron, zorder=1)

ax.set_title("Canterbury Weather Stations", fontsize=14, fontweight="bold")
ax.legend(title="Zone", loc="upper left", fontsize=9)
ax.set_axis_off()

plt.tight_layout()
outfile = OUT / "canterbury_stations_map.png"
plt.savefig(outfile, dpi=200, bbox_inches="tight")
print(f"Saved map to {outfile}")

plt.show()
