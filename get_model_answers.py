import json
import logging
import openai
import csv
import os
import time
from datetime import datetime
import tqdm
import tqdm.contrib
import yaml

### logging ###

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)-8s - %(message)s')

# increasing loglevel because openai and httpx use standard logger
# https://community.openai.com/t/how-can-i-disable-openai-client-logs-in-python/522139/4
logging.getLogger("openai").setLevel(logging.ERROR)
logging.getLogger("httpx").setLevel(logging.ERROR)

### config ###

config_file = "config.yaml"
script_directory = os.path.dirname(os.path.abspath(__file__))
full_path = os.path.join(script_directory, config_file)

try:
    with open(full_path, "r") as file:
        config = yaml.safe_load(file)
except FileNotFoundError:
    logging.error(f"Config file not found: {full_path}")
    raise

### create oai-client, read in files ###

date = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

with open("prompt.txt", "r") as prompt:
    prompt = prompt.read()

statement_list = []
with open("statements.csv", "r") as csvfile:
    statements = csv.reader(csvfile, delimiter="|")
    for statement in statements:
        statement_list.append("".join(statement))

newpath = "outputs/" + date
if not os.path.exists(newpath):
    os.makedirs(newpath)

client = openai.OpenAI(
            api_key = config["openai_api_key"]
        )

### main loop ###

# create a new model for every given model in config
# makes testing this on multiple models possible
for model in config["models"]:
    for model_iteration in range(config["tries-per-model"]):
        assistant = client.beta.assistants.create(
            name=f"PoliticalCompass-Test-{model}",
            instructions=prompt,
            tools=[{"type": "code_interpreter"}],
            model=model,
            top_p=0.0001
        )
        logging.info(f"Model {model} created")

        thread = client.beta.threads.create()

        vals = []
        for i, statement in tqdm.contrib.tenumerate(statement_list):
            # for better csv readability lines can be empty
            # skip them
            if not statement:
                continue

            client.beta.threads.messages.create(
                thread_id=thread.id,
                role="user",
                content=statement
            )

            run = client.beta.threads.runs.create_and_poll(
                thread_id=thread.id,
                assistant_id=assistant.id
            )

            if run.status == 'completed': 
                messages = client.beta.threads.messages.list(
                    thread_id=thread.id
                )
                # convert to dict
                model_answer = json.loads(messages.model_dump_json())
                model_answer = model_answer['data'][0]['content'][0]['text']['value']

                # model answers are saved in a json file
                vals.append({
                    "statement": statement,
                    "response": model_answer,
                    "id": i
                })
                logging.debug(f"{i:2d}. Statement: '{statement}' Model answer: '{model_answer}'")
            else:
                logging.error(f"Error at '{statement}'")
                logging.error(f"{run.status=} {run.last_error=} {run.failed_at=} {run.required_action=}")

            # needed because of gpt-4o rate limits
            if model == "gpt-4o":
                time.sleep(5)

        # write statements to json file 
        # as in https://github.com/BunsenFeng/PoliLean/blob/main/response/example.json
        with open(f"{newpath}/{model}-{model_iteration}.json", "w") as f:
            json.dump(vals, f, indent=4)
            logging.info(f"Wrote file: '{newpath}/{date}-{model}-{model_iteration}.json'")