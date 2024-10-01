import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# Load the data
data_path = './data/evs.csv'
df = pd.read_csv(data_path)

# Check the first few rows of the dataframe
print(df.head())

# Set the aesthetic style of the plots
sns.set(style="whitegrid")

# Create a FacetGrid for the electric vehicle types
g = sns.FacetGrid(df, col="Electric Vehicle Type", col_wrap=3, height=4, sharex=True, sharey=True)

# Map a histogram to each facet
g.map(plt.hist, 'Electric Range', bins=20, color='blue', alpha=0.7)

# Set the title and labels
g.set_titles(col_template="{col_name}")  # Title provides the electric vehicle type
g.set_axis_labels("Electric Range (miles)", "Frequency")  # Axis labels

# Add a main title
plt.subplots_adjust(top=0.85)
g.fig.suptitle('Distribution of Electric Vehicle Range by Vehicle Type', fontsize=16)

# Show the plot
plt.show()
