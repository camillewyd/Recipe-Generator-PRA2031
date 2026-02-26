#diet_filters.py

import pandas as pd

# Extract dietary profiles

def get_diet_options(csv_path):
    df = pd.read_csv(csv_path)
    df.columns = df.columns.str.strip()

    all_diet_tags = set()
    for profiles in df["dietary_profile"].dropna():
        clean_str = str(profiles).strip("[]").replace("'","").replace('"','')
        tags = clean_str.split(",")

        for tag in tags:
            clean_tag = tag.strip().lower()

            if clean_tag:
                all_diet_tags.add(clean_tag)
            
    return sorted(all_diet_tags)