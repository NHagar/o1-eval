import os

import matplotlib.pyplot as plt
import pandas as pd

# Define the path to the CSV file
csv_file_path = './data/evs.csv'

# Check if the file exists
if not os.path.exists(csv_file_path):
    raise FileNotFoundError(f"The file {csv_file_path} does not exist.")

# Read the CSV file, selecting only necessary columns to optimize memory usage
use_columns = ['Electric Vehicle Type', 'Electric Range']
df = pd.read_csv(csv_file_path, usecols=use_columns)

# Drop rows with missing values in 'Electric Vehicle Type' or 'Electric Range'
df.dropna(subset=['Electric Vehicle Type', 'Electric Range'], inplace=True)

# Get the unique electric vehicle types
ev_types = df['Electric Vehicle Type'].unique()

# Determine the number of subplots needed
num_types = len(ev_types)

# Set up the matplotlib figure and axes
fig, axes = plt.subplots(1, num_types, figsize=(6*num_types, 6), sharey=True)

# If there's only one EV type, axes may not be an array
if num_types == 1:
    axes = [axes]

# Define the number of bins for the histograms
bins = 30

# Plot a histogram for each electric vehicle type
for ax, ev_type in zip(axes, ev_types):
    # Filter the data for the current EV type
    range_data = df[df['Electric Vehicle Type'] == ev_type]['Electric Range']

    # Plot the histogram
    ax.hist(range_data, bins=bins, color='skyblue', edgecolor='black')

    # Set the title and labels
    ax.set_title(f"{ev_type}")
    ax.set_xlabel("Electric Range (miles)")
    ax.set_ylabel("Frequency")
    ax.grid(True, linestyle='--', alpha=0.7)

# Adjust layout for better spacing
plt.tight_layout()

# Display the plot
plt.show()
