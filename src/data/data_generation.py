import pandas as pd
import numpy as np
import os

def generate_synthetic_data(num_samples=10000):
    np.random.seed(42)
    
    # Generate random user characteristics
    ages = np.random.randint(18, 65, num_samples)
    weights = np.random.normal(115, 15, num_samples)  # in kg
    heights = np.random.normal(190, 10, num_samples)  # in cm
    genders = np.random.choice(['male', 'female'], num_samples)
    activity_levels = np.random.choice(['sedentary', 'light', 'moderate',  'extra'], num_samples)
    goals = np.random.choice(['gain', 'loss'], num_samples)
    
    # Generate target variables
    base_calories = []
    protein_ratios = []
    carb_ratios = []
    fat_ratios = []
    exercise_intensities = []
    
    for i in range(num_samples):
        # BMR calculation with some noise
        if genders[i] == 'male':
            base = (10 * weights[i]) + (6.25 * heights[i]) - (5 * ages[i]) + 5
        else:
            base = (10 * weights[i]) + (6.25 * heights[i]) - (5 * ages[i]) - 161
        
        # Activity level multiplier
        activity_multipliers = {
            'sedentary': 1.2,
            'light': 1.375,
            'moderate': 1.55,
            'very': 1.725,
            'extra': 1.9
        }
        base *= activity_multipliers[activity_levels[i]]
        
        # Goal adjustment
        if goals[i] == 'gain':
            base += 200
        else:
            base -= 500
        
        # Add random noise (±10%)
        base *= np.random.normal(1, 0.1)
        base_calories.append(base)
        
        # Generate macro ratios based on goals
        if goals[i] == 'gain':
            protein_ratio = np.random.normal(0.3, 0.05)  # 30% protein
            fat_ratio = np.random.normal(0.25, 0.05)  # 25% fat
        else:
            protein_ratio = np.random.normal(0.35, 0.05)  # 35% protein
            fat_ratio = np.random.normal(0.2, 0.05)  # 20% fat
        
        carb_ratio = 1 - (protein_ratio + fat_ratio)
        
        protein_ratios.append(protein_ratio)
        carb_ratios.append(carb_ratio)
        fat_ratios.append(fat_ratio)
        
        # Exercise intensity (1-5 scale)
        if activity_levels[i] in ['very', 'extra']:
            intensity = np.random.normal(4, 0.5)
        elif activity_levels[i] == 'moderate':
            intensity = np.random.normal(3, 0.5)
        else:
            intensity = np.random.normal(2, 0.5)
        
        exercise_intensities.append(np.clip(intensity, 1, 5))
    
    # Create DataFrame
    data = pd.DataFrame({
        'age': ages,
        'weight': weights,
        'height': heights,
        'gender': genders,
        'activity_level': activity_levels,
        'goal': goals,
        'target_calories': base_calories,
        'protein_ratio': protein_ratios,
        'carb_ratio': carb_ratios,
        'fat_ratio': fat_ratios,
        'exercise_intensity': exercise_intensities
    })
    
    return data

def save_data(data, filepath='raw/fitness_training_data.csv'):
    # Ensure the parent directory exists
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    # Save the data
    data.to_csv(filepath, index=False)
    print(f"Data generated and saved to {filepath}")

if __name__ == "__main__":
    # Generate and save data
    data = generate_synthetic_data()
    save_data(data)
