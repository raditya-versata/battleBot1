import json

class key_helper:
    def __init__(self):
        self.keys = json.load(open("../config.json", "r", encoding="utf8"))

    def mongo_uri(self):
        return self.keys["mongo_uri"]

    def openai_key(self):
        return self.keys["openai_key"]