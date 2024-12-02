import os
import json
import numpy as np
import pandas as pd
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay

# Folder where the JSON files are stored
DATA_FOLDER = "outputs/2024-11-27-18-59-32"

def load_json(filepath):
    """Loads a JSON file and returns it as a list of objects."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.loads(f.read())

def get_responses(file):
    """Extracts IDs, responses, and statements from a JSON file."""
    data = load_json(file)
    return {item["id"]: (item["response"], item["statement"]) for item in data}

def compare_models(file1, file2):
    """Compares the responses of two models."""
    responses1 = get_responses(file1)
    responses2 = get_responses(file2)
    
    common_ids = set(responses1.keys()).intersection(set(responses2.keys()))
    
    model1_responses = [responses1[i][0] for i in common_ids]
    model2_responses = [responses2[i][0] for i in common_ids]
    
    statements = {i: responses1[i][1] for i in common_ids}  # Extract the statements
    
    return model1_responses, model2_responses, common_ids, responses1, responses2, statements

def find_disagreements(common_ids, responses1, responses2, statements):
    """Finds IDs, responses, and statements where models disagree."""
    disagreements = [
        (id, statements[id], responses1[id][0], responses2[id][0]) 
        for id in common_ids 
        if responses1[id][0] != responses2[id][0]
    ]
    return disagreements

def generate_confusion_matrix(responses1, responses2, labels=None):
    """Generates a confusion matrix based on the responses of two models."""
    cm = confusion_matrix(responses1, responses2, labels=labels)
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=labels)
    disp.plot(cmap="Blues", colorbar=True)
    return cm

def main():
    # Load all JSON files from the folder
    files = [os.path.join(DATA_FOLDER, f) for f in os.listdir(DATA_FOLDER) if f.endswith('.json')]
    
    if len(files) < 2:
        print("At least two JSON files must be present in the 'data' folder.")
        return
    
    # Compare two specific files (can be adjusted)
    file1, file2 = files[0], files[1]
    print(f"Comparing files: {file1} and {file2}")
    
    responses1, responses2, common_ids, full_responses1, full_responses2, statements = compare_models(file1, file2)
    
    # Identify all possible labels (e.g., "Strong Agree", "Disagree", etc.)
    all_labels = sorted(set(responses1).union(set(responses2)))
    
    # Generate the confusion matrix
    print("Generating confusion matrix...")
    cm = generate_confusion_matrix(responses1, responses2, labels=all_labels)
    print("Confusion Matrix:")
    print(pd.DataFrame(cm, index=all_labels, columns=all_labels))
    
    # Find and display disagreements
    print("\nDisagreements between the models:")
    disagreements = find_disagreements(common_ids, full_responses1, full_responses2, statements)
    for id, statement, response1, response2 in disagreements:
        print(f"ID: {id}\nStatement: {statement}\nModel 1: {response1}\nModel 2: {response2}\n")
    
    print(f"Number of disagreements: {len(disagreements)}")

if __name__ == "__main__":
    main()
