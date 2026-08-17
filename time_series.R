# Plot a time series for NIWA - extreme_rainfall
# Reads datasets/station_metadata.csv (run metadata_table.py first)

library(readr)
library(dplyr)
library(ggplot2)

#NIWA
aero <- read_csv("datasets/chch_aero_rain_hourly.csv") |>
  mutate(time = `Observation time UTC`,
         station = "Christchurch Aero",
         provider = "NIWA",
         rainfall = `Rainfall [mm]`) |>
  select(time, rainfall, station, provider)

gardens <- read_csv("datasets/chch_gardens_rain_hourly.csv") |>
  mutate(time = `Observation time UTC`,
         station = "Christchurch Gardens",
         provider = "NIWA",
         rainfall = `Rainfall [mm]`) |>
  select(time, rainfall, station, provider)

#Combining datasets
all_rain <- bind_rows(aero, gardens)

ggplot(all_rain, aes(x = time, y = rainfall, colour = station)) +
  geom_line() +
  labs(
    title = "Rainfall Time Series Across NIWA Stations",
    x = "Date",
    y = "Time",
    colour = "Station"
  ) + theme_minimal()



  
