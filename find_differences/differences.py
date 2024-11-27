import os
import json

def load_json(filepath):
    """Loads a JSON file and returns it as a list of objects."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.loads(f.read())

def compare_responses(folder_path):
    """Vergleicht Antworten in allen JSON-Dateien innerhalb eines Ordners."""
    # Alle JSON-Dateien im Ordner sammeln
    files = [f for f in os.listdir(folder_path) if f.endswith('.json')]
    data = {}
    
    # Alle Dateien durchgehen und Inhalte in data speichern
    for file in files:
        file_path = os.path.join(folder_path, file)
        content = load_json(file_path)
        for item in content:
            statement_id = item['id']
            statement_text = item['statement']
            response = item['response']
            
            # Struktur für Vergleiche initialisieren
            if statement_id not in data:
                data[statement_id] = {
                    "statement": statement_text,
                    "responses": {}
                }
            data[statement_id]["responses"][file] = response
    
    return data

def group_identical_responses(responses):
    """Gruppiert identische Antworten zusammen."""
    grouped = {}
    for file, response in responses.items():
        if response not in grouped:
            grouped[response] = []
        grouped[response].append(file)
    return grouped

def generate_output(data):
    """Erstellt einen stringbasierten Bericht über die Unterschiede."""
    output = []
    for statement_id, details in data.items():
        responses = details["responses"]
        # Prüfen, ob Unterschiede zwischen Antworten existieren
        if len(set(responses.values())) > 1:
            output.append(f"ID: {statement_id}")
            output.append(f"Statement: {details['statement']}")
            
            # Gruppiere identische Antworten
            grouped_responses = group_identical_responses(responses)
            for response, files in grouped_responses.items():
                # Sortiere die Dateinamen
                files.sort()
                # Verbinde die Dateinamen mit Kommas
                files_str = ", ".join(files)
                output.append(f"{files_str}: {response}")
            
            output.append("") # Leerzeile für bessere Lesbarkeit
    
    return "\n".join(output)

def main():
    folder_path = "outputs/2024-11-27-21-11-47" # Ordner mit JSON-Dateien
    data = compare_responses(folder_path)
    differences = generate_output(data)
    print(differences)

if __name__ == "__main__":
    main()