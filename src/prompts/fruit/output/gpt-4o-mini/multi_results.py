import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# Step 1: Load the Data
file_path = "./data/fruit_prices.csv"
fruit_prices_df = pd.read_csv(file_path)

# Step 2: Explore the Data
print(fruit_prices_df.head())  # Show the first few rows of the DataFrame
print(
    fruit_prices_df.info()
)  # Show DataFrame summary including data types and non-null counts

# Step 3: Data Cleaning
# Check for missing values
missing_values = fruit_prices_df.isnull().sum()
print("Missing values in each column:")
print(missing_values)

# Remove rows with missing values if necessary
fruit_prices_df = fruit_prices_df.dropna()

# Check for duplicates
duplicates = fruit_prices_df.duplicated().sum()
if duplicates > 0:
    fruit_prices_df = fruit_prices_df.drop_duplicates()
    print(f"Removed {duplicates} duplicate rows.")

# Ensure correct data types
fruit_prices_df["RetailPrice"] = fruit_prices_df["RetailPrice"].astype(float)
fruit_prices_df["Yield"] = fruit_prices_df["Yield"].astype(float)
fruit_prices_df["CupEquivalentSize"] = fruit_prices_df["CupEquivalentSize"].astype(
    float
)
fruit_prices_df["CupEquivalentPrice"] = fruit_prices_df["CupEquivalentPrice"].astype(
    float
)

# Step 4: Descriptive Statistics
print("Descriptive statistics for RetailPrice and CupEquivalentPrice:")
print(fruit_prices_df[["RetailPrice", "CupEquivalentPrice"]].describe())

# Step 5: Correlation Analysis
correlation = fruit_prices_df["RetailPrice"].corr(fruit_prices_df["CupEquivalentPrice"])
print(
    f"Correlation coefficient between RetailPrice and CupEquivalentPrice: {correlation}"
)

# Step 6: Data Visualization
# Set the aesthetic style of the plots
sns.set(style="whitegrid")

# Scatter Plot
plt.figure(figsize=(10, 6))
sns.scatterplot(
    data=fruit_prices_df,
    x="RetailPrice",
    y="CupEquivalentPrice",
    hue="Form",
    style="Form",
    s=100,
    palette="deep",
)
plt.title("Scatter Plot of Retail Price vs Cup Equivalent Price")
plt.xlabel("Retail Price (per unit)")
plt.ylabel("Cup Equivalent Price (per cup unit)")
plt.grid()
plt.legend(title="Form", bbox_to_anchor=(1, 1), loc="upper left")
plt.tight_layout()
plt.show()

# Regression Plot
plt.figure(figsize=(10, 6))
sns.regplot(
    data=fruit_prices_df,
    x="RetailPrice",
    y="CupEquivalentPrice",
    scatter_kws={"alpha": 0.6},
    line_kws={"color": "orange"},
)
plt.title("Retail Price vs Cup Equivalent Price with Regression Line")
plt.xlabel("Retail Price (per unit)")
plt.ylabel("Cup Equivalent Price (per cup unit)")
plt.grid()
plt.tight_layout()
plt.show()

# Pairplot (Optional)
sns.pairplot(
    fruit_prices_df,
    vars=["RetailPrice", "CupEquivalentPrice", "Yield", "CupEquivalentSize"],
    hue="Form",
    diag_kind="kde",
)
plt.suptitle(
    "Pairplot of Retail Price, Cup Equivalent Price, Yield, and Cup Equivalent Size",
    y=1.02,
)
plt.tight_layout()
plt.show()
