import io

import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
import requests

# Step 1: Load collision data
collision_data = pd.read_csv("./data/collisions.csv", usecols=["BOROUGH"])

# Remove entries with missing or unknown boroughs
collision_data = collision_data[collision_data["BOROUGH"].notna()]
collision_data = collision_data[collision_data["BOROUGH"] != "UNKNOWN"]

# Step 2: Aggregate number of collisions per borough
collision_counts = collision_data["BOROUGH"].value_counts().reset_index()
collision_counts.columns = ["Borough", "Collision_Count"]

# Step 3: Load NYC borough boundaries using GeoJSON
# NYC borough boundaries GeoJSON URL
geojson_url = (
    "https://raw.githubusercontent.com/dwillis/nyc-maps/master/boroughs.geojson"
)

# Fetch the GeoJSON data
geojson_response = requests.get(geojson_url)
if geojson_response.status_code != 200:
    raise ValueError("Could not retrieve GeoJSON data for NYC boroughs.")

boroughs_geo = gpd.read_file(io.StringIO(geojson_response.text))

# Ensure the borough names match between datasets
boroughs_geo["BoroName"] = boroughs_geo["BoroName"].str.upper()
collision_counts["Borough"] = collision_counts["Borough"].str.upper()

# Step 4: Merge collision counts with geographical data
merged_data = boroughs_geo.merge(
    collision_counts, left_on="BoroName", right_on="Borough"
)

# Step 5: Plot the choropleth map
fig, ax = plt.subplots(1, 1, figsize=(10, 10))
merged_data.plot(
    column="Collision_Count",
    ax=ax,
    legend=True,
    cmap="OrRd",
    edgecolor="black",
    linewidth=0.8,
    legend_kwds={"label": "Number of Collisions", "orientation": "horizontal"},
)


# Add titles and labels
ax.set_title("Number of Traffic Collisions per Borough in New York City", fontsize=16)
ax.axis("off")

# Annotate borough names
for idx, row in merged_data.iterrows():
    plt.annotate(
        text=row["BoroName"],
        xy=(row["geometry"].centroid.x, row["geometry"].centroid.y),
        horizontalalignment="center",
        fontsize=12,
        fontweight="bold",
    )

plt.tight_layout()
plt.show()
