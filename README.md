# District Cities Data Processor

This project processes and merges U.S. city geolocation and population data.

## Script: `combine.py`

The `combine.py` script performs the following steps:

1. Loads U.S. city geolocation data from a text file.
2. Cleans and standardizes city names and state abbreviations.
3. Loads U.S. city population estimates from an Excel file.
4. Extracts city and state information from the population data.
5. Merges the geolocation and population data on city name and state.
6. Saves the combined data to a CSV file.
7. Converts the result into a GeoDataFrame for spatial analysis.

The output CSV and GeoDataFrame can be used for further geospatial processing or visualization.