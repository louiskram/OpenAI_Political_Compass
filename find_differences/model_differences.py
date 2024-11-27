import os
import json
from itertools import combinations

# Folder where the JSON files are stored
DATA_FOLDER = "outputs/2024-11-27-21-11-47"

def load_json(filepath):
    """Loads a JSON file and returns it as a list of objects."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.loads(f.read())

def get_responses(file):
    """Extracts IDs, responses, and statements from a JSON file."""
    data = load_json(file)
    return {item["id"]: (item["response"], item["statement"]) for item in data}

def compare_all_models(files):
    """Compares responses across all models in the folder."""
    # Load responses from all files
    all_responses = {os.path.basename(f): get_responses(f) for f in files}
    
    # Get all pairwise combinations of files for comparison
    file_pairs = list(combinations(all_responses.keys(), 2))
    differences = []

    # Compare each pair of models
    for file1, file2 in file_pairs:
        responses1 = all_responses[file1]
        responses2 = all_responses[file2]
        
        # Find common IDs
        common_ids = set(responses1.keys()).intersection(set(responses2.keys()))
        
        # Check for disagreements
        for id in common_ids:
            response1, statement = responses1[id]
            response2, _ = responses2[id]
            if response1 != response2:
                differences.append({
                    "id": id,
                    "statement": statement,
                    "file1": file1,
                    "response1": response1,
                    "file2": file2,
                    "response2": response2
                })
    
    return differences

def main():
    # Get all JSON files from the folder
    files = [DATA_FOLDER + "/gpt-4o-mini-0.json", DATA_FOLDER + "/gpt-4o-mini-1.json"]
    
    if len(files) < 2:
        print("At least two JSON files must be present in the 'data' folder.")
        return
    
    print(f"Comparing {len(files)} files: {', '.join([os.path.basename(f) for f in files])}")
    
    # Compare all models
    differences = compare_all_models(files)
    
    # Output differences
    print("\nDisagreements between models:")
    for diff in differences:
        print(f"ID: {diff['id']}\nStatement: {diff['statement']}\n"
              f"File 1 ({diff['file1']}): {diff['response1']}\n"
              f"File 2 ({diff['file2']}): {diff['response2']}\n")
    
    print(f"Number of disagreements: {len(differences)}")

if __name__ == "__main__":
    main()
