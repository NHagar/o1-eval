import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# Load the dataset
file_path = './data/fruit_prices.csv'
df = pd.read_csv(file_path)

# Display the first few rows of the DataFrame
print("Initial Dataframe:\n", df.head())

# Display basic information about the DataFrame
print("\nDataFrame Info:\n")
df.info()

# Check for missing values
print("\nMissing Values by Column:\n", df.isnull().sum())

# Drop any rows with missing RetailPrice or CupEquivalentPrice if necessary
df = df.dropna(subset=['RetailPrice', 'CupEquivalentPrice'])

# Check data types to confirm they are appropriate for analysis
# Convert column types if needed (e.g., converting categorical columns to category data type for efficiency)
df['Fruit'] = df['Fruit'].astype('category')
df['Form'] = df['Form'].astype('category')
df['RetailPriceUnit'] = df['RetailPriceUnit'].astype('category')
df['CupEquivalentUnit'] = df['CupEquivalentUnit'].astype('category')

# Display the cleaned DataFrame information
print("\nCleaned DataFrame Info:\n")
df.info()

# Correlation between RetailPrice and CupEquivalentPrice
correlation = df['RetailPrice'].corr(df['CupEquivalentPrice'])
print(f"\nCorrelation between Retail Price and Cup Equivalent Price: {correlation:.2f}")

# Set the style for the plots
sns.set(style="whitegrid")

# Scatter plot to visualize the relationship
plt.figure(figsize=(12, 8))
sns.scatterplot(data=df, x='RetailPrice', y='CupEquivalentPrice', hue='Fruit', style='Form', s=100, palette='viridis')

# Add a regression line
sns.regplot(data=df, x='RetailPrice', y='CupEquivalentPrice', scatter=False, color='red')

# Title and labels
plt.title('Retail Price vs. Cup Equivalent Price of Fruits', fontsize=16)
plt.xlabel('Retail Price', fontsize=14)
plt.ylabel('Cup Equivalent Price', fontsize=14)

# Adjust the legend
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', title='Fruit & Form', fontsize='10')

# Improve layout
plt.tight_layout()

# Show plot
plt.show()
