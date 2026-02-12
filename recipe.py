# recipe.py

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

    def __repr__(self):
        return f"Recipe('{self.title}', {len(self.ingredients)} ingredients)"