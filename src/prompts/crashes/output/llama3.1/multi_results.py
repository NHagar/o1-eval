import folium
import pandas as pd
from sklearn.preprocessing import LabelEncoder

# Load the data
df = pd.read_csv("./data/collisions.csv")

# Print the first few rows of the data
print(df.head())

# Check for missing values
print("Missing Values:")
print(df.isnull().sum())

# Convert categorical variables to lowercase
df["BOROUGH"] = df["BOROUGH"].str.lower()
df["CRASH_DATE"] = df["CRASH DATE"].str.lower()
df["CRASH_TIME"] = df["CRASH TIME"].str.lower()
# df["CONTRIBUTING_FACTOR_1"] = df["CONTRIBUTING_FACTOR_1"].str.lower()
# df["CONTRIBUTING_FACTOR_2"] = df["CONTRIBUTING_FACTOR_2"].str.lower()
# df["CONTRIBUTING_FACTOR_3"] = df["CONTRIBUTING_FACTOR_3"].str.lower()
# df["CONTRIBUTING_FACTOR_4"] = df["CONTRIBUTING_FACTOR_4"].str.lower()
# df["CONTRIBUTING_FACTOR_5"] = df["CONTRIBUTING_FACTOR_5"].str.lower()

# Convert object-type columns to categorical variables
le = LabelEncoder()
df["BOROUGH"] = le.fit_transform(df["BOROUGH"])
df["CRASH_DATE"] = le.fit_transform(df["CRASH_DATE"])
df["CRASH_TIME"] = le.fit_transform(df["CRASH_TIME"])
# df["CONTRIBUTING_FACTOR_1"] = le.fit_transform(df["CONTRIBUTING_FACTOR_1"])
# df["CONTRIBUTING_FACTOR_2"] = le.fit_transform(df["CONTRIBUTING_FACTOR_2"])
# df["CONTRIBUTING_FACTOR_3"] = le.fit_transform(df["CONTRIBUTING_FACTOR_3"])
# df["CONTRIBUTING_FACTOR_4"] = le.fit_transform(df["CONTRIBUTING_FACTOR_4"])
# df["CONTRIBUTING_FACTOR_5"] = le.fit_transform(df["CONTRIBUTING_FACTOR_5"])

# Create a new column 'borough_numeric' with a numeric value for each borough
df["borough_numeric"] = df.apply(lambda row: 0, axis=1)

# Map boroughs to numbers
borough_map = {
    "MANHATTAN": 1,
    "BRONX": 2,
    "BROOKLYN": 3,
    "QUEENS": 4,
    "STATEN ISLAND": 5,
}


# # Assign a numeric value for each borough
# df["borough_numeric"] = df.apply(lambda row: borough_map[row["BOROUGH"]], axis=1)

# Group by borough and count the number of collisions
borough_counts = df.groupby("BOROUGH")["borough_numeric"].count().reset_index()
borough_counts.columns = ["Borough", "Number of Collisions"]

# Create a dictionary to map boroughs to colors
color_map = {
    "manhattan": "#FF0000",
    "bronx": "#008000",
    "brooklyn": "#0000FF",
    "queens": "#FFFF00",
    "staten island": "#800080",
}

# Create a Folium map
m = folium.Map(location=[40.7128, -74.0060], zoom_start=10)

# Add boroughs to the map with shading based on collision counts
for index, row in borough_counts.iterrows():
    borough_name = row["Borough"]
    color = color_map[borough_name]
    collision_count = int(row["Number of Collisions"])
    folium.features.Marker(
        location=[40.7128 + (collision_count / 10000), -74.0060],
        icon=folium.features.DivIcon(
            html=f'<div style="position: absolute; top: {20 + (collision_count / 500)}px; left: 50px; width: 10px; height: {collision_count}px; background-color: {color}"></div>'
        ),
    ).add_to(m)

# Add a legend to the map
legend_html = '<style>body{ margin:0; padding:0;}</style><table style="background-color:#f2f2f2;">'
for borough_name, color in color_map.items():
    legend_html += f'<tr><td style="background-color:{color}; width:20px;height:10px"></td><td>{borough_name}</td></tr>'
legend_html += "</table>"
folium.IFrame(html=legend_html, width=200, height=100).add_to(m)

# Save the map to an HTML file
m.save("collision_map.html")

# Group by borough and count the number of collisions (for display)
display_borough_counts = df.groupby("BOROUGH")["borough_numeric"].count().reset_index()
display_borough_counts.columns = ["Borough", "Number of Collisions"]

# Display the map
print("Map saved to collision_map.html")

# Print the borough counts for display
print(display_borough_counts)

# Display the borough counts for further analysis
analysis_borough_counts = df.groupby("BOROUGH")["borough_numeric"].count().reset_index()
analysis_borough_counts.columns = ["Borough", "Number of Collisions"]

# Display the borough counts
print("Analysis Borough Counts:")
print(analysis_borough_counts)
