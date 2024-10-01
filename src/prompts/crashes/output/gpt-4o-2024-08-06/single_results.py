import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
from geodatasets import get_path

path_to_file = get_path("nybb")

# Load the collision data
collisions_df = pd.read_csv("./data/collisions.csv", encoding="latin1")

# Count the number of collisions in each borough
borough_counts = collisions_df["BOROUGH"].value_counts()

# Load a geospatial file of NYC boroughs
# NYC borough shapefiles might be available as part of datasets like the Natural Earth, NYC Open Data, or similar sources
nyc_boroughs = gpd.read_file(path_to_file)

# Ensure the structure of the borough names is consistent across dataframes
nyc_boroughs["BoroName"] = nyc_boroughs["BoroName"].str.upper()

# Merge the geodataframe with the collision data
nyc_boroughs = nyc_boroughs.set_index("BoroName").join(borough_counts).reset_index()

print(nyc_boroughs)

# Plotting the map
fig, ax = plt.subplots(1, 1, figsize=(10, 8))
nyc_boroughs.plot(
    column="BoroName",
    ax=ax,
    legend=True,
    cmap="OrRd",
    missing_kwds={"color": "lightgrey"},
)
ax.set_title("Number of Collisions in Each NYC Borough", fontsize=14)
ax.set_axis_off()
plt.show()
