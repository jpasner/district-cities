# District Cities Data Processor

This project processes and merges U.S. city geolocation and population data, and enhances it with congressional district information for spatial analysis.

## Script: `combine.py`

The `combine.py` script performs the following steps:

1. **Load Geolocation Data:**
   - [2023 National Gazetteer Places File](https://www2.census.gov/geo/docs/maps-data/data/gazetteer/2023_Gazetteer/2023_Gaz_place_national.zip)
   - Reads U.S. city geolocation data from a text file.
   - Contains 32,329 rows of cities

2. **Clean and Standardize Data:**
   - Cleans and standardizes city names and state abbreviations.

3. **Load Population Estimates:**
   - [2023 Census file of Incorporated Places](https://www2.census.gov/programs-surveys/popest/tables/2020-2023/cities/totals/SUB-IP-EST2023-POP.xlsx)
   - Loads U.S. city population estimates from an Excel file.
   - Contains 19,484 City Population rows

4. **Extract City and State Information:**
   - Extracts relevant city and state data from the population file.

5. **Merge Datasets:**
   - Merges the geolocation and population data based on city name and state.

6. **Match and Validate City/State Combinations:**
   - Processes 19,484 records from the 2023 Census file of Incorporated Places to find 19,473 unique city/state combinations.
   - Matches these against the 2023 National Gazetteer Places files to extract geographic information.
   - **Notes:** 
     - 22 city/state combinations appear as duplicates (e.g., two towns named Reno in Texas); these may be due to data quality issues.
     - The population file appears to be missing smaller incorporated places (e.g. Penn Valley, California)

7. **Integrate Congressional District Data:**
   - [2023 | 118th Congress Districts Line Layer](https://www2.census.gov/geo/tiger/TIGER2023/CD/)
   - **NOTE:** Created `download_data.py` script to automate download
   - Reads multiple congressional district shapefiles from .zip files located in the `data/tiger_cd_shapefiles` folder.
   - Combines these shapefiles and performs a spatial join with the merged cities data to assign each city its corresponding congressional district.

8. **Output Final Data:**
   - Saves the combined data (including congressional district information) to a CSV file.

9. **Create a GeoDataFrame:**
   - Converts the final CSV output into a GeoDataFrame for further spatial analysis or visualization.

The output CSV and GeoDataFrame serve as key resources for subsequent geospatial processing and visualization.