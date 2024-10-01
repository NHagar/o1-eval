import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd

# --- Data Load and Clean ---

# Load the CSV file into a DataFrame
file_path = "./data/collisions.csv"
df = pd.read_csv(file_path)

# Remove rows with missing values in the BOROUGH column
df_cleaned = df.dropna(subset=["BOROUGH"])

# Remove duplicates if necessary
df_cleaned = df_cleaned.drop_duplicates()

# Ensure borough names are uppercase (could be redundant but ensures uniformity)
df_cleaned["BOROUGH"] = df_cleaned["BOROUGH"].str.upper()

# --- Data Aggregation ---

# Count the number of collisions per borough
borough_crash_counts = (
    df_cleaned.groupby("BOROUGH")["COLLISION_ID"].count().reset_index()
)
borough_crash_counts.rename(columns={"COLLISION_ID": "Collision_Count"}, inplace=True)

# --- Visualization ---

# Load a shapefile of the borough boundaries for visualization
# Ensure the file exists and replace 'boroughs.geojson' with your actual file
boroughs_geojson = "./data/boroughs.geojson"
gdf_boroughs = gpd.read_file(boroughs_geojson)

# Merge the collision counts with the geographical data
gdf_merged = gdf_boroughs.set_index("name").join(
    borough_crash_counts.set_index("BOROUGH"), how="left"
)

# Plot the map
fig, ax = plt.subplots(1, 1, figsize=(12, 8))
gdf_merged.plot(
    column="Collision_Count",
    cmap="OrRd",
    linewidth=0.8,
    ax=ax,
    edgecolor="0.8",
    legend=True,
)

# Add a title and labels
plt.title("Number of Collisions in Each Borough")
plt.xlabel("Longitude")
plt.ylabel("Latitude")

# Show the plot
plt.show()
