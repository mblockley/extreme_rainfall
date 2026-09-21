import pandas as pd
import numpy as np
import pymannkendall as mk

df = pd.read_csv("datasets/all_rain.csv")

df["time"] = pd.to_datetime(df["time"])
df["date"] = df["time"].dt.floor("D")


## Create Man-Kendall trend analysis
def run_mk(series):
  """Runs Mann-Kendall Test and returns the result"""
  # remove missing values
  series = series.dropna()
  
  #Man-Kendall needs at least two obseervations to continue
  if len(series) < 2:
    return {
      "trend": "insufficient data",
      "p_value": np.nan,
      "kendall_tau": np.nan,
      "sen_slope": np.nan
    }
  
  result = mk.original_test(series)
  
  return {
    "trend": result.trend,
    "p_value": result.p,
    "kendall_tau": result.Tau,
    "sen_slope": result.slope
  }
  
all_results = []

for station, station_df in df.groupby("station"):
  ## Create daily rainfall
  daily = (
    station_df
    .groupby("date")["rainfall"]
    .sum()
    .reset_index()
    )

  daily["year"] = daily["date"].dt.year

  ## Create annual total rainfall

  annual_total = (
      daily
      .groupby("year")["rainfall"]
      .sum()
  )

  ## Create annual maximum daily rainfall
  annual_max = (
      daily
      .groupby("year")["rainfall"]
      .max()
  )

  ## Extreme rainfall threshold
  
  rainy_days = daily.loc[
    daily["rainfall"] >= 1.0,
    "rainfall"
  ]
  
  if len(rainy_days) == 0:
    continue

  threshold = np.percentile(rainy_days, 95)
  
  extreme = daily[daily["rainfall"] > threshold].copy()
  
  extreme["year"] = extreme["date"].dt.year


  ## number of extreme days

  annual_extreme_days = (
    extreme
    .groupby("year")
    .size()
    .reindex(annual_total.index, fill_value=0)
  )


  ## Run the Man-Kendall tests


  metrics = {
    "annual_total_rainfall": annual_total,
    "annual_max_daily_rainfall": annual_max,
    "annual_extreme_days": annual_extreme_days,
    }

  for metric, series in metrics.items():
    result = run_mk(series)
  
    all_results.append({
      "station": station,
      "metric": metric,
      "threshold_mm": threshold,
      "n_years": len(series),
      "trend": result["trend"],
      "p_value": result["p_value"],
      "kendall_tau": result["kendall_tau"],
      "sen_slope": result["sen_slope"],
      "significant_0.05": result["p_value"] < 0.05
    })

## save the results

results_df = pd.DataFrame(all_results)
results_df.to_csv(
  "outputs/mann_kendall_results.csv",
  index=False
)
print(results_df)

