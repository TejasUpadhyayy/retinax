import os
import pandas as pd
import numpy as np

# Define paths
train_label_file = r"C:\Users\upadh\Documents\IDRiD_Disease_Grading\train\a. IDRiD_Disease Grading_Training Labels.csv"  # Replace with the path to your training labels CSV
test_label_file = r"C:\Users\upadh\Documents\IDRiD_Disease_Grading\test\b. IDRiD_Disease Grading_Testing Labels.csv"  # Replace with the path to your testing labels CSV
train_output_dir = r"C:\Users\upadh\Documents\IDRiD_Disease_Grading\train\Processed_train_labels"
test_output_dir = r"C:\Users\upadh\Documents\IDRiD_Disease_Grading\test\Processed_test_labels"

# Create output directories if they don't exist
os.makedirs(train_output_dir, exist_ok=True)
os.makedirs(test_output_dir, exist_ok=True)

# Function to process labels
def process_labels(label_file, output_dir):
    labels = pd.read_csv(label_file)  # Load the CSV file
    labels.columns = labels.columns.str.strip()  # Remove extra spaces from column names
    print("Available Columns in CSV:", labels.columns)  # Debug: print column names to verify
    
    # Define column names
    dr_column = "Retinopathy grade"
    dme_column = "Risk of macular edema"

    # Validate column names
    if dr_column not in labels.columns or dme_column not in labels.columns:
        raise KeyError(f"Expected columns '{dr_column}' and/or '{dme_column}' not found in the CSV.")

    # Extract labels
    dr_labels = labels[dr_column].to_numpy()
    dme_labels = labels[dme_column].to_numpy()
    
    # Save the labels as NumPy arrays
    np.save(os.path.join(output_dir, "dr_labels.npy"), dr_labels)
    np.save(os.path.join(output_dir, "dme_labels.npy"), dme_labels)
    print(f"Processed labels saved to {output_dir}")

# Process training labels
process_labels(train_label_file, train_output_dir)

# Process testing labels
process_labels(test_label_file, test_output_dir)