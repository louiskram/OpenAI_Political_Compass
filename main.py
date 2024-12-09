import json
import logging
import openai
import csv
import os
from datetime import datetime
from tqdm.contrib import tenumerate
import yaml

def setup_logging():
    """Configure logging."""
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)-8s - %(message)s')
    logging.getLogger("openai").setLevel(logging.ERROR)
    logging.getLogger("httpx").setLevel(logging.ERROR)

def load_config(config_path):
    """Load and return the configuration from a YAML file."""
    try:
        with open(config_path, "r") as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        logging.error(f"Config file not found: {config_path}")
        raise

def read_file(file_path):
    """Read and return the content of a text file."""
    with open(file_path, "r") as file:
        return file.read()

def read_statements(csv_file_path):
    """Read and return statements from a CSV file."""
    statements = []
    with open(csv_file_path, "r") as csvfile:
        reader = csv.reader(csvfile, delimiter="|")
        for statement in reader:
            statements.append("".join(statement))
    return statements

def create_output_directory(base_path):
    """Create a directory for the output files if it doesn't exist."""
    if not os.path.exists(base_path):
        os.makedirs(base_path)

def create_openai_client(api_key):
    """Create and return an OpenAI client."""
    return openai.OpenAI(api_key=api_key)

def process_statements(client, prompt, statements, models, tries_per_model, output_base_path):
    """Process statements using OpenAI models and save the responses."""
    for model in models:
        for model_iteration in range(tries_per_model):
            logging.info(f"Model {model} created")
            _ = client.beta.threads.create()
            results = []

            for i, statement in tenumerate(statements):
                completion = client.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": prompt},
                        {"role": "user", "content": statement}
                    ],
                    top_p=1e-11  # Making the model response deterministic.
                )
                response = completion.choices[0].message.content
                results.append({"statement": statement, "response": response, "id": i})
                logging.debug(f"{i:2d}. Statement: '{statement}' Model answer: '{response}'")

            output_filepath = os.path.join(output_base_path, f"{model}-{model_iteration}.json")
            with open(output_filepath, "w") as f:
                json.dump(results, f, indent=4)
            logging.info(f"Wrote file: '{output_filepath}'")

def main():
    setup_logging()

    script_directory = os.path.dirname(os.path.abspath(__file__))
    config_file = "config.yaml"
    config_path = os.path.join(script_directory, config_file)
    config = load_config(config_path)

    prompt = read_file("prompt.txt")
    statements = read_statements("statements.csv")

    date = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    output_base_path = os.path.join("outputs", date)
    create_output_directory(output_base_path)

    client = create_openai_client(config["openai_api_key"])
    process_statements(client, prompt, statements, config["models"], config["tries-per-model"], output_base_path)

if __name__ == "__main__":
    main()