import matplotlib.pyplot as plt
import pandas as pd

# Load the data
df = pd.read_csv('./data/fruit_prices.csv')

# Create a scatter plot of RetailPrice and CupEquivalentPrice with a line of best fit
plt.figure(figsize=(8,6))
plt.scatter(df['RetailPrice'], df['CupEquivalentPrice'])
z = np.polyfit(np.log(df['RetailPrice']), np.log(df['CupEquivalentPrice']), 1)
p = np.poly1d(z)
xp = np.linspace(min(df['RetailPrice']), max(df['RetailPrice']), 100)
yp = p(xp)
plt.plot(np.exp(xp), np.exp(yp), color='red')
plt.xscale('log')
plt.yscale('log')

# Add title and labels
plt.title('Relationship between Retail Price and Cup Equivalent Price')
plt.xlabel('Retail Price ($)')
plt.ylabel('Cup Equivalent Price ($)')

# Show the plot
plt.show()
