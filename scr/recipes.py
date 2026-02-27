# recipe.py

import csv 
from typing import List, Optional
from ingredients import Ingredient


# RECIPE CLASS: represents a recipe with title, ingredients, directions, health score, and optional diet tags
class Recipe:

    def __init__(
            self, 
            title: str,
            ingredients: List[Ingredient], 
            directions: List[str],
            health_score: float,
            health_level: str,
            diet_tags: Optional[list[str]]=None,
            raw_ingredients: Optional[list[str]] = None):
        
        self.title = title
        self.ingredients = ingredients #List of ingredient objects 
        self.raw_ingredients = raw_ingredients or [] #List of ingredient names as strings, for easier matching
        self.directions = directions #list of steps 
        self.health_score= float(health_score)
        self.health_level=health_level  
        self.diet_tags = diet_tags or []
        self.num_steps = len(directions)

    def match_score(self, available_ingredients: List[Ingredient]) -> int:
        """
        Returns how many ingredients match.
        """
        available_names = [i.name for i in available_ingredients]
        recipe_names = [i.name for i in self.ingredients]
        matches = [ing for ing in recipe_names if ing in available_names]
        return len(matches)

    def missing_ingredients(self, available_ingredients: List[Ingredient]) -> List[str]: 
        """Returns a list of missing ingredient names (as strings) that are in the recipe but not in the user's available ingredients."""
        available_names = [i.name for i in available_ingredients]

        if self.raw_ingredients: 
            """ If we have raw ingredient strings, we can use those for a more user-friendly display of missing ingredients (with quantities if available) """
            return [ing for ing in self.raw_ingredients if ing not in available_names]
        else:
            return [ing.name for ing in self.ingredients if ing.name not in available_names]

    def display(self, available_ingredients: List[Ingredient]) -> None:
        print(f"\nRecipe: {self.title}")
        print(f"Health Score: {self.health_score}/10 ({self.health_level})")
        if self.diet_tags:
            print(f"Diet Tags: {', '.join(self.diet_tags)}")

        available_names = [i.name for i in available_ingredients]

         # Decide which text to show (raw with quantities or cleaned names)
        if self.raw_ingredients:
            pairs = list(zip(self.ingredients, self.raw_ingredients))
        else:
            pairs = [(ing, ing.name) for ing in self.ingredients]

        # Split into “have” and “missing”
        have_pairs = [(ing, raw) for ing, raw in pairs if ing.name in available_names]
        missing_pairs = [(ing, raw) for ing, raw in pairs if ing.name not in available_names]

        #Show both lists grouped by category (using existing Ingredient.category)
        def group_by_category(pairs_list):
            grouped: dict[str, list[str]] = {}
            for ing, raw in pairs_list:
                cat = ing.category or "other"
                grouped.setdefault(cat, []).append(raw)
            return grouped

        have_by_cat = group_by_category(have_pairs)
        missing_by_cat = group_by_category(missing_pairs)

        print("\nIngredients you have (by category):")
        if not have_by_cat:
            print("- (none)")
        else:
            for cat in sorted(have_by_cat.keys()):
                print(f"{cat.upper()}:")
                for raw in have_by_cat[cat]:
                    print(f"  - {raw}")

        if missing_by_cat:
            print("\nMissing ingredients (by category):")
            for cat in sorted(missing_by_cat.keys()):
                print(f"{cat.upper()}:")
                for raw in missing_by_cat[cat]:
                    print(f"  - {raw}")

        print("\nDirections:")
        for i, step in enumerate(self.directions, 1):
            print(f"{i}. {step}")

    def __repr__(self) -> str:
        return f"Recipe('{self.title}', {len(self.ingredients)} ingredients)"
    
    #CSV loader function
def load_recipes_from_csv(file_path):
    recipes = []

    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader: #Assumes columns: recipe_title, ingredients, directions, healthiness_score, health_level, dietary_profile
            title = row["recipe_title"]          # not "title"
            directions_raw = row["directions"]   # same style list string
            health_score = float(row["healthiness_score"])
            health_level = row["health_level"]
            ingredients_raw = row["ingredients"]
            
            # parse ingredients list string
            inner = ingredients_raw.strip()[1:-1].replace('""', '"')
            raw_items = [s.strip() for s in inner.split('",') if s.strip()]
            raw_ingredients_list = [s.strip().strip('"').strip() for s in raw_items] 
            ingredients_list = [Ingredient(name) for name in raw_ingredients_list]

            # parse directions list string
            directions_clean = (
                directions_raw.strip()[1:-1]
                .replace('""', '"')
                .replace('"', '')
            )
            directions_list = [s.strip() for s in directions_clean.split(".,") if s.strip()]
            

            # dietary_profile
            diet_raw = row["dietary_profile"]
            diet_clean = (
                diet_raw.strip()[1:-1]
                .replace('""', '"')
                .replace('"', '')
            )
            diet_tags_list = [t.strip().lower() for t in diet_clean.split(",") if t.strip()]

            recipe = Recipe(
                title=title,
                raw_ingredients=raw_ingredients_list,
                ingredients=ingredients_list,
                directions=directions_list,
                health_score=health_score,
                health_level=health_level,
                diet_tags=diet_tags_list,
            )
            recipes.append(recipe)

    return recipes
 
    
 
