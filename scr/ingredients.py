# ingredients.py
"""
Handles ingredient management with simplified categorization .
Integrates with read_csv.py to work with ingredients from the recipe dataset.
"""

import re
from typing import List, Dict, Optional


class Ingredient:
    """
    Represents a single ingredient with category classification.
    The class includes methods to clean ingredient names, auto-detect categories, and compare ingredients.
    Categories include: proteins, carbs, produce, dairy, pantry.
    """
    
    # Simplified ingredient categories (5 main groups)
    CATEGORIES = {
        'proteins': {
            'chicken', 'beef', 'pork', 'turkey', 'lamb', 'fish', 'salmon', 'tuna',
            'shrimp', 'prawns', 'crab', 'lobster', 'eggs', 'egg', 'tofu', 'tempeh',
            'ground beef', 'ground turkey', 'bacon', 'sausage', 'ham',
            'chicken breast', 'chicken thighs', 'chicken wings',
            'beans', 'lentils', 'chickpeas', 'black beans', 'peas'
        },
        'carbs': {
            'rice', 'pasta', 'bread', 'quinoa', 'noodles', 'flour', 'oats',
            'all-purpose flour', 'bread crumbs', 'panko', 'crackers',
            'tortillas', 'potatoes', 'sweet potato', 'cornmeal'
        },
        'produce': {
            'tomatoes', 'lettuce', 'spinach', 'kale', 'broccoli', 'carrots',
            'celery', 'cucumber', 'bell pepper', 'onion', 'garlic', 'mushrooms',
            'zucchini', 'eggplant', 'cauliflower', 'cabbage', 'asparagus',
            'green beans', 'corn', 'red onion', 'green onions', 'scallions',
            'lemon', 'lime', 'apple', 'banana', 'orange', 'berries', 'avocado'
        },
        'dairy': {
            'milk', 'cheese', 'butter', 'cream', 'yogurt', 'sour cream',
            'cream cheese', 'mozzarella', 'cheddar', 'parmesan', 'feta',
            'heavy cream', 'greek yogurt'
        },
        'pantry': {
            'olive oil', 'vegetable oil', 'cooking spray', 'oil',
            'soy sauce', 'ketchup', 'mustard', 'mayonnaise', 'vinegar',
            'salt', 'pepper', 'black pepper', 'garlic powder', 'onion powder',
            'paprika', 'cumin', 'oregano', 'basil', 'thyme', 'parsley',
            'sugar', 'brown sugar', 'honey', 'maple syrup',
            'broth', 'stock', 'chicken broth', 'vegetable broth',
            'baking powder', 'baking soda', 'vanilla extract'
        }
    }
    
    def __init__(self, name: str, category: Optional[str] = None):
        # Clean the ingredient name and auto-detect category if not provided
        self.name = self._clean_ingredient_name(name)
        self.category = category.lower() if category else self._detect_category()
    
    def _clean_ingredient_name(self, ingredient_str: str) -> str:
       #Clean ingredient string to extract just the ingredient name.
       
        ingredient = ingredient_str.lower().strip()
        
        # Remove measurements at the beginning
        ingredient = re.sub(r'^\d+\s*/?-?\s*\d*\s*', '', ingredient)
        ingredient = re.sub(r'^(cup|cups|tablespoon|tablespoons|teaspoon|teaspoons|tbsp|tsp|pound|pounds|lb|lbs|ounce|ounces|oz|package|packages|jar|can|bottle|serving)\s+', '', ingredient)
        
        # Remove parenthetical content
        ingredient = re.sub(r'\(.*?\)', '', ingredient)
        
        # Remove common descriptors
        descriptors = ['fresh', 'frozen', 'dried', 'ground', 'whole', 'chopped', 'diced', 
                      'minced', 'sliced', 'grated', 'shredded', 'large', 'small', 'medium',
                      'or to taste', 'to taste', 'as needed', 'for garnish', 'optional',
                      'finely', 'thinly', 'softened', 'melted', 'divided', 'beaten']
        
        for desc in descriptors:
            ingredient = re.sub(rf'\b{desc}\b', '', ingredient, flags=re.IGNORECASE)
        
        # Clean up whitespace
        ingredient = re.sub(r'\s+', ' ', ingredient).strip()
        ingredient = ingredient.strip(',').strip()
        
        return ingredient if ingredient else ingredient_str.lower().strip() #If cleaning results in an empty string, return the original lowercased string as a fallback
    
    def _detect_category(self) -> str:
       #Auto-detect the category of the ingredient based on its name using the predefined categories.
        name_lower = self.name.lower()
        
        for category, ingredients in self.CATEGORIES.items(): #Check for exact matches first
            if name_lower in ingredients:
                return category
            
            # Check for partial matches
            for cat_ingredient in ingredients:
                if cat_ingredient in name_lower or name_lower in cat_ingredient:
                    return category
        
        return 'pantry'  # Default to pantry instead of 'other'
    
    def __repr__(self) -> str: #String representation for debugging
        return f"Ingredient(name='{self.name}', category='{self.category}')"
    
    def __str__(self) -> str: #User-friendly string representation (just the name)
        return self.name
    
    def __eq__(self, other) -> bool:
        """Check equality based on ingredient name."""
        if isinstance(other, Ingredient):
            return self.name == other.name
        elif isinstance(other, str):
            return self.name == other.lower().strip()
        return False
    
    def __hash__(self) -> int:
        """Make ingredient hashable for use in sets."""
        return hash(self.name)


