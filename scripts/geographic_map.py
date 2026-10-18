import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs

# Load ERA5 MSLP dataset
mslp = xr.open_dataset("data_stream-oper_stepType-instant.nc")

# Select the day you want
day = "2026-02-16"   # change to 2026-02-15 if needed

# Extract all hours for that day
mslp_day = mslp.sel(valid_time=mslp.valid_time.dt.date == day)

# Loop through each hour
for t in mslp_day.valid_time.values:

    mslp_t = mslp.sel(valid_time=t).msl

    fig = plt.figure(figsize=(16, 8))
    ax = plt.axes(projection=ccrs.PlateCarree(central_longitude=180))
    ax.set_extent([140, 190, -50, -20], crs=ccrs.PlateCarree())
    ax.coastlines(resolution='10m', linewidth=1.0, color='black')

    # Plot MSLP
    mslp_t.plot(
        ax=ax,
        transform=ccrs.PlateCarree(),
        cmap='viridis',
        cbar_kwargs={'label':'MSLP (Pa)', 'shrink':0.75, 'pad':0.03}
    )

    ax.set_title(f"ERA5 MSLP — {str(t)}", fontsize=15)
    plt.savefig(f"mslp_{str(t).replace(':','')}.png", dpi=200, bbox_inches="tight")
    plt.show()


