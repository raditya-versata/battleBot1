import fnmatch
import json
import os
from html2text import html2text
import re


class article_cleaner:
    def __init__(self):
        self.relative_path = "../"
        self.input_dir = "_input/articles/"
        self.output_dir = "_output/articles/"


    def clean(self):
        matches = []
        for dir_path, dir_names, filenames in os.walk(self.relative_path + self.input_dir):
            for filename in fnmatch.filter(filenames, "*.json"):
                matches.append(os.path.join(dir_path, filename))
                self.clean_article(matches[-1])
        return matches

    def clean_article(self, article_path):
        """
        Extract JSON content, convert HTML to Markdown and save the Markdown file.
        """
        # Load the JSON file
        print(f"converting article {article_path}")
        with open(article_path, 'r') as file:
            content = json.load(file)

        # Get HTML content
        html_content = content.get('body')

        # Convert HTML to Markdown
        md_content = html2text(html_content)

        # Output file path
        base_name = os.path.basename(article_path)
        file_name = os.path.splitext(base_name)[0]
        output_file_path = os.path.join(self.relative_path + self.output_dir, f'{file_name}.md')

        # Save the Markdown content
        with open(output_file_path, 'w') as file:
            file.write(md_content)

    # List of common navigational phrases to remove
    common_nav_phrases = ['Back to top']

    def convert_to_plain_text(self):
        for filename in os.listdir(os.path.join(self.relative_path, self.input_dir)):
            if filename.endswith('.json'):
                with open(os.path.join(self.relative_path, self.input_dir, filename)) as file:
                    data = json.load(file)
                    content = data.get('body', '')  # Fetching content from 'body' instead of 'content'

                # Convert HTML content to plain text
                plain_text_content = html2text(content)

                # Remove common navigational phrases
                for phrase in self.common_nav_phrases:
                    plain_text_content = plain_text_content.replace(phrase, '')

                # Compressed the content by removing leading and trailing whitespaces
                compressed_content = " ".join(plain_text_content.split())

                # Change the extension to .txt for new file
                txt_filename = os.path.splitext(filename)[0] + '.txt'

                # Write converted content to new file in output directory
                with open(os.path.join(self.relative_path, self.output_dir, txt_filename), 'w') as file:
                    file.write(compressed_content)

if __name__ == '__main__':
    cleaner = article_cleaner()
    cleaner.clean()
    cleaner.convert_to_plain_text()
