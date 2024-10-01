import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Load the data
data = pd.read_csv('./data/fruit_prices.csv')

# Extract relevant columns
x = data['RetailPrice']
y = data['CupEquivalentPrice']

# Create a scatter plot
plt.figure(figsize=(10, 6))
plt.scatter(x, y, color='blue', label='Data points')

# Calculate a line of best fit
m, b = np.polyfit(x, y, 1)  # Linear regression
plt.plot(x, m*x + b, color='red', label='Line of best fit')

# Add titles and labels
plt.title('Relationship Between Retail Price and Cup Equivalent Price')
plt.xlabel('Retail Price ($)')
plt.ylabel('Cup Equivalent Price ($/cup)')
plt.legend()
plt.grid()

# Show the plot
plt.show()
