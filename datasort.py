import pandas as pd

# Path to your original CSV file
input_file = "recipes_extended.csv"

# Path to save the new filtered CSV
output_file = "final_filtered_recipes.csv"

# Columns to keep
columns_to_keep = [
    "recipe_title",
    "subcategory",
    "ingredients",
    "directions",
    "num_ingredients",
    "num_steps",
    "cook_speed",
    "dietary_profile",
    "healthiness_score",
    "health_level"
]

# Read the original CSV
df = pd.read_csv(input_file)

# Filter the columns
filtered_df = df[columns_to_keep]

# Keep 1 row, delete 2 rows, repeating
filtered_df = filtered_df.iloc[::3]  # Keeps every 3rd row starting from index 0

# Save the new CSV
filtered_df.to_csv(output_file, index=False)

print(f"Filtered CSV saved as {output_file}")
