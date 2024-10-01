import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Load the data from the CSV file
data = pd.read_csv('./data/fruit_prices.csv')

# Extract the relevant columns
retail_price = data['RetailPrice']
cup_equivalent_price = data['CupEquivalentPrice']

# Calculate the line of best fit
slope, intercept = np.polyfit(retail_price, cup_equivalent_price, 1)
best_fit_line = slope * retail_price + intercept

# Create the scatter plot
plt.figure(figsize=(10, 6))
plt.scatter(retail_price, cup_equivalent_price, color='blue', label='Data Points')

# Plot the line of best fit
plt.plot(retail_price, best_fit_line, color='red', label='Best Fit Line')

# Add title and labels
plt.title('Relationship between Retail Price and Cup Equivalent Price of Fruits')
plt.xlabel('Retail Price (per unit)')
plt.ylabel('Cup Equivalent Price')

# Add a legend
plt.legend()

# Display the plot
plt.show()
