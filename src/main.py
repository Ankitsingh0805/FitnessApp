import logging
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
import pickle
import os

from src.utils.exercise_generator import generate_exercise_plan
from src.utils.meal_planner import generate_meal_plan

logging.basicConfig(level=logging.DEBUG)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class UserInput(BaseModel):
    age: int
    weight: float
    height: float
    gender: str
    activity_level: str
    goal: str

def load_models(model_dir='src/data/models'):
    models = {}
    for target in ['target_calories', 'protein_ratio', 'carb_ratio', 'fat_ratio', 'exercise_intensity']:
        try:
            with open(f'{model_dir}/{target}_model.pkl', 'rb') as f:
                models[target] = pickle.load(f)
        except FileNotFoundError:
            logging.error(f"Model file for {target} not found")
            raise HTTPException(status_code=500, detail=f"Model file for {target} not found")

    try:
        with open(f'{model_dir}/preprocessing.pkl', 'rb') as f:
            preprocessing = pickle.load(f)
    except FileNotFoundError:
        logging.error("Preprocessing pipeline not found")
        raise HTTPException(status_code=500, detail="Preprocessing pipeline not found")

    return models, preprocessing

@app.post("/api/fitness-plan")
async def get_fitness_plan(user_input: UserInput):
    try:
        # Load models and preprocessing
        models, preprocessing = load_models()

        # Prepare input data
        input_data = pd.DataFrame({
            'age': [user_input.age],
            'weight': [user_input.weight],
            'height': [user_input.height],
            'gender': [user_input.gender],
            'activity_level': [user_input.activity_level],
            'goal': [user_input.goal]
        })

        # Transform input data
        X_transformed = preprocessing.transform(input_data)

        # Reconstruct feature names
        numeric_features = ['age', 'weight', 'height']
        cat_features = ['gender', 'activity_level', 'goal']
        
        cat_feature_names = preprocessing.transformers_[1][1].named_steps['encoder'].get_feature_names_out(cat_features)
        all_feature_names = numeric_features + list(cat_feature_names)
        
        X_input_df = pd.DataFrame(X_transformed, columns=all_feature_names)

        # Make predictions
        predictions = {}
        for target, model in models.items():
            predictions[target] = float(model.predict(X_input_df)[0])

        # Generate plans
        exercise_plan = generate_exercise_plan(predictions['exercise_intensity'])
        meal_plan = generate_meal_plan(
            predictions['target_calories'],
            predictions['protein_ratio'],
            predictions['carb_ratio'],
            predictions['fat_ratio']
        )

        return {
            "predictions": {
                "target_calories": round(predictions['target_calories']),
                "protein_ratio": round(predictions['protein_ratio'] * 100, 1),
                "carb_ratio": round(predictions['carb_ratio'] * 100, 1),
                "fat_ratio": round(predictions['fat_ratio'] * 100, 1),
                "exercise_intensity": round(predictions['exercise_intensity'], 1)
            },
            "exercise_plan": exercise_plan,
            "meal_plan": meal_plan
        }
    except Exception as e:
        logging.error(f"Error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)





