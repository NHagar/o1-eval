import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Load the data from the fruit_prices.csv file into a DataFrame
df = pd.read_csv('./data/fruit_prices.csv')

# Extract the RetailPrice and CupEquivalentPrice columns from the DataFrame
retail_price = df['RetailPrice']
cup_equivalent_price = df['CupEquivalentPrice']

# Ensure there are no missing or invalid values in the RetailPrice and CupEquivalentPrice columns
if retail_price.isnull().values.any() or cup_equivalent_price.isnull().values.any():
    print("Warning: There are missing or invalid values in the data.")
else:
    # Create a scatter plot of the RetailPrice and CupEquivalentPrice columns
    plt.scatter(retail_price, cup_equivalent_price)

    # Calculate a line of best fit for the data (linear)
    z = np.polyfit(retail_price, cup_equivalent_price, 1)
    p = np.poly1d(z)

    # Use the coefficients to create a line that spans the range of x values in the scatter plot
    xp = np.linspace(min(retail_price), max(retail_price), 100)
    yp = p(xp)

    plt.plot(xp, yp, "r--")

    # Add labels to the axes and title for clarity
    plt.xlabel('Retail Price')
    plt.ylabel('Cup Equivalent Price')
    plt.title('Relationship between Retail Price and Cup Equivalent Price')

    # Display the figure
    plt.show()
