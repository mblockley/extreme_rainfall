# Station data availability timeline - extreme_rainfall
# Reads datasets/station_metadata.csv (run metadata_table.py first)

library(readr)
library(dplyr)
library(ggplot2)

stations <- read_csv("datasets/station_metadata.csv") %>%
  mutate(
    record_start = as.Date(record_start),
    record_end   = as.Date(record_end),
    label = paste0(format(record_start, "%Y"), "-", format(record_end, "%Y"),
                   "  (", round(as.numeric(record_end - record_start) / 365.25), " years)"),
    station_name = reorder(paste0(station_name, " [", provider, "]"),
                           -as.numeric(record_start))
  ) %>%
  filter(!is.na(record_start), !is.na(record_end))

p <- ggplot(stations) +
  geom_segment(aes(x = record_start, xend = record_end,
                   y = station_name, yend = station_name, colour = provider),
               linewidth = 5, lineend = "round") +
  geom_text(aes(x = record_end, y = station_name, label = label),
            hjust = -0.08, size = 2.7, colour = "grey") +
  scale_colour_manual(values = c(FENZ = "blue", ECAN = "red", NIWA = "purple")) +
  scale_x_date(expand = expansion(mult = c(0.02, 0.20))) +
  labs(title = "Rain gauge data timeline",
       x = NULL, y = NULL, colour = "Provider") +
  theme_minimal(base_size = 11) +
  theme(panel.grid.major.y = element_blank())

ggsave("outputs/station_timeline.png", p, width = 10, height = 6, dpi = 300, bg = "white")

