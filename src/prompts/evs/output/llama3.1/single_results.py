import matplotlib.pyplot as plt
import pandas as pd

# Load data from CSV file
df = pd.read_csv('./data/evs.csv')

# Define a dictionary to group electric vehicle types by color
colors = {
    'Battery Electric Vehicle (BEV)': 'blue',
    'Plug-in Hybrid Electric Vehicle (PHEV)': 'red',
}

# Create a figure with multiple subplots for each electric vehicle type
fig, axs = plt.subplots(len(colors), figsize=(8, 6 * len(colors)))

# Iterate over each electric vehicle type
for i, ev_type in enumerate(colors):
    # Filter the data by electric vehicle type
    ev_df = df[df['Electric Vehicle Type'] == ev_type]

    # Plot a histogram of electric range for this type
    axs[i].hist(ev_df['Electric Range'], bins=20, alpha=0.7, color=colors[ev_type], edgecolor='black')
    axs[i].set_title(f'{ev_type} Electric Vehicles - Electric Range Distribution')
    axs[i].set_xlabel('Range (miles)')
    axs[i].set_ylabel('Frequency')

# Layout so plots do not overlap
fig.tight_layout()

# Show the plot
plt.show()
