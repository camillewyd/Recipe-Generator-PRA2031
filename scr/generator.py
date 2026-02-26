#generator.py

from ingredients import quick_ingredient_input, Ingredient
from recipes import load_recipes_from_csv, Recipe
from diet_filters import get_diet_options
import random

def filter_recipes(recipes, diet_choice, min_health_score):
    filtered = []

    for r in recipes:
        if r.health_score < min_health_score:
            continue
        if diet_choice and diet_choice not in r.diet_tags:
            continue

        filtered.append(r)
    return filtered

def generate_recipes(available_ingredients, all_recipes):
    """
    Sort recipes by 
    1. Ingredient match score 
    2. health score 
    """

    ranked= sorted(
        all_recipes,
        key=lambda r : (r.match_score(available_ingredients),r.health_score),
        reverse=True)
    # Only show recipes that match at least 1 ingredient if 1 ingredient is available, or at least 2 if more are available
    if len(available_ingredients) == 1:
        return [r for r in ranked if r.match_score(available_ingredients) >= 1]
    else:
        return [r for r in ranked if r.match_score(available_ingredients) >= 2]


def main():
    csv_path = "filtered_recipes(10columns).csv"

    #Diet options
    diet_options = get_diet_options(csv_path)
    diet_options = [d for d in diet_options if d!= "unspecified"]  # Remove empty tags
    print("Available diet options:")
    for i, option in enumerate(diet_options, 1):
        print(f"{i}. {option}")

    choice = input("Select a diet option (or press Enter to skip): ").strip()
    diet_choice = None
    if choice:
        try:
            diet_choice = diet_options[int(choice) - 1]
        except (ValueError, IndexError):
            print("Choice not available. No diet filter will be applied.")

    min_health_score = input("Enter minimum health score (0-100, or press Enter to skip): ").strip()
    min_health_score = float(min_health_score) if min_health_score else 0

    #load recipes from CSV 
    recipes=load_recipes_from_csv(csv_path)

    #filter by diet and health score
    recipes=filter_recipes(recipes,diet_choice,min_health_score)


    #get ingredients from user (which are auto-categorized)
    manager = quick_ingredient_input()
    available_ingredients = manager.get_all_ingredients()

    #generate matching recipes 
    matches=generate_recipes(available_ingredients,recipes)
    if not matches :
        print("No matching recipes found. Try adjusting your filters or adding more ingredients.")
        return

    top_n = min(10, len(matches))
    print(f"\nTop {top_n} recipes:")
    for i, recipe in enumerate(matches[:top_n], 1):
        print(f"{i}.{recipe.title} (match score: {recipe.match_score(available_ingredients)})")

    selection = input(f"Select a recipe to view details (1-{top_n}): ").strip()
    try:
        idx = int(selection) - 1
        if idx<0 or idx >= top_n:
            print("Invalid selection. Exiting.")
            return
    except ValueError:
        print("Invalid input. Exiting.")
        return
        
    chosen_recipe = matches[idx]
    chosen_recipe.display(available_ingredients)

if __name__ == "__main__":
    main()

   