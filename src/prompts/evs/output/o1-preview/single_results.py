import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# Read the data from the CSV file
df = pd.read_csv('./data/evs.csv')

# Select relevant columns and drop rows with missing values
df_filtered = df[['Electric Vehicle Type', 'Electric Range']].dropna()

# Get the unique electric vehicle types
vehicle_types = df_filtered['Electric Vehicle Type'].unique()

# Create subplots for each vehicle type
fig, axes = plt.subplots(1, len(vehicle_types), figsize=(12, 6), sharey=True)

# If there's only one vehicle type, ensure axes is iterable
if len(vehicle_types) == 1:
    axes = [axes]

# Plot histograms for each electric vehicle type
for ax, v_type in zip(axes, vehicle_types):
    # Filter data for the current vehicle type
    data = df_filtered[df_filtered['Electric Vehicle Type'] == v_type]['Electric Range']

    # Plot the histogram
    sns.histplot(data, bins=20, kde=False, ax=ax, edgecolor='black')

    # Set plot titles and labels
    ax.set_title(f"{v_type}")
    ax.set_xlabel('Electric Range (miles)')
    ax.set_ylabel('Frequency')

# Adjust layout to prevent overlap
plt.tight_layout()

# Display the plot
plt.show()
