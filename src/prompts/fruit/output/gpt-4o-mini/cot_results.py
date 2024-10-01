# Import necessary libraries
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Load the data
data = pd.read_csv('./data/fruit_prices.csv')

# Extract relevant columns
x = data['RetailPrice']
y = data['CupEquivalentPrice']

# Create a scatter plot
plt.scatter(x, y, color='blue', label='Data points')

# Calculate line of best fit
m, b = np.polyfit(x, y, 1)
plt.plot(x, m*x + b, color='red', label='Line of Best Fit')

# Add title and labels
plt.title('Relationship Between Retail Price and Cup Equivalent Price')
plt.xlabel('Retail Price ($)')
plt.ylabel('Cup Equivalent Price ($)')

# Show legend
plt.legend()

# Display the plot
plt.show()
