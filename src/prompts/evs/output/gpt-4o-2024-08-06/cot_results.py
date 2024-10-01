import matplotlib.pyplot as plt
import pandas as pd

# Load the data
data_path = './data/evs.csv'
data = pd.read_csv(data_path)

# Check and handle missing data
data = data.dropna(subset=['Electric Vehicle Type', 'Electric Range'])

# Get unique electric vehicle types
vehicle_types = data['Electric Vehicle Type'].unique()

# Set up the figure
fig, axes = plt.subplots(1, len(vehicle_types), figsize=(15, 5), sharey=True)
fig.suptitle('Distribution of Electric Vehicle Range by Type')

# Generate a histogram for each electric vehicle type
for ax, vehicle_type in zip(axes, vehicle_types):
    type_data = data[data['Electric Vehicle Type'] == vehicle_type]
    ax.hist(type_data['Electric Range'], bins=30, alpha=0.7)
    ax.set_title(vehicle_type)
    ax.set_xlabel('Range (miles)')
    ax.set_ylabel('Frequency')

# Adjust layout for clarity
plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.show()
