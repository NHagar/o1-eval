import matplotlib.pyplot as plt
import pandas as pd
from mpl_toolkits.basemap import Basemap

# Load data
df = pd.read_csv("./data/collisions.csv")

# Group by borough and count collisions
borough_counts = df["BOROUGH"].value_counts()

# Create a map of New York City
fig, ax = plt.subplots(figsize=(10, 8))
m = Basemap(
    llcrnrlon=-74.1, llcrnrlat=40.6, urcrnrlon=-72.9, urcrnrlat=41.2, resolution="l"
)
m.drawmapboundary(fill_color="#66B3FF")

# Add borough names
boroughs = ["Manhattan", "Queens", "The Bronx", "Staten Island"]
x, y = m(-74.05, 40.7), m(-73.9, 41.1)
for i, borough in enumerate(boroughs):
    m.plot(x[i], y[i], marker="o", markersize=10, color="red")
    plt.text(x[i] + 0.01, y[i], borough)

# Add county names
counties = ["New York County", "Queens County", "Bronx County"]
x, y = m(-74.05, 40.7), m(-73.9, 41.1)
for i, county in enumerate(counties):
    m.plot(x[i], y[i], marker="o", markersize=10, color="green")
    plt.text(x[i] + 0.01, y[i], county)

# Plot boroughs by number of collisions
x, y = m(df["LONGITUDE"].iloc[0], df["LATITUDE"].iloc[0])
borough_counts.plot(kind="bar", ax=ax, x_compat=True)
for i, (borough, count) in enumerate(borough_counts.items()):
    x, y = m(-74.05 + (i % 4) * 0.25, 40.7 + (i // 4) * 0.25)
    m.plot(x, y, marker="o", markersize=10, color="blue")
    plt.text(x + 0.01, y, borough, rotation=45)

plt.title("Number of Collisions by Borough in New York City")
plt.xlabel("Borough")
plt.ylabel("Count")

plt.show()