class IngredientManager:
    """
Manages a collection of ingredients organized by category. 
Provides methods to add ingredients, retrieve them by category, and display them in an organized manner.
"""
    
    def __init__(self):
        """Initialize an empty IngredientManager."""
        self.ingredients: Dict[str, List[Ingredient]] = {
            category: [] for category in Ingredient.CATEGORIES.keys()
        }
    
    def add_ingredient(self, ingredient: Ingredient) -> None: #Adds a single ingredient to the appropriate category list
        if ingredient.category in self.ingredients:
            #Avoid duplicates
            if ingredient not in self.ingredients[ingredient.category]:
                self.ingredients[ingredient.category].append(ingredient)
        else:
            #If category doesn't exist, add to 'pantry'
            if ingredient not in self.ingredients['pantry']:
                self.ingredients['pantry'].append(ingredient)
    
    def add_ingredients_from_list(self, ingredient_names: List[str]) -> None: #Adds multiple ingredients from a list of names, auto-categorizing them
        for name in ingredient_names:
            if name and name.strip():
                ingredient = Ingredient(name)
                self.add_ingredient(ingredient)
    
    def get_category(self, category: str) -> List[Ingredient]:
        """Get ingredients by category. Returns an empty list if the category doesn't exist or has no ingredients."""
        return self.ingredients.get(category.lower(), [])
    
    def get_all_ingredients(self) -> List[Ingredient]:
        """Get a flat list of all ingredients across all categories."""
        all_ingredients = []
        for category_list in self.ingredients.values():
            all_ingredients.extend(category_list)
        return all_ingredients
    
    def get_ingredient_count(self) -> int:
        """Get the total count of unique ingredients across all categories."""
        return len(self.get_all_ingredients())
    
    def get_category_counts(self) -> Dict[str, int]:
        """
        Get count of ingredients in each category.
        Returns a dictionary with category names as keys and counts as values, only for categories that have at least one ingredient.
        """
        return {
            category: len(ingredients) 
            for category, ingredients in self.ingredients.items()
            if len(ingredients) > 0
        }
    
    def display_by_category(self) -> None:
        """Display all ingredients organized by category."""
        print("\n" + "="*60)
        print("YOUR INGREDIENTS BY CATEGORY")
        print("="*60)
        
        total = 0 # To keep track of total ingredients across all categories
        for category, ingredients in self.ingredients.items():
            if ingredients:
                print(f"\n{category.upper()} ({len(ingredients)}):")
                for ing in sorted(ingredients, key=lambda x: x.name):
                    print(f"  • {ing.name}")
                total += len(ingredients)
        
        print(f"\n{'='*60}")
        print(f"Total ingredients: {total}")
        print("="*60)
    
    def __repr__(self) -> str:
        """String representation of the manager."""
        total = self.get_ingredient_count()
        return f"IngredientManager({total} ingredients)"
    
    def __str__(self) -> str:
        """User-friendly string representation."""
        counts = self.get_category_counts()
        return f"IngredientManager with {sum(counts.values())} ingredients across {len(counts)} categories"


def quick_ingredient_input() -> IngredientManager:
    """
    Simplified ingredient input - just comma-separated list with auto-categorization.
    """
    print("\n" + "="*60)
    print("QUICK INGREDIENT INPUT")
    print("="*60)
    print("Enter all your ingredients separated by commas.")
    print("They will be automatically categorized.\n")
    
    user_input = input("Your ingredients:\n> ").strip()
    
    manager = IngredientManager()
    
    if user_input: # Only process if the user entered something
        ingredient_names = [name.strip() for name in user_input.split(',') if name.strip()]
        manager.add_ingredients_from_list(ingredient_names)
    
    return manager


def load_ingredients_from_csv(csv_filepath: str) -> List[str]:
    """
    Load all unique ingredients from the CSV file using read_csv.py's extract_all_ingredients function.
    This function serves as a bridge to get ingredient data from the CSV for use in the ingredient manager or for other purposes.
    """
    try:
        from scr.diet_filters import extract_all_ingredients
        ingredients = extract_all_ingredients(csv_filepath, sample_size=1000)
        return sorted(list(ingredients)) 
    except ImportError:
        print("Warning: read_csv.py not found. Cannot load ingredients from CSV.")
        return []
    except Exception as e:
        print(f"Error loading ingredients from CSV: {e}")
        return []

    