import pandas as pd

# -----------------------------
# Classes
# -----------------------------

class Ingredient:
    def __init__(self, name):
        self.name = name.lower().strip()

    def __repr__(self):
        return self.name


class Recipe:
    def __init__(self, title, ingredients, directions, diet_tags=None):
        self.title = title
        self.ingredients = ingredients
        self.directions = directions
        self.diet_tags = diet_tags or []

    def match_score(self, available_ingredients):
        """
        Returns how many ingredients match.
        """
        available_names = [i.name for i in available_ingredients]
        recipe_names = [i.name for i in self.ingredients]
        matches = [ing for ing in recipe_names if ing in available_names]
        return len(matches)

    def missing_ingredients(self, available_ingredients):
        available_names = [i.name for i in available_ingredients]
        return [ing.name for ing in self.ingredients if ing.name not in available_names]

    def display(self, available_ingredients):
        print(f"\nRecipe: {self.title}")
        print("Ingredients:")
        for ing in self.ingredients:
            print(f"- {ing.name}")

        missing = self.missing_ingredients(available_ingredients)

        if missing:
            print("\nYou are missing:")
            for m in missing:
                print(f"- {m}")
        else:
            print("\nYou have all ingredients!")

        print("\nDirections:")
        for i, step in enumerate(self.directions, 1):
            print(f"{i}. {step}")


# -----------------------------
# Load CSV
# -----------------------------
df = pd.read_csv("/Users/jessicaabraham/Desktop/PRA2031 Python/Project /final_filtered_recipes.csv")
df.columns = df.columns.str.strip()

all_recipes = []

for _, row in df.iterrows():
    ingredients_list = [Ingredient(i.strip()) for i in row['ingredients'].split(',')]
    directions_list = [s.strip() for s in row['directions'].split('.') if s.strip()]
    diet_tags = [d.strip() for d in str(row['dietary_profile']).split(',')]

    recipe = Recipe(row['recipe_title'], ingredients_list, directions_list, diet_tags)
    all_recipes.append(recipe)

# -----------------------------
# User Input
# -----------------------------
user_input = input("Enter ingredients you have (comma-separated): ")
available_ingredients = [Ingredient(i.strip()) for i in user_input.split(',')]

# -----------------------------
# Recipe Matching
# -----------------------------
scored_recipes = []

for recipe in all_recipes:
    score = recipe.match_score(available_ingredients)
    if score > 0:
        scored_recipes.append((score, recipe))

# Sort by best match
scored_recipes.sort(reverse=True, key=lambda x: x[0])

# Always show top matches
top_n = 3 if len(scored_recipes) >= 3 else len(scored_recipes)

if top_n > 0:
    print("\nBest recipe matches for you:")
    for _, recipe in scored_recipes[:top_n]:
        recipe.display(available_ingredients)
else:
    print("\nNo ingredient matches found — try entering more common ingredients!")