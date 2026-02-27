#diet_filters.py

import pandas as pd


def get_diet_options(csv_path: str) -> list[str]:
    """Extracts all unique diet tags from the CSV file.
    This function scans the 'deitary profile', cleans the data and returns a sorted list of tags"""

    df = pd.read_csv(csv_path) #Load the CSV file into a DataFrame (Pandas)
    df.columns = df.columns.str.strip() #Removes space around column names

    all_diet_tags = set()
    for profiles in df["dietary_profile"].dropna():
        clean_str = str(profiles).strip("[]").replace("'","").replace('"','') #Converts to string, removes brackets and quotes
        tags = clean_str.split(",") #Split into individual tags based on comma separation

        for tag in tags:
            clean_tag = tag.strip().lower() #strips whitespace and converts to lowercase for consistency

            if clean_tag:
                all_diet_tags.add(clean_tag)
            
    return sorted(all_diet_tags)