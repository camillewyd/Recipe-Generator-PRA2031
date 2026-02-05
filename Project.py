import pandas as pd

# Load CSV file
df = pd.read_csv('recipes_extended.csv')

# Inspect original data (optional)
print("Original data columns:")
print(df.columns)

# Keep only the first 10 columns
df = df.iloc[:, :10]  # all rows, columns 0 to 9

# Inspect the updated dataframe
print("\nData after keeping first 10 columns:")
print(df.head())

# Optional: save cleaned data to a new CSV
df.to_csv('cleaned_data.csv', index=False)