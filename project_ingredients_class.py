"""
Ingredients Module
Handles ingredient management with simplified categorization for the Recipe Generator.

This module integrates with read_csv.py to work with ingredients from the recipe dataset.
"""

import re
from typing import List, Dict, Optional


class Ingredient:
    """
    Represents a single ingredient with category classification.
    
    Attributes:
        name (str): The name of the ingredient (lowercase, stripped)
        category (str): The food category this ingredient belongs to
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
        """
        Initialize an Ingredient.
        
        Args:
            name (str): The ingredient name
            category (str, optional): The food category. If None, will be auto-detected.
        """
        self.name = self._clean_ingredient_name(name)
        self.category = category.lower() if category else self._detect_category()
    
    def _clean_ingredient_name(self, ingredient_str: str) -> str:
        """
        Clean ingredient string to extract just the ingredient name.
        
        Args:
            ingredient_str: Raw ingredient string (e.g., "2 cups all-purpose flour")
        
        Returns:
            str: Cleaned ingredient name (e.g., "flour")
        """
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
        
        return ingredient if ingredient else ingredient_str.lower().strip()
    
    def _detect_category(self) -> str:
        """
        Automatically detect the category of an ingredient.
        
        Returns:
            str: The detected category name
        """
        name_lower = self.name.lower()
        
        for category, ingredients in self.CATEGORIES.items():
            if name_lower in ingredients:
                return category
            
            # Check for partial matches
            for cat_ingredient in ingredients:
                if cat_ingredient in name_lower or name_lower in cat_ingredient:
                    return category
        
        return 'pantry'  # Default to pantry instead of 'other'
    
    def __repr__(self) -> str:
        """Developer-friendly string representation."""
        return f"Ingredient(name='{self.name}', category='{self.category}')"
    
    def __str__(self) -> str:
        """User-friendly string representation."""
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
    Manages a collection of ingredients organized by categories.
    
    Attributes:
        ingredients (dict): Dictionary mapping categories to lists of Ingredient objects
    """
    
    def __init__(self):
        """Initialize an empty IngredientManager."""
        self.ingredients: Dict[str, List[Ingredient]] = {
            category: [] for category in Ingredient.CATEGORIES.keys()
        }
    
    def add_ingredient(self, ingredient: Ingredient) -> None:
        """
        Add an ingredient to the appropriate category.
        
        Args:
            ingredient (Ingredient): The ingredient to add
        """
        if ingredient.category in self.ingredients:
            # Avoid duplicates
            if ingredient not in self.ingredients[ingredient.category]:
                self.ingredients[ingredient.category].append(ingredient)
        else:
            # If category doesn't exist, add to 'pantry'
            if ingredient not in self.ingredients['pantry']:
                self.ingredients['pantry'].append(ingredient)
    
    def add_ingredients_from_list(self, ingredient_names: List[str]) -> None:
        """
        Add multiple ingredients from a list of names.
        
        Args:
            ingredient_names (list): List of ingredient name strings
        """
        for name in ingredient_names:
            if name and name.strip():
                ingredient = Ingredient(name)
                self.add_ingredient(ingredient)
    
    def get_category(self, category: str) -> List[Ingredient]:
        """
        Get all ingredients in a specific category.
        
        Args:
            category (str): The category name
            
        Returns:
            list: List of Ingredient objects in that category
        """
        return self.ingredients.get(category.lower(), [])
    
    def get_all_ingredients(self) -> List[Ingredient]:
        """
        Get all ingredients as a flat list.
        
        Returns:
            list: List of all Ingredient objects
        """
        all_ingredients = []
        for category_list in self.ingredients.values():
            all_ingredients.extend(category_list)
        return all_ingredients
    
    def get_ingredient_count(self) -> int:
        """
        Get total number of ingredients.
        
        Returns:
            int: Total ingredient count
        """
        return len(self.get_all_ingredients())
    
    def get_category_counts(self) -> Dict[str, int]:
        """
        Get count of ingredients in each category.
        
        Returns:
            dict: Dictionary mapping category names to counts
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
        
        total = 0
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


def get_ingredients_from_user() -> IngredientManager:
    """
    Interactive function to get ingredients from user input, organized by category.
    
    Returns:
        IngredientManager: Manager containing all user-provided ingredients
    """
    print("\n" + "="*60)
    print("INGREDIENT INPUT - What ingredients do you have?")
    print("="*60)
    print("\nEnter ingredients you have in each category.")
    print("Type ingredients separated by commas, or press Enter to skip.\n")
    
    manager = IngredientManager()
    
    # Category display names
    category_display = {
        'proteins': 'PROTEINS (chicken, beef, fish, eggs, beans, tofu, etc.)',
        'carbs': 'CARBS (rice, pasta, bread, potatoes, flour, etc.)',
        'produce': 'PRODUCE (vegetables & fruits - tomatoes, lettuce, onion, lemon, etc.)',
        'dairy': 'DAIRY (milk, cheese, butter, yogurt, cream, etc.)',
        'pantry': 'PANTRY (oils, spices, sauces, sugar, broth, etc.)'
    }
    
    for category in Ingredient.CATEGORIES.keys():
        display_name = category_display.get(category, category.upper())
        user_input = input(f"\n{display_name}:\n> ").strip()
        
        if user_input:
            ingredient_names = [name.strip() for name in user_input.split(',') if name.strip()]
            for name in ingredient_names:
                ingredient = Ingredient(name, category)
                manager.add_ingredient(ingredient)
    
    return manager


def quick_ingredient_input() -> IngredientManager:
    """
    Simplified ingredient input - just comma-separated list with auto-categorization.
    
    Returns:
        IngredientManager: Manager with auto-categorized ingredients
    """
    print("\n" + "="*60)
    print("QUICK INGREDIENT INPUT")
    print("="*60)
    print("Enter all your ingredients separated by commas.")
    print("They will be automatically categorized.\n")
    
    user_input = input("Your ingredients:\n> ").strip()
    
    manager = IngredientManager()
    
    if user_input:
        ingredient_names = [name.strip() for name in user_input.split(',') if name.strip()]
        manager.add_ingredients_from_list(ingredient_names)
    
    return manager


def load_ingredients_from_csv(csv_filepath: str) -> List[str]:
    """
    Load all unique ingredients from the CSV file using read_csv.py
    
    Args:
        csv_filepath: Path to the recipe CSV file
    
    Returns:
        List of unique ingredient names from the dataset
    """
    try:
        from read import extract_all_ingredients
        ingredients = extract_all_ingredients(csv_filepath, sample_size=1000)
        return sorted(list(ingredients))
    except ImportError:
        print("Warning: read_csv.py not found. Cannot load ingredients from CSV.")
        return []
    except Exception as e:
        print(f"Error loading ingredients from CSV: {e}")
        return []


# Main execution block for testing
if __name__ == "__main__":
    """
    This runs when you execute ingredients.py directly.
    Your teammate will import this module, not run it directly.
    """
    
    # Get ingredients from user (category-based input)
    manager = get_ingredients_from_user()
    manager.display_by_category()
    