import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd

# Read the collision data
df = pd.read_csv('./data/collisions.csv')

# Remove rows with missing 'BOROUGH' values
df = df[df['BOROUGH'].notna()]

# Count the number of collisions per borough
collision_counts = df['BOROUGH'].value_counts().reset_index()
collision_counts.columns = ['Borough', 'Collision_Count']

# Load the NYC borough boundaries shapefile from geopandas datasets
boroughs = gpd.read_file(gpd.datasets.get_path('nybb'))

# Ensure borough names match by converting to uppercase
boroughs['Borough'] = boroughs['BoroName'].str.upper()

# Merge collision counts into the borough GeoDataFrame
boroughs = boroughs.merge(collision_counts, on='Borough', how='left')

# Replace NaN in 'Collision_Count' with zero if any boroughs have no collisions
boroughs['Collision_Count'] = boroughs['Collision_Count'].fillna(0)

# Plot the map
fig, ax = plt.subplots(1, 1, figsize=(10, 10))
boroughs.plot(column='Collision_Count', ax=ax, cmap='OrRd', legend=True,
              legend_kwds={'label': "Number of Collisions", 'shrink': 0.6})

ax.set_title('Number of Collisions per Borough in NYC')
ax.axis('off')

plt.show()
