import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
from geodatasets import get_path

path_to_file = get_path("nybb")

# Load the collision data
collision_data = pd.read_csv("./data/collisions.csv")

# Count collisions per borough
borough_collision_counts = collision_data["BOROUGH"].value_counts().reset_index()
borough_collision_counts.columns = ["BOROUGH", "COLLISION_COUNT"]

# Load the NYC boroughs shapefile (assuming a local or accessible GeoJSON of NYC boroughs)
nyc_boroughs = gpd.read_file(path_to_file)  # Adjust the path accordingly

# Merge collision counts with borough shapes
nyc_boroughs = nyc_boroughs.merge(
    borough_collision_counts, left_on="BoroName", right_on="BOROUGH", how="left"
)

# Plotting
fig, ax = plt.subplots(1, 1, figsize=(10, 10))
nyc_boroughs.boundary.plot(ax=ax, linewidth=1, color="black")
nyc_boroughs.plot(
    column="COLLISION_COUNT",
    ax=ax,
    legend=True,
    legend_kwds={
        "label": "Number of Collisions by Borough",
        "orientation": "horizontal",
    },
    cmap="OrRd",
    missing_kwds={"color": "lightgrey"},
)
plt.title("Number of Collisions in New York City by Borough")
plt.axis("off")
plt.show()
