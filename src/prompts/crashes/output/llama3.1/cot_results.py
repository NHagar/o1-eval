import folium
import pandas as pd

df = pd.read_csv('./data/collisions.csv')
df['BOROUGH'] = df['BOROUGH'].fillna('')
df['BOROUGH'] = df['BOROUGH'].apply(lambda x: '' if x.lower() not in ['brooklyn', 'queens', 'manhattan', 'the bronx'] else x)
borough_counts = df['BOROUGH'].value_counts().to_dict()
m = folium.Map(location=[40.7128, -74.0060], zoom_start=11)

for borough, count in borough_counts.items():
    if count > 0: # Ignore boroughs with zero collisions
        folium.Marker([40.7677 + (borough == 'brooklyn') * (-1.5), -74.0056], popup=f'{borough}: {count} collisions', icon=folium.Icon(color='red')).add_to(m)

m.save('collision_map.html')
