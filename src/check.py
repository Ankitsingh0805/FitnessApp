import os
import pickle

def check_files(model_files):
    """
    Check if the required model files exist and are not corrupted.

    :param model_files: List of model files to check.
    :return: None
    """
    for file_path in model_files:
        if not os.path.exists(file_path):
            print(f"File missing: {file_path}")
            return False
        else:
            try:
                # Try loading the file to check if it is corrupted
                with open(file_path, 'rb') as f:
                    pickle.load(f)
                print(f"File loaded successfully: {file_path}")
            except (pickle.UnpicklingError, IOError) as e:
                print(f"Error loading file {file_path}: {e}")
                return False
    return True


model_files = [
    './src/data/models/preprocessing.pkl',  # Correct relative path
    './src/data/models/encoder.pkl',
    './src/data/models/target_calories_model.pkl',
    './src/data/models/protein_ratio_model.pkl',
    './src/data/models/carb_ratio_model.pkl',
    './src/data/models/fat_ratio_model.pkl',
    './src/data/models/exercise_intensity_model.pkl'
]

# Check the files
if check_files(model_files):
    print("All files are present and not corrupted.")
else:
    print("One or more files are missing or corrupted.")
