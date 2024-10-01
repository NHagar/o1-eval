import matplotlib.pyplot as plt
import pandas as pd

# Load the dataset
data = pd.read_csv('./data/evs.csv')

# Extract relevant columns
vehicle_ranges = data[['Electric Vehicle Type', 'Electric Range']]

# Drop rows with NaN electric ranges
vehicle_ranges = vehicle_ranges.dropna(subset=['Electric Range'])

# Separate data by vehicle type
bev_data = vehicle_ranges[vehicle_ranges['Electric Vehicle Type'] == 'Battery Electric Vehicle (BEV)']['Electric Range']
phev_data = vehicle_ranges[vehicle_ranges['Electric Vehicle Type'] == 'Plug-in Hybrid Electric Vehicle (PHEV)']['Electric Range']

# Create subplots for side-by-side histograms
fig, axes = plt.subplots(1, 2, figsize=(12, 5), sharey=True)
fig.suptitle('Electric Vehicle Range Distribution by Type')

# BEV Histogram
axes[0].hist(bev_data, bins=30, color='blue', alpha=0.7)
axes[0].set_title('Battery Electric Vehicle (BEV)')
axes[0].set_xlabel('Range (miles)')
axes[0].set_ylabel('Frequency')

# PHEV Histogram
axes[1].hist(phev_data, bins=30, color='green', alpha=0.7)
axes[1].set_title('Plug-in Hybrid Electric Vehicle (PHEV)')
axes[1].set_xlabel('Range (miles)')

plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.show()
