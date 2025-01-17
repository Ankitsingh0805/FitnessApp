from src.database.exercise_db import EXERCISE_DATABASE
from src.database.nutrition_db import FOOD_DATABASE
def validate_exercise_db():
    # Check if all categories exist in the EXERCISE_DATABASE
    required_categories = ['push', 'pull', 'legs', 'core', 'cardio']
    for category in required_categories:
        if category not in EXERCISE_DATABASE:
            print(f"Missing category: {category}")
            return False
        if not isinstance(EXERCISE_DATABASE[category], list):
            print(f"Invalid type for {category}: Expected list, got {type(EXERCISE_DATABASE[category])}")
            return False
        if not all(isinstance(exercise, str) for exercise in EXERCISE_DATABASE[category]):
            print(f"Invalid value in {category}: Expected string, found non-string values.")
            return False
    print("Exercise database is valid.")
    return True


def validate_food_db():
    # Check if each food item has the required nutritional keys
    required_keys = ['calories', 'protein', 'carbs', 'fats']
    for food, nutrients in FOOD_DATABASE.items():
        if not isinstance(nutrients, dict):
            print(f"Invalid structure for food: {food}. Expected a dictionary, got {type(nutrients)}")
            return False
        for key in required_keys:
            if key not in nutrients:
                print(f"Missing '{key}' for food item: {food}")
                return False
            if not isinstance(nutrients[key], (int, float)):
                print(f"Invalid value for '{key}' in {food}: Expected number, found {type(nutrients[key])}")
                return False
    print("Food database is valid.")
    return True


# Example Usage
if __name__ == "__main__":
    if validate_exercise_db() and validate_food_db():
        print("Both exercise and food databases are valid!")
    else:
        print("Database validation failed.")
