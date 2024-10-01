import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
from geodatasets import get_path

path_to_file = get_path("nybb")

# Load the collision data
collisions_df = pd.read_csv("./data/collisions.csv")

# Count the number of collisions per borough
borough_collision_counts = collisions_df["BOROUGH"].value_counts().reset_index()
borough_collision_counts.columns = ["BOROUGH", "COLLISION_COUNT"]

# Load a map of New York City boroughs
nyc_boroughs = gpd.read_file(path_to_file)

# Merge the collision counts with the NYC map
nyc_boroughs = nyc_boroughs.rename(columns={"BoroName": "BOROUGH"})
merged = nyc_boroughs.merge(borough_collision_counts, on="BOROUGH", how="left")

# Fill NaN values with 0 (in case a borough has no recorded collisions)
merged["COLLISION_COUNT"] = merged["COLLISION_COUNT"].fillna(0)

# Plot the figure
fig, ax = plt.subplots(1, 1, figsize=(12, 12))
merged.plot(
    column="COLLISION_COUNT",
    ax=ax,
    legend=True,
    legend_kwds={
        "label": "Number of Collisions by Borough",
        "orientation": "horizontal",
    },
    cmap="OrRd",
)

# Set axis title and plot title
ax.set_title("Number of Collisions in New York City Boroughs", fontsize=15)
ax.set_axis_off()  # Optional to turn off the axis

# Show the plot
plt.show()
