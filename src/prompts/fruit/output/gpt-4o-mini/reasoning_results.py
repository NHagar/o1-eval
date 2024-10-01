import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.linear_model import LinearRegression

# Load the dataset
file_path = './data/fruit_prices.csv'
dataset = pd.read_csv(file_path)

# Extract relevant columns
x = dataset['RetailPrice']
y = dataset['CupEquivalentPrice']

# Create scatter plot
plt.figure(figsize=(10, 6))
sns.scatterplot(x=x, y=y)

# Fit line of best fit
model = LinearRegression()
model.fit(x.values.reshape(-1, 1), y)
line_x = np.linspace(min(x), max(x), 100)
line_y = model.predict(line_x.reshape(-1, 1))
plt.plot(line_x, line_y, color='red', label='Line of Best Fit')

# Add title and labels
plt.title('Relationship between Retail Price and Cup Equivalent Price')
plt.xlabel('Retail Price')
plt.ylabel('Cup Equivalent Price')
plt.legend()
plt.grid(True)
plt.show()
