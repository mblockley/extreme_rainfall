import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs

# ---------------------------------------------------------
# Load ERA5 total precipitation dataset
# ---------------------------------------------------------
tp = xr.open_dataset("data_stream-oper_stepType-accum.nc")

# ---------------------------------------------------------
# Times to plot (−18h, peak hour, +6h)
# ---------------------------------------------------------
times_to_plot = [
    "2026-02-15T13:00",   # -18 hours
    "2026-02-16T07:00",   # peak hour
    "2026-02-16T13:00"    # +6 hours
]

# ---------------------------------------------------------
# Loop through each synoptic time
# ---------------------------------------------------------
for t in times_to_plot:

    # Convert m → mm
    tp_t = tp.sel(valid_time=t).tp * 1000

    fig = plt.figure(figsize=(16, 8))
    ax = plt.axes(projection=ccrs.PlateCarree(central_longitude=180))
    ax.set_extent([140, 190, -50, -20], crs=ccrs.PlateCarree())
    ax.coastlines(resolution='10m', linewidth=1.0, color='black')

    # ---------------------------------------------------------
    # Precipitation shading only (now in mm)
    # ---------------------------------------------------------
    tp_t.plot(
        ax=ax,
        transform=ccrs.PlateCarree(),
        cmap='Blues',
        vmin=0,
        vmax=12,   # 0.012 m = 12 mm
        cbar_kwargs={'label':'Total Precipitation (mm)', 'shrink':0.75, 'pad':0.03}
    )

    # ---------------------------------------------------------
    # Title
    # ---------------------------------------------------------
    ax.set_title(f"ERA5 Total Precipitation — {t}", fontsize=15)

    # ---------------------------------------------------------
    # Layout
    # ---------------------------------------------------------
    fig.subplots_adjust(left=0.05, right=0.85, top=0.92, bottom=0.08)

    # ---------------------------------------------------------
    # Save figure
    # ---------------------------------------------------------
    plt.savefig(f"era5_precip_{t.replace(':','')}.png", dpi=200, bbox_inches="tight")
    plt.show()
