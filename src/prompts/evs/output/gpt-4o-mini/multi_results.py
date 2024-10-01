# Import necessary libraries
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# Load the data
file_path = './data/evs.csv'
evs_data = pd.read_csv(file_path)

# Explore the data
print("DataFrame Shape:", evs_data.shape)  # Check the number of rows and columns
print(evs_data.head())  # Display the first few rows of the DataFrame

# Data Cleaning
# Check for missing values
missing_values = evs_data.isnull().sum()
print("Missing Values:\n", missing_values)

# Drop rows with missing 'Electric Range' or 'Electric Vehicle Type'
evs_data_cleaned = evs_data.dropna(subset=['Electric Range', 'Electric Vehicle Type'])

# Check the shape of the cleaned DataFrame
print("Cleaned DataFrame Shape:", evs_data_cleaned.shape)

# Ensure correct data types
print("Data Types:\n", evs_data_cleaned.dtypes)

# Convert 'Electric Range' to float, if not already
evs_data_cleaned['Electric Range'] = evs_data_cleaned['Electric Range'].astype(float)

# Verify the data after cleaning
print("First few rows of cleaned data:\n", evs_data_cleaned.head())

# Analyze the distribution of electric vehicle range
# Create a box plot to visualize the distribution of electric range by vehicle type
plt.figure(figsize=(12, 6))
sns.boxplot(x='Electric Vehicle Type', y='Electric Range', data=evs_data_cleaned)
plt.title('Distribution of Electric Vehicle Range by Type')
plt.xticks(rotation=45)  # Rotate x labels for better readability
plt.xlabel('Electric Vehicle Type')
plt.ylabel('Electric Range (miles)')
plt.ylim(0, evs_data_cleaned['Electric Range'].max() + 50)  # Set y-axis limits
plt.grid()
plt.tight_layout()
plt.show()

# Summary Statistics
summary_stats = (
    evs_data_cleaned
    .groupby('Electric Vehicle Type')['Electric Range']
    .agg(['mean', 'median', 'min', 'max', 'std', 'count'])
    .reset_index()
)
print("Summary Statistics of Electric Range by Vehicle Type:\n", summary_stats)

# Visualization of the distribution of electric vehicle range for each type
# Create a histogram for each electric vehicle type
vehicle_types = evs_data_cleaned['Electric Vehicle Type'].unique()
num_types = len(vehicle_types)
fig, axes = plt.subplots(nrows=num_types, ncols=1, figsize=(10, num_types * 4), sharex=True)

# Plot a histogram for each vehicle type
for i, vehicle_type in enumerate(vehicle_types):
    sns.histplot(evs_data_cleaned[evs_data_cleaned['Electric Vehicle Type'] == vehicle_type]['Electric Range'],
                 bins=20, kde=True, ax=axes[i], color=sns.color_palette()[i % 10])
    axes[i].set_title(vehicle_type)
    axes[i].set_ylabel('Frequency')
    axes[i].set_xlim(0, evs_data_cleaned['Electric Range'].max() + 50)  # Set x-axis limits

# Overall labels
plt.xlabel('Electric Range (miles)')
plt.tight_layout()  # Adjust padding for better spacing
plt.show()
