import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
from geodatasets import get_path

path_to_file = get_path("nybb")

# Step 1: Load the Data
file_path = "./data/collisions.csv"
data = pd.read_csv(file_path)

# Step 2: Examine the Data
print("Data Preview:")
print(data.head())

# Step 3: Check for Missing Values
print("\nMissing Values:")
print(data.isnull().sum())

# Step 4: Data Type Verification
print("\nData Types:")
print(data.dtypes)

# Step 5: Clean the 'BOROUGH' Column
# Remove leading/trailing whitespace and convert to uppercase for consistency
if "BOROUGH" in data.columns:
    data["BOROUGH"] = data["BOROUGH"].str.strip().str.upper()

# Step 6: Handle Missing Values
# Drop rows where 'BOROUGH' is missing as they cannot be analyzed
data = data.dropna(subset=["BOROUGH"])

# Step 7: Count the Number of Collisions in Each Borough
borough_collision_counts = data["BOROUGH"].value_counts().reset_index()
borough_collision_counts.columns = ["BOROUGH", "NUMBER_OF_COLLISIONS"]

# Step 8: Load Borough GeoJSON/Shapefile
boroughs_geo = gpd.read_file(path_to_file)  # Adjust this path as necessary

# Step 9: Merge Collision Counts with Borough Geometry
merged = boroughs_geo.set_index("BoroName").join(
    borough_collision_counts.set_index("BOROUGH")
)

# Step 10: Plotting
fig, ax = plt.subplots(1, 1, figsize=(10, 8))
merged.boundary.plot(ax=ax, color="black", linewidth=1)  # Plot the boundaries
merged.plot(
    column="NUMBER_OF_COLLISIONS",
    ax=ax,
    legend=True,
    legend_kwds={
        "label": "Number of Collisions by Borough",
        "orientation": "horizontal",
    },
    cmap="OrRd",
    missing_kwds={"color": "lightgrey"},
)  # Color categories

# Set title and labels
plt.title("Number of Collisions in Each Borough in NYC")
plt.axis("off")  # Hide the axis
plt.show()
