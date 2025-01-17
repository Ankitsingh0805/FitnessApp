import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.ensemble import RandomForestRegressor
import pickle
import os

def prepare_data(file_path):
    data = pd.read_csv(file_path)

    features = ['age', 'weight', 'height', 'gender', 'activity_level', 'goal']
    targets = ['target_calories', 'protein_ratio', 'carb_ratio', 'fat_ratio', 'exercise_intensity']

    numeric_features = ['age', 'weight', 'height']
    categorical_features = ['gender', 'activity_level', 'goal']

    numeric_transformer = StandardScaler()
    categorical_transformer = Pipeline(steps=[
        ('encoder', OneHotEncoder(handle_unknown='ignore'))
    ])
    
    preprocessing = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, numeric_features),
            ('cat', categorical_transformer, categorical_features)
        ]
    )

    X_transformed = preprocessing.fit_transform(data[features])

    cat_feature_names = preprocessing.transformers_[1][1].named_steps['encoder'].get_feature_names_out(categorical_features)
    all_feature_names = numeric_features + list(cat_feature_names)

    X = pd.DataFrame(X_transformed, columns=all_feature_names)
    y = {target: data[target] for target in targets}
    
    # Extract the encoder from the preprocessing pipeline
    encoder = preprocessing.transformers_[1][1].named_steps['encoder']
    
    return data, features, targets, preprocessing, encoder, X, y


def train_models(data, features, targets, X, y):
    models = {}
    for target in targets:
        model = RandomForestRegressor(random_state=42)
        model.fit(X, y[target]) 
        models[target] = model
    return models


def save_models(models, preprocessing):
    try:
        # Ensure the directory exists
        os.makedirs('./models', exist_ok=True)
        print("Saving models...")

        # Save the preprocessing pipeline
        with open('./models/preprocessing.pkl', 'wb') as f:
            pickle.dump(preprocessing, f)

        # Extract and save the encoders for individual features
        encoders = {
            'gender': preprocessing.transformers_[1][1].named_steps['encoder'],
            'activity_level': preprocessing.transformers_[1][1].named_steps['encoder'],
            'goal': preprocessing.transformers_[1][1].named_steps['encoder']
        }

        # Save the encoders separately
        with open('./models/encoders.pkl', 'wb') as f:
            pickle.dump(encoders, f)

        # Save each model separately
        for target_name, model in models.items():
            model_path = f'./models/{target_name}_model.pkl'
            with open(model_path, 'wb') as f:
                pickle.dump(model, f)

        print("Models, preprocessing, and encoders saved successfully.")
    except Exception as e:
        print(f"Error while saving models: {e}")

def predict(models, input_data, features, preprocessing, encoder):
    X_input = preprocessing.transform(input_data)

    num_features = ['age', 'weight', 'height']
    cat_features = encoder.get_feature_names_out(['gender', 'activity_level', 'goal'])
    all_features = num_features + list(cat_features)
    X_input_df = pd.DataFrame(X_input, columns=all_features)
    
    predictions = {}
    for target_name, model in models.items():
        predictions[target_name] = model.predict(X_input_df)
    
    return predictions


def main(): 
    try:
        data, features, targets, preprocessing, encoder, X, y = prepare_data('./fitness_training_data.csv')

        models = train_models(data, features, targets, X, y)
        
        # Save models, preprocessing pipeline, and encoder
        save_models(models, preprocessing)
        
        # Example input data in the same format as your database
        new_data = pd.DataFrame({
            'age': [25],
            'weight': [70],
            'height': [175],
            'gender': ['male'],  # Textual gender
            'activity_level': ['moderate'],  # Textual activity level
            'goal': ['gain']  # Textual goal
        })
        
        # Load models and preprocessing pipeline
        with open('./models/preprocessing.pkl', 'rb') as f:
            loaded_preprocessing = pickle.load(f)
        
        # Load the encoder separately
        with open('./models/encoder.pkl', 'rb') as f:
            loaded_encoder = pickle.load(f)
        
        loaded_models = {}
        for target_name in targets:
            with open(f'./models/{target_name}_model.pkl', 'rb') as f:
                loaded_models[target_name] = pickle.load(f)
        
        # Make predictions
        predictions = predict(loaded_models, new_data, features, loaded_preprocessing, loaded_encoder)
        print("Predictions:", predictions)
    
    except Exception as e:
        print(f"Error during training or prediction: {e}")

if __name__ == "__main__":
    main()










