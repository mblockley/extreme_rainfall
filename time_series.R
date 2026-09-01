# Plot a time series for NIWA - extreme_rainfall
# Reads datasets/station_metadata.csv (run metadata_table.py first)

library(readr)
library(dplyr)
library(ggplot2)

#------------------NIWA Datasets -----------------------------------------------
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

#------------------ECAN Datasets -----------------------------------------------
banks_peninsula <- read_csv("datasets/ECAN_Banks_Peninsula_at_Kaituna_Valley.csv") |>
  mutate(time = `time`,
         station = "Banks Peninsula at Kaituna Valley",
         provider = "ECAN",
         rainfall = `precipitation`) |>
  select(time, rainfall, station, provider)

barrys_bay <- read_csv("datasets/ECAN_Barrys_Bay_at_Hilltop.csv") |>
  mutate(time = `time`,
         station = "Barrys Bay at Hilltop",
         provider = "ECAN",
         rainfall = `precipitation`) |>
  select(time, rainfall, station, provider)

chch_aero <- read_csv("datasets/ECAN_Christchurch_Aero.csv") |>
  mutate(time = `time`,
         station = "Christchurch Aero",
         provider = "ECAN",
         rainfall = `precipitation`) |>
  select(time, rainfall, station, provider)

chch_gardens <- read_csv("datasets/ECAN_Christchurch_Gardens.csv") |>
  mutate(time = `time`,
         station = "Christchurch Gardens",
         provider = "ECAN",
         rainfall = `precipitation`) |>
  select(time, rainfall, station, provider)

kyle_st <- read_csv("datasets/ECAN_Christchurch_Kyle_St_EWS.csv") |>
  mutate(time = `time`,
         station = "Christchurch, Kyle St EWS",
         provider = "ECAN",
         rainfall = `precipitation`) |>
  select(time, rainfall, station, provider)

cust_main_drain <- read_csv("datasets/ECAN_Cust_Main_Drain_at_Threlkelds_Road.csv") |>
  mutate(time = `time`,
         station = "Cust Main Drain at Threlkelds Road",
         provider = "ECAN",
         rainfall = `precipitation`) |>
  select(time, rainfall, station, provider)

coopers_knob <- read_csv("datasets/ECAN_Halswell_at_Coopers_Knob.csv") |>
  mutate(time = `time`,
         station = "Halswell at Coopers Knob",
         provider = "ECAN",
         rainfall = `precipitation`) |>
  select(time, rainfall, station, provider)

ryans_bge <- read_csv("datasets/ECAN_Halswell_at_Ryans_Bge.csv") |>
  mutate(time = `time`,
         station = "Halswell at Ryans Bge",
         provider = "ECAN",
         rainfall = `precipitation`) |>
  select(time, rainfall, station, provider)

tai_tapu <- read_csv("datasets/ECAN_Halswell_at_Tai_Tapu.csv") |>
  mutate(time = `time`,
         station = "Halswell at Tai Tapu",
         provider = "ECAN",
         rainfall = `precipitation`) |>
  select(time, rainfall, station, provider)

hoon_hay <- read_csv("datasets/ECAN_Heathcote_at_Hoon_Hay.csv") |>
  mutate(time = `time`,
         station = "Heathcote at Hoon Hay",
         provider = "ECAN",
         rainfall = `precipitation`) |>
  select(time, rainfall, station, provider)

summit <- read_csv("datasets/ECAN_Hukahuka_at_Summit.csv") |>
  mutate(time = `time`,
         station = "Hukahuka at Summit",
         provider = "ECAN",
         rainfall = `precipitation`) |>
  select(time, rainfall, station, provider)

kaituna_valley_rd <- read_csv("datasets/ECAN_Kaituna_at_Kaituna_valley_Rd.csv") |>
  mutate(time = `time`,
         station = "Kaituna at Kaituna Valley Rd",
         provider = "ECAN",
         rainfall = `precipitation`) |>
  select(time, rainfall, station, provider)

tophouse <- read_csv("datasets/ECAN_Kaituna_Valley_at_Tophouse.csv") |>
  mutate(time = `time`,
         station = "Kaituna Valley at Tophouse",
         provider = "ECAN",
         rainfall = `precipitation`) |>
  select(time, rainfall, station, provider)

lincoln_broadfield <- read_csv("datasets/ECAN_Lincoln_Broadfield_EWS.csv") |>
  mutate(time = `time`,
         station = "Lincoln, Broadfield Ews",
         provider = "ECAN",
         rainfall = `precipitation`) |>
  select(time, rainfall, station, provider)

