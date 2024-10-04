import matplotlib.pyplot as plt
import pandas as pd

# Load libraries and read csv into DataFrame
ev_df = pd.read_csv('./data/evs.csv')

# Filter out missing values in 'Electric Vehicle Type'
ev_df = ev_df.dropna(subset=['Electric Vehicle Type'])

# Convert 'Electric Vehicle Type' to categorical for histograms
ev_df['Electric Vehicle Type'] = pd.Categorical(ev_df['Electric Vehicle Type'])

# Melt the data along 'Electric Vehicle Type'
melted_ev_df = pd.melt(ev_df, id_vars=['Electric Range'], value_vars=['Electric Vehicle Type'])

# Group the melted data by 'Electric Vehicle Type' and take the mean of 'Electric Range'
grouped_ev_df = melted_ev_df.groupby('variable')['value'].mean().reset_index()

# Create a figure with multiple subplots for different EV types
fig, axs = plt.subplots(len(grouped_ev_df), figsize=(8, 6 * len(grouped_ev_df)))

for i, ev_type in enumerate(grouped_ev_df['variable']):
    # Get data specifically for current electric vehicle type
    specific_ev_data = melted_ev_df[melted_ev_df['variable'] == ev_type]

    # Create a histogram for the current EV type on its corresponding subplot
    axs[i].hist(specific_ev_data['value'], bins=range(0, int(max(melted_ev_df['value'])) + 50, 50), alpha=0.7)

# Set labels and title for all subplots
for ax in axs:
    ax.set_xlabel('Electric Range (miles)')
    ax.set_ylabel('Count')
plt.suptitle('Distribution of Electric Vehicle Range by Type')

# Layout so plots do not overlap
fig.tight_layout(rect=[0, 0.03, 1, 0.95])

plt.show()
