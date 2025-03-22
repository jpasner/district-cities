import geopandas as gpd
import pandas as pd

# Load city geolocation data from 2023_Gaz_place_national.txt
cities_geo = pd.read_csv('~/gitHub/district-cities/data/2023_Gaz_place_national.txt', sep='\t', dtype={'GEOID': str})

# Print column names to verify correct column names
print("Cities Geo Columns:", cities_geo.columns)

# Ensure correct column selection
actual_columns = cities_geo.columns.str.upper()

lat_col = next((col for col in cities_geo.columns if 'LAT' in col.upper()), None)
lon_col = next((col for col in cities_geo.columns if 'LONG' in col.upper()), None)

if lat_col and lon_col:
    print(f"Using columns: {lon_col} and {lat_col} for longitude and latitude")
else:
    raise KeyError("Could not find latitude/longitude columns in city geolocation file.")

# Rename columns if necessary
cities_geo.rename(columns={lon_col: 'INTPTLONG', lat_col: 'INTPTLAT', 'NAME': 'city_name', 'USPS': 'state'}, inplace=True)

# Remove " CDP" from city names to ensure consistency
cities_geo['city_name'] = cities_geo['city_name'].str.replace(r' CDP$', '', regex=True).str.strip()

# Select only available columns
selected_columns = ['city_name', 'state', 'ALAND_SQMI', 'AWATER_SQMI', 'INTPTLAT', 'INTPTLONG']
selected_columns = [col for col in selected_columns if col in cities_geo.columns]

cities_geo = cities_geo[selected_columns]

# Load city population estimates from SUB-IP-EST2023-POP.xlsx
city_population = pd.read_excel('~/gitHub/district-cities/data/SUB-IP-EST2023-POP.xlsx')

# Extract city and state from 'Geographic Area'
city_population[['city_name', 'state_name']] = city_population['Geographic Area'].str.rsplit(',', n=1, expand=True)
city_population['city_name'] = city_population['city_name'].str.strip()
city_population['state_name'] = city_population['state_name'].str.strip()

# Dictionary mapping full state names to abbreviations
state_abbreviations = {
    'Alabama': 'AL', 'Alaska': 'AK', 'Arizona': 'AZ', 'Arkansas': 'AR', 'California': 'CA',
    'Colorado': 'CO', 'Connecticut': 'CT', 'Delaware': 'DE', 'Florida': 'FL', 'Georgia': 'GA',
    'Hawaii': 'HI', 'Idaho': 'ID', 'Illinois': 'IL', 'Indiana': 'IN', 'Iowa': 'IA',
    'Kansas': 'KS', 'Kentucky': 'KY', 'Louisiana': 'LA', 'Maine': 'ME', 'Maryland': 'MD',
    'Massachusetts': 'MA', 'Michigan': 'MI', 'Minnesota': 'MN', 'Mississippi': 'MS', 'Missouri': 'MO',
    'Montana': 'MT', 'Nebraska': 'NE', 'Nevada': 'NV', 'New Hampshire': 'NH', 'New Jersey': 'NJ',
    'New Mexico': 'NM', 'New York': 'NY', 'North Carolina': 'NC', 'North Dakota': 'ND', 'Ohio': 'OH',
    'Oklahoma': 'OK', 'Oregon': 'OR', 'Pennsylvania': 'PA', 'Rhode Island': 'RI', 'South Carolina': 'SC',
    'South Dakota': 'SD', 'Tennessee': 'TN', 'Texas': 'TX', 'Utah': 'UT', 'Vermont': 'VT',
    'Virginia': 'VA', 'Washington': 'WA', 'West Virginia': 'WV', 'Wisconsin': 'WI', 'Wyoming': 'WY'
}

# Convert full state names to abbreviations
city_population['state'] = city_population['state_name'].map(state_abbreviations)

# Merge population data with city geolocations using city_name and state, keeping all cities from city_population
combined_cities = pd.merge(city_population, cities_geo, on=['city_name', 'state'], how='left')

# Save the intermediate output
combined_cities.to_csv('~/gitHub/district-cities/output/combined_cities.csv', index=False)

# Convert the combined DataFrame to a GeoDataFrame
cities_gdf = gpd.GeoDataFrame(combined_cities, 
                              geometry=gpd.points_from_xy(combined_cities.INTPTLONG, combined_cities.INTPTLAT),
                              crs="EPSG:4326")

print("City geolocation and population data merged successfully.")

# Step 2: Add congressional district information from multiple zip files
import glob
import pandas as pd

# Get all .zip files in the data/tiger_cd_shapefiles folder
zip_files = glob.glob("data/tiger_cd_shapefiles/*.zip")
print("Number of zip files:", len(zip_files))

# Create a list to hold each congressional district GeoDataFrame
cd_gdfs = []
for zip_file in zip_files:
    gdf = gpd.read_file(zip_file)
    cd_gdfs.append(gdf)

# Combine all the congressional district shapefiles into one GeoDataFrame
congressional_districts = gpd.GeoDataFrame(pd.concat(cd_gdfs, ignore_index=True), crs=cd_gdfs[0].crs)

# Save the combined congressional districts GeoDataFrame to a new shapefile in a .zip file
output_shp = '~/gitHub/district-cities/data/combined_cd_shapefile/combined_congressional_districts.shp'
congressional_districts.to_file(output_shp)

# Ensure the CRS matches the cities GeoDataFrame
congressional_districts = congressional_districts.to_crs(cities_gdf.crs)

# Perform spatial join to assign congressional district to each city (using 'within' predicate)
cities_with_cd = gpd.sjoin(cities_gdf, congressional_districts, how='left', predicate='within')

# Rename the district name column to 'congressional_district' (assuming the district name is in the 'NAME' column)
cities_with_cd = cities_with_cd.rename(columns={'NAME': 'congressional_district'})

# Save the resulting GeoDataFrame to a new shapefile
output_shp = '~/gitHub/district-cities/output/shapefile/combined_cities_with_cd.shp'
cities_with_cd.to_file(output_shp)

# Save the resulting DataFrame to a new CSV file without the geometry column
output_csv = '~/gitHub/district-cities/output/combined_cities_with_cd.csv'
cities_with_cd.drop(columns='geometry').to_csv(output_csv, index=False)

print("Cities data successfully joined with congressional district information.")