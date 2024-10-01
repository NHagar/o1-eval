import matplotlib.pyplot as plt
import pandas as pd

# Step 1: Load the data
data = pd.read_csv('./data/evs.csv')

# Step 2: Data Cleaning
data = data.dropna(subset=['Electric Range', 'Electric Vehicle Type'])

# Step 3: Group the data by Electric Vehicle Type
ev_types = data['Electric Vehicle Type'].unique()

# Step 4: Create Histograms
plt.figure(figsize=(15, 8))
colors = plt.cm.viridis(range(len(ev_types)))  # Get colors for each type
for i, ev_type in enumerate(ev_types):
    subset = data[data['Electric Vehicle Type'] == ev_type]
    plt.hist(subset['Electric Range'], bins=20, alpha=0.7, label=ev_type, color=colors[i])

# Step 5: Customize the plot
plt.title('Distribution of Electric Vehicle Range by Type')
plt.xlabel('Electric Range (miles)')
plt.ylabel('Frequency')
plt.legend(title='Electric Vehicle Type')
plt.grid(axis='y', alpha=0.75)
plt.tight_layout()

# Show the plot
plt.show()
