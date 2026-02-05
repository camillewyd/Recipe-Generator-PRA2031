class Recipe:
    """
    Recipe with its attributes:
    - name (str): Name of the recipe
    - subcategory (str): Subcategory of the recipe
    - ingredients (list): List of ingredients required for the recipe (with measurements)
    - directions (list): Step-by-step instructions to prepare the recipe
    - num_ingredients (int): Number of ingredients required for the recipe
    - num_steps (int): Number of steps in the directions to prepare the recipe
    - cook_speed (str): Speed at which the recipe can be cooked ('fast', 'medium', 'slow')
    - dietary profile (str): vegan, gluten-free, nut-free, etc
    - healthiness_score (int): from 0 to 100, indicating how healthy the recipe is
    - health_level (str): healthy, moderate, etc
    """

    def __init__(self, name, subcategory, ingredients, directions, cook_speed,
                 dietary_profile, healthiness_score, health_level):
        self.name = name
        self.subcategory = subcategory
        self.ingredients = ingredients
        self.directions = directions
        self.num_ingredients = len(ingredients)
        self.num_steps = len(directions)
        self.cook_speed = cook_speed
        self.dietary_profile = dietary_profile
        self.healthiness_score = healthiness_score
        self.health_level = health_level

   