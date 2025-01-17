# AI-Powered Fitness Plan Generator

A FastAPI-based application that generates personalized fitness and nutrition plans using machine learning models. The system takes into account user characteristics such as age, weight, height, gender, activity level, and goals to create customized exercise routines and meal plans.

## Features

- **Personalized Calorie Calculation**: Uses ML models to determine optimal daily caloric intake
- **Macro-nutrient Distribution**: Calculates protein, carbohydrate, and fat ratios based on user goals
- **Exercise Plan Generation**: Creates customized workout plans with:
  - Exercise selection based on fitness level
  - Sets and reps optimization
  - Rest period recommendations
- **Meal Plan Creation**: Generates daily meal plans with:
  - Meal timing distribution
  - Food selection based on nutritional goals
  - Portion size calculations

## Project Structure
fitness_app/
│
├── src/                      # Source code
│   ├── main.py              # FastAPI application
│   ├── data/                # Data generation and training
│   ├── models/              # Trained ML models
│   ├── database/            # Exercise and nutrition data
│   └── utils/               # Helper functions
│
├── tests/                    # Test files
├── data/                     # Data storage
├── notebooks/               # Jupyter notebooks
└── requirements.txt         # Dependencies
## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/fitness-app.git
cd fitness-app
```
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```
3. Install dependencies:
```bash
pip install -r requirements.txt
```
   
