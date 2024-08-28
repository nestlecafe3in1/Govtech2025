import pandas as pd
import json
import requests
import numpy as np

class Constants:
    restaurant_url = "https://raw.githubusercontent.com/Papagoat/brain-assessment/main/restaurant_data.json"
    country_code_file = "Country-Code.xlsx"


class QuestionOne:
    def __init__(self):
        self.restaurant_url = Constants.restaurant_url
        self.country_code_file = Constants.country_code_file

    def extract_json(self):
        response = requests.get(self.restaurant_url)
        if response.ok:
            return response.json()
        else:
            response.raise_for_status()

    def normalize_json(self, column_to_normalize):
        json_data = self.extract_json()
        return pd.json_normalize(json_data, column_to_normalize)

    def read_csv(self):
        try:
            return pd.read_excel(self.country_code_file)
        except FileNotFoundError:
            print(f"File not found: {self.country_code_file}")

    def
    
    def run(self):
        base_restaurant_df = self.normalize_json()
        country_code_df = self.read_csv()
    