mcqueens <- read_csv("datasets/ECAN_McQueens_Valley.csv") |>
  mutate(time = `time`,
         station = "McQueens Valley",
         provider = "ECAN",
         rainfall = `precipitation`) |>
  select(time, rainfall, station, provider)

kainga_yard <- read_csv("datasets/ECAN_Waimakariri_at_Kainga_Yard.csv") |>
  mutate(time = `time`,
         station = "Waimakariri at Kainga Yard",
         provider = "ECAN",
         rainfall = `precipitation`) |>
  select(time, rainfall, station, provider)

#------------------FENZ Datasets -----------------------------------------------

bottle_lake <- read_csv("datasets/FENZ_Bottle_Lake_Forest.csv") |>
  mutate(time = `time`,
         station = "Bottle Lake",
         provider = "FENZ",
         rainfall = `precipitation`) |>
  select(time, rainfall, station, provider)

chch_aws <- read_csv("datasets/FENZ_Christchurch_AWS.csv") |>
  mutate(time = `time`,
         station = "Christchurch Aws",
         provider = "FENZ",
         rainfall = `precipitation`) |>
  select(time, rainfall, station, provider)

diamond_harbour_ews <- read_csv("datasets/FENZ_Diamond_Harbour_EWS.csv") |>
  mutate(time = `time`,
         station = "Diamond Harbour Ews",
         provider = "FENZ",
         rainfall = `precipitation`) |>
  select(time, rainfall, station, provider)

diamond_harbour <- read_csv("datasets/FENZ_Diamond_Harbour.csv") |>
  mutate(time = `time`,
         station = "Diamond Harbour",
         provider = "FENZ",
         rainfall = `precipitation`) |>
  select(time, rainfall, station, provider)

early_valley <- read_csv("datasets/FENZ_Early_Valley.csv") |>
  mutate(time = `time`,
         station = "Early Valley",
         provider = "FENZ",
         rainfall = `precipitation`) |>
  select(time, rainfall, station, provider)

godley_head <- read_csv("datasets/FENZ_Godley_Head.csv") |>
  mutate(time = `time`,
         station = "Godley Head",
         provider = "FENZ",
         rainfall = `precipitation`) |>
  select(time, rainfall, station, provider)

lincoln <- read_csv("datasets/FENZ_Lincoln.csv") |>
  mutate(time = `time`,
         station = "Lincoln",
         provider = "FENZ",
         rainfall = `precipitation`) |>
  select(time, rainfall, station, provider)

mcleans <- read_csv("datasets/FENZ_McLeans.csv") |>
  mutate(time = `time`,
         station = "McLeans",
         provider = "FENZ",
         rainfall = `precipitation`) |>
  select(time, rainfall, station, provider)

motukarara <- read_csv("datasets/FENZ_Motukarara.csv") |>
  mutate(time = `time`,
         station = "Motukarara",
         provider = "FENZ",
         rainfall = `precipitation`) |>
  select(time, rainfall, station, provider)

rangiora <- read_csv("datasets/FENZ_Rangiora.csv") |>
  mutate(time = `time`,
         station = "Rangiora",
         provider = "FENZ",
         rainfall = `precipitation`) |>
  select(time, rainfall, station, provider)

#Combining datasets
all_rain <- bind_rows(aero,gardens,banks_peninsula,barrys_bay,chch_aero, 
                      chch_gardens,kyle_st,cust_main_drain,coopers_knob,ryans_bge,
                      tai_tapu,hoon_hay,summit,kaituna_valley_rd,tophouse,
                      lincoln_broadfield,mcqueens,kainga_yard,bottle_lake,chch_aws,
                      diamond_harbour_ews,diamond_harbour,early_valley,godley_head,
                      lincoln,mcleans,motukarara,rangiora)

ggplot(all_rain, aes(x = time, y = rainfall)) +
  geom_line() +
  labs(
    title = "Rainfall Time Series Across ALL Stations",
    x = "Date",
    y = "Time",
  ) + theme_minimal()

write.csv(all_rain)

#Calculating extreme rainfall separately depending on the zone
metadata <- read_csv("datasets/station_metadata.csv")

all_rain <- all_rain |> 
  left_join(metadata |>
              select(station_name, provider, zone),
            by = c("station" = "station_name", "provider" = "provider"))

  
all_rain |>
  filter(rainfall > 0) |>
  group_by(zone) |>
  summarise(
    p90 = quantile(rainfall, 0.90, na.rm = TRUE),
    p95 = quantile(rainfall, 0.95, na.rm = TRUE),
    p99 = quantile(rainfall, 0.99, na.rm = TRUE),
    max = max(rainfall, na.rm = TRUE)
  )

