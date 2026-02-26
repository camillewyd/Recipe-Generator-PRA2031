#generator.py

from ingredients import quick_ingredient_input, Ingredient
from recipes import load_recipes_from_csv, Recipe
from diet_filters import get_diet_options

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
    # Only show recipes that match at least 1 ingredient
    return [r for r in ranked if r.match_score(available_ingredients) > 0]

def main():
    csv_path = "final_filtered_recipes(10columns).csv"

    #Diet options
    diet_options = get_diet_options(csv_path)
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
    if matches :
        for recipe in matches:
            recipe.display(available_ingredients)

    else :
        print ("No matching recipes found.")

if __name__ == "__main__":
    main()

   