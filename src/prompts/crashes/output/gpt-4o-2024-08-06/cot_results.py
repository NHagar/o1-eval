import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
from geodatasets import get_path

# Step 1: Load collision data
collisions_df = pd.read_csv("./data/collisions.csv")

# Step 2: Ensure we're only dealing with entries that have a borough listed
collisions_df = collisions_df.dropna(subset=["BOROUGH"])

# Step 3: Count the collisions per borough
borough_collisions = collisions_df["BOROUGH"].value_counts().reset_index()
borough_collisions.columns = ["BOROUGH", "COLLISIONS"]

# Step 4: Load NYC borough shapes using geopandas (this requires having a GeoJSON file of NYC boroughs)
nyc_boroughs = gpd.read_file(get_path("nybb"))
nyc_boroughs = nyc_boroughs.to_crs(epsg=4326)  # reprojecting to a common system
nyc_boroughs["BoroName"] = nyc_boroughs[
    "BoroName"
].str.upper()  # Match casing on borough names

# Step 5: Merge the collisions data with the GeoDataFrame
nyc_boroughs = nyc_boroughs.merge(
    borough_collisions, left_on="BoroName", right_on="BOROUGH", how="left"
)

# Step 6: Plotting the map
fig, ax = plt.subplots(1, 1, figsize=(10, 10))
nyc_boroughs.boundary.plot(ax=ax, linewidth=1)
nyc_boroughs.plot(
    column="COLLISIONS",
    ax=ax,
    legend=True,
    legend_kwds={
        "label": "Number of Collisions by Borough",
        "orientation": "horizontal",
    },
)

# Add titles and labels
plt.title("Number of Collisions by Borough in New York City")
plt.xlabel("Longitude")
plt.ylabel("Latitude")

plt.show()
