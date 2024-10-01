import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# Load the data
file_path = './data/evs.csv'
data = pd.read_csv(file_path)

# Extract relevant columns
ev_data = data[['Electric Vehicle Type', 'Electric Range']]

# Define the plot style
sns.set(style='whitegrid')

# Create the histograms
plt.figure(figsize=(12, 6))
ev_types = ev_data['Electric Vehicle Type'].unique()

for i, ev_type in enumerate(ev_types, 1):
    plt.subplot(1, len(ev_types), i)
    sns.histplot(ev_data[ev_data['Electric Vehicle Type'] == ev_type]['Electric Range'].dropna(), bins=20)
    plt.title(ev_type)
    plt.xlabel('Electric Range (miles)')
    plt.ylabel('Frequency')

plt.tight_layout()
plt.show()
