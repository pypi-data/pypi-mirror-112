import json
import sys


class Config:
    DEFAULT_CONFIG_DATA = {
        "api_key": "",
    }

    def __init__(self, config_file="config.json", create_config_if_not_found=True):
        self.config_file = config_file
        self.create_config_if_not_found = create_config_if_not_found
        self.config = {}

        self.load_config_file()

    def get(self, key):
        return self.config.get(key)

    def load_config_file(self):
        try:
            with open(self.config_file, "r", encoding="utf-8") as f:
                self.config = json.load(f)
        except FileNotFoundError as e:
            if self.create_config_if_not_found:
                self.create_default_config_file()
            else:
                raise e

    def write_config_file(self):
        with open(self.config_file, "w", encoding="utf-8") as f:
            json.dump(self.config, f, indent=2)

    def get_config(self):
        if not self.config:
            self.load_config_file()

        return self.config

    def create_default_config_file(self):
        self.config = self.DEFAULT_CONFIG_DATA
        self.write_config_file()
        print("[!] Config file created, Please fill the required data and rerun the script.")
        sys.exit()
