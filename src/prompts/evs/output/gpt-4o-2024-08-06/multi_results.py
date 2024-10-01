import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# Load the data
file_path = './data/evs.csv'
ev_data = pd.read_csv(file_path)

# Inspect the data
print("Data Head:")
print(ev_data.head())
print("\nData Info:")
print(ev_data.info())

# Data Cleaning

# Check for missing values in 'Electric Range'
missing_range_count = ev_data['Electric Range'].isnull().sum()
print(f"\nMissing values in 'Electric Range': {missing_range_count}")

# Drop rows with missing Electric Range
ev_data.dropna(subset=['Electric Range'], inplace=True)

# Check for consistent entries in 'Electric Vehicle Type'
print("\nElectric Vehicle Type counts:")
print(ev_data['Electric Vehicle Type'].value_counts())

# Drop duplicates if they exist
ev_data.drop_duplicates(inplace=True)

# Optionally, save the cleaned data for future use
cleaned_file_path = './data/cleaned_evs.csv'
ev_data.to_csv(cleaned_file_path, index=False)

# Analyze the distribution
ev_range_stats = ev_data.groupby('Electric Vehicle Type')['Electric Range'].describe()
print("\nElectric Range Statistics by Vehicle Type:")
print(ev_range_stats)

# Visualize the distribution
vehicle_types = ev_data['Electric Vehicle Type'].unique()
num_types = len(vehicle_types)

# Set up the matplotlib figure for histograms
fig, axes = plt.subplots(1, num_types, figsize=(5 * num_types, 6), sharey=True)

# Plot a histogram for each vehicle type
for ax, vehicle_type in zip(axes, vehicle_types):
    subset = ev_data[ev_data['Electric Vehicle Type'] == vehicle_type]
    sns.histplot(subset['Electric Range'], bins=20, kde=True, ax=ax)
    ax.set_title(vehicle_type)
    ax.set_xlabel('Electric Range (miles)')
    ax.set_ylabel('Frequency')

# Add a main title
plt.suptitle('Electric Range Distribution by Vehicle Type', y=1.05)

# Adjust layout
plt.tight_layout()

# Display the plot
plt.show()
