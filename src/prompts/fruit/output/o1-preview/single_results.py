import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# Read the data
df = pd.read_csv('./data/fruit_prices.csv', index_col=0)

# Remove rows with missing data in the relevant columns
df = df.dropna(subset=['RetailPrice', 'CupEquivalentPrice'])

# Create the scatter plot with regression line
sns.set(style='whitegrid')
g = sns.lmplot(x='RetailPrice', y='CupEquivalentPrice', data=df, aspect=1.5)

# Set axis labels and title
g.set_axis_labels('Retail Price ($ per unit)', 'Cup Equivalent Price ($ per cup)')
g.fig.suptitle('Relationship between Retail Price and Cup Equivalent Price of Fruits', y=1.03)

# Show the plot
plt.tight_layout()
plt.show()
