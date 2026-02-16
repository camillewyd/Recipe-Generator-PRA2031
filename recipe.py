# recipe.py

import csv 
class Ingredient:
    def __init__(self, name):
        self.name = name.lower().strip()

    def __repr__(self):
        return self.name

# RECIPE CLASS
class Recipe:
    def __init__(self, title, ingredients, directions, health_score, diet_tags=None):
        self.title = title
        self.ingredients = ingredients #List of ingredient objects 
        self.directions = directions #list of steps 
        self.health_score=health_score
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
        print(f"Health Score: {self.health_score}/10")
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

    def __repr__(self):
        return f"Recipe('{self.title}', {len(self.ingredients)} ingredients)"
    
    #CSV loader function
    def load_recipes_from_csv(file_path):
        recipes=[]

        with open (file_path,newline='', encoding='utf-8') as csvfile:
            reader=csv.DictReader(csvfile)

            for row in reader:
                title=row["title"]

                #Split ingredients by comma
                ingredients_list= [
                    Ingredient(name) for name in row["ingredients"].split(",")
                ]

                #Split directions by "|"
                directions_list=row["directions"].split("|")
                health_score=row["health_score"]

                #optional diet tags column 
                diet_tags=row.get("diet_tags", "")
                diet_tags_list=diet_tags.split(",")if diet_tags else []

                recipe=Recipe(
                    title,
                    ingredients_list,
                    directions_list,
                    health_score,
                    diet_tags_list
                )
                recipes.append(recipe)

            return recipes 

# ==============================
# RECIPE GENERATOR FUNCTION
# ==============================

def generate_recipes(available_ingredients, all_recipes):
    """
    Sort recipes by 
    1. Ingredient match score 
    2. health score 
    """

    ranked= sorted(
        all_recipes
        key=lambda r : (r.match_score(available_ingredients),r.health_score),
        reverse=True
    )
    # Only show recipes that match at least 1 ingredient
    return [r for r in ranked if r.match_score(available_ingredients) > 0]


# ==============================
# MAIN PROGRAM
# ==============================

#load recipes from CSV 
recipes=load_recipes_from_csv("recipes.csv")

#get user input
user_input=input("Enter ingredients you have (comma seperated):")

#convert input into ingredient obejects
available= [Ingredient(name) for name in user_input.split (",")]

#generate matching recipes 
matches=generate_recipes(available,recipes)

if matches :
    for recipe in matches:
        recipe.display(available)

else :
    print ("No matching recipes found.")


#teammate must import classes from recipe import Recipe ,ingredient 