import pickle
import pandas as pd
from sklearn.preprocessing import OneHotEncoder

# Step 1: Train the encoders
def train_and_save_encoders():
    # Define the training data for categorical columns
    gender_data = [["male"], ["female"]]
    activity_level_data = [["sedentary"], ["active"], ["very active"]]

    # Train the OneHotEncoders
    gender_encoder = OneHotEncoder(sparse_output=False, handle_unknown="ignore")
    activity_level_encoder = OneHotEncoder(sparse_output=False, handle_unknown="ignore")

    gender_encoder.fit(gender_data)
    activity_level_encoder.fit(activity_level_data)

    # Create a dictionary mapping column names to their encoders
    encoders = {
        "gender": gender_encoder,
        "activity_level": activity_level_encoder,
    }

    # Save the encoders to a file
    with open("src/data/models/encoder.pkl", "wb") as f:
        pickle.dump(encoders, f)

    print("Encoders trained and saved successfully.")

# Step 2: Verify encoder functionality
def verify_encoders():
    with open("src/data/models/encoder.pkl", "rb") as f:
        encoders = pickle.load(f)

    # Prepare sample input data for verification
    sample_data = pd.DataFrame({
        "gender": ["male"],
        "activity_level": ["sedentary"]
    })

    # Transform sample data
    print("\nVerifying Encoders:")
    for column in encoders.keys():
        encoder = encoders[column]
        transformed = encoder.transform(sample_data[[column]])
        print(f"Encoded '{column}':\n", transformed)

# Step 3: Load encoders and transform new input data
def transform_input_data():
    # Load the encoders
    with open("src/data/models/encoder.pkl", "rb") as f:
        encoders = pickle.load(f)

    # Prepare input data
    input_data = pd.DataFrame({
        "gender": ["female"],
        "activity_level": ["active"]
    })

    # Transform input data using loaded encoders
    print("\nTransforming Input Data:")
    for column in encoders.keys():
        if column in input_data.columns:
            encoder = encoders[column]
            encoded_array = encoder.transform(input_data[[column]])
            encoded_columns = encoder.get_feature_names_out([column])
            encoded_df = pd.DataFrame(encoded_array, columns=encoded_columns)

            # Add encoded columns to input data and drop the original column
            input_data = pd.concat([input_data, encoded_df], axis=1).drop(column, axis=1)

    print("Transformed Input Data:\n", input_data)

# Main function to execute all steps
if __name__ == "__main__":
    # Ensure directory exists
    import os
    os.makedirs("src/data/models", exist_ok=True)

    print("Training and Saving Encoders...")
    train_and_save_encoders()

    print("\nVerifying Encoders...")
    verify_encoders()

    print("\nTransforming New Input Data...")
    transform_input_data()
