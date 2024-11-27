import logging
import os
import yaml

class ConfigLoader:
    def __init__(self, config_file):
        """
        Loads the configuration from the config file.
        """
        script_directory = os.path.dirname(os.path.abspath(__file__))
        full_path = os.path.join(script_directory, config_file)

        try:
            with open(full_path, "r") as file:
                self.data = yaml.safe_load(file)
            logging.info("Configuration loaded successfully")
        except FileNotFoundError:
            logging.error(f"Config file not found: {full_path}")
            raise

    def __getitem__(self, key):
        return self.data[key]