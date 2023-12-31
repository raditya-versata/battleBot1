import json

import tiktoken
from typing import List
import os
import pandas as pd

class TextFileTokenCounter:

    def __init__(self):
        self.encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")

    def count_tokens_in_text(self, text: str) -> int:
        tokens = self.encoding.encode(text)
        return len(tokens)

    def count_tokens_in_file(self, filename: str) -> int:
        with open(filename, "r") as file:
            text = file.read()
        return self.count_tokens_in_text(text)

    def count_tokens_in_directory(self, dir_name: str) -> List[int]:
        token_counts = []
        for filename in os.listdir(dir_name):
            if filename.endswith(".txt"):
                full_path = os.path.join(dir_name, filename)
                token_count = self.count_tokens_in_file(full_path)
                token_counts.append((filename, token_count))
        return token_counts

    def save_results(self, token_counts: List[int], filename: str):
        with open(filename, 'w') as file:
            json.dump(token_counts, file)

    def print_summary(self, token_counts: List[int], cost_per_1k_tokens=0.01):
        total_tokens = sum(token for _, token in token_counts)
        total_cost = (total_tokens / 1000) * cost_per_1k_tokens
        print(f"Total tokens: {total_tokens}")
        print(f"Estimated cost: ${total_cost:.2f}")

if __name__ == "__main__":
    counter = TextFileTokenCounter()
    directory = "../_output/articles"  # specify the correct path
    token_counts = counter.count_tokens_in_directory(directory)
    counter.save_results(token_counts, f"../_output/token_counts.json")
    counter.print_summary(token_counts, 0.0010)