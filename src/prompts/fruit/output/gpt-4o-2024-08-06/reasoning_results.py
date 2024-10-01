import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# Load the data from CSV
file_path = './data/fruit_prices.csv'
data = pd.read_csv(file_path)

# Create the scatter plot with line of best fit
sns.lmplot(x='RetailPrice', y='CupEquivalentPrice', data=data, height=6, aspect=1.5)

# Add a title
plt.title('Relationship between Retail Price and Cup Equivalent Price')

# Show the plot
plt.show()
