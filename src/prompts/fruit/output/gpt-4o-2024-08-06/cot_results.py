import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.linear_model import LinearRegression

# Load the data
data = pd.read_csv('./data/fruit_prices.csv')

# Plot configuration
plt.figure(figsize=(10, 6))

# Create a scatter plot
sns.scatterplot(x='RetailPrice', y='CupEquivalentPrice', data=data, label='Data Points')

# Prepare data for the line of best fit
X = data[['RetailPrice']]
y = data['CupEquivalentPrice']

# Fit a linear regression model
model = LinearRegression()
model.fit(X, y)

# Create the line of best fit
x_values = np.array([X.min(), X.max()]).reshape(-1, 1)
y_values = model.predict(x_values)
plt.plot(x_values, y_values, color='red', label='Line of Best Fit')

# Add labels and title
plt.xlabel('Retail Price (per unit)')
plt.ylabel('Cup Equivalent Price')
plt.title('Relationship between Retail Price and Cup Equivalent Price')
plt.legend()

# Show the plot
plt.show()
