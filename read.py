import pandas as pd

df = pd.read_csv("final_filtered_recipes(10columns).csv")
df.columns = df.columns.str.strip()

# Extract dietary profiles

all_diet_tags = set()

for profiles in df["dietary_profile"].dropna():
    tags = str(profiles).split(",")

    for tag in tags:
        clean_tag = tag.strip().lower()

        if clean_tag:
            all_diet_tags.add(clean_tag)

# Convert to sorted list
diet_options = sorted(all_diet_tags)

print("\nAvailable dietary profiles in dataset:")
for i, d in enumerate(diet_options, 1):
    print(f"{i}. {d}")