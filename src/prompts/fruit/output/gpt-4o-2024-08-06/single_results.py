import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# Load the data
data = pd.read_csv('./data/fruit_prices.csv')

# Set the theme for seaborn
sns.set_theme()

# Create a scatter plot with a line of best fit
plt.figure(figsize=(10, 6))
sns.regplot(x='RetailPrice', y='CupEquivalentPrice', data=data, scatter_kws={'alpha':0.6})

# Add title and labels
plt.title('Relationship between Retail Price and Cup Equivalent Price')
plt.xlabel('Retail Price (per unit)')
plt.ylabel('Cup Equivalent Price (per cup)')

# Show the plot
plt.show()
