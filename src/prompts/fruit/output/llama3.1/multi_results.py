import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

# Load the data from the CSV file
data = pd.read_csv('./data/fruit_prices.csv')

# Print a summary of the loaded data
print(data.head())
print(data.info())
print(data.describe())

# Check for missing values in relevant columns
missings = data[['RetailPrice', 'CupEquivalentPrice']].isnull().sum()
print(missings)

# Convert object types to float64 if necessary (e.g., RetailPriceUnit, CupEquivalentUnit)
data['RetailPrice'] = pd.to_numeric(data['RetailPrice'])
data['CupEquivalentPrice'] = pd.to_numeric(data['CupEquivalentPrice'])

# Drop any rows with missing values in relevant columns
data.dropna(subset=['RetailPrice', 'CupEquivalentPrice'], inplace=True)

# Ensure that Yield is not influencing the relationship between retail and cup equivalent prices
data.loc[data['Yield'] == 1.0, 'Yield'] = np.nan

# Handle any inconsistencies in unit conversion (if necessary)
# This might require domain-specific knowledge or additional data

# Create a scatter plot to visualize the relationship between RetailPrice and CupEquivalentPrice
plt.figure(figsize=(8, 6))
plt.scatter(data['RetailPrice'], data['CupEquivalentPrice'])
plt.title('Relationship Between Retail Price and Cup Equivalent Price')
plt.xlabel('Retail Price ($)')
plt.ylabel('Cup Equivalent Price ($)')
plt.grid(True)

# Add a regression line to the scatter plot
z = np.polyfit(data['RetailPrice'], data['CupEquivalentPrice'], 1)
p = np.poly1d(z)
plt.plot(data['RetailPrice'], p(data['RetailPrice']), "r--")

# Annotate the points with fruit names
for i, row in data.iterrows():
    plt.annotate(row['FruitName'], (row['RetailPrice'], row['CupEquivalentPrice']))

# Show the plot
plt.show()

# Create a bar chart to visualize the distribution of RetailPrice and CupEquivalentPrice by fruit type
fig, ax = plt.subplots(1, 2, figsize=(12, 6))
data.groupby('FruitType')['RetailPrice'].mean().plot(kind='bar', ax=ax[0])
data.groupby('FruitType')['CupEquivalentPrice'].mean().plot(kind='bar', ax=ax[1])

# Set labels and title
ax[0].set_title('Mean Retail Price by Fruit Type')
ax[0].set_xlabel('Fruit Type')
ax[0].set_ylabel('$')

ax[1].set_title('Mean Cup Equivalent Price by Fruit Type')
ax[1].set_xlabel('Fruit Type')
ax[1].set_ylabel('$')

# Show the plot
plt.show()

# Create a heatmap to visualize the correlation matrix between RetailPrice and CupEquivalentPrice for different fruit types
correlation_matrix = data.groupby('FruitType')[['RetailPrice', 'CupEquivalentPrice']].corr()
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm')

# Set labels and title
plt.title('Correlation Matrix Between Retail Price and Cup Equivalent Price')
plt.xlabel('Feature')
plt.ylabel('Feature')

# Show the plot
plt.show()

# Create a boxplot to visualize the distribution of RetailPrice and CupEquivalentPrice by fruit type
fig, ax = plt.subplots(1, 2, figsize=(12, 6))
data.groupby('FruitType')['RetailPrice'].boxplot(ax=ax[0])
data.groupby('FruitType')['CupEquivalentPrice'].boxplot(ax=ax[1])

# Set labels and title
ax[0].set_title('Distribution of Retail Price by Fruit Type')
ax[0].set_xlabel('Fruit Type')
ax[0].set_ylabel('$')

ax[1].set_title('Distribution of Cup Equivalent Price by Fruit Type')
ax[1].set_xlabel('Fruit Type')
ax[1].set_ylabel('$')

# Show the plot
plt.show()
