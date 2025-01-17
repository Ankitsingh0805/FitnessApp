import random
from typing import List, Dict
from ..database.nutrition_db import FOOD_DATABASE

def generate_meal_plan(target_calories: float, protein_ratio: float, carb_ratio: float, fat_ratio: float) -> List[Dict]:
    meals = []
    meal_distribution = {
        'Breakfast': 0.25,
        'Lunch': 0.35,
        'Dinner': 0.30,
        'Snacks': 0.10
    }

    for meal_name, calorie_ratio in meal_distribution.items():
        meal_calories = target_calories * calorie_ratio
        foods = {}
        current_calories = 0

        available_foods = list(FOOD_DATABASE.keys())
        while current_calories < meal_calories and available_foods:
            food = random.choice(available_foods)
            food_data = FOOD_DATABASE[food]

            calories_needed = meal_calories - current_calories
            grams = min(300, max(50, int(calories_needed / (food_data['calories'] / 100))))

            foods[food] = grams
            current_calories += (food_data['calories'] * grams / 100)
            available_foods.remove(food)

        meals.append({
            'meal_name': meal_name,
            'foods': foods,
            'total_calories': round(current_calories)
        })

    return meals
