import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd

# Load the dataset
collisions_data = pd.read_csv('./data/collisions.csv')

# Count the number of collisions in each borough
borough_collision_counts = collisions_data['BOROUGH'].value_counts()

# Load NYC boroughs shapefile
nyc_boroughs = gpd.read_file('./data/nyc_boroughs.shp')

# Merging dataframes on boroughs
nyc_boroughs = nyc_boroughs.merge(borough_collision_counts.rename('COLLISION_COUNT'), left_on='boroname', right_index=True)

# Plotting the map
fig, ax = plt.subplots(1, 1, figsize=(10, 10))
nyc_boroughs.boundary.plot(ax=ax, color='black')  # Borough boundaries
nyc_boroughs.plot(column='COLLISION_COUNT', ax=ax, legend=True, cmap='OrRd')
ax.set_title('Number of Collisions by Borough in NYC')
plt.show()
