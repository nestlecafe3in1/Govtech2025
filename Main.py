import pandas as pd
import json
import requests
import numpy as np

class Constants:
    restaurant_url = "https://raw.githubusercontent.com/Papagoat/brain-assessment/main/restaurant_data.json"
    country_code_file = "Country-Code.xlsx"
    q1_json_normalize_column = "restaurants"
    q1_left_on = 'restaurant.location.country_id'
    q1_right_on = 'Country Code'
    q1_column_dict = {
        'restaurant.R.res_id': 'Restaurant Id',
        'restaurant.name': 'Restaurant Name',
        'restaurant.location.city': 'City',
        'restaurant.user_rating.votes': 'User Rating Votes',
        'restaurant.user_rating.aggregate_rating': 'User Aggregate Rating',
        'restaurant.cuisines': 'Cuisines'
    }
    q1_selected_columns = [
        'Restaurant Id', 
        'Restaurant Name', 
        'Country', 
        'City', 
        'User Rating Votes', 
        'User Aggregate Rating', 
        'Cuisines'
    ]


class QuestionOne:
    def __init__(self):
        self.restaurant_url = Constants.restaurant_url
        self.country_code_file = Constants.country_code_file
        self.restaurant_data = None

    def extract_json(self):
        response = requests.get(self.restaurant_url)
        if response.ok:
            return response.json()
        else:
            response.raise_for_status()

    def create_json_dataframe(self, column_to_normalize:str):
        json_data = self.extract_json()
        return pd.json_normalize(json_data, column_to_normalize)

    def read_csv(self):
        try:
            return pd.read_excel(self.country_code_file)
        except FileNotFoundError:
            print(f"File not found: {self.country_code_file}")

    def merge_dataframes(self, left_df:pd.DataFrame, right_df:pd.DataFrame, left_on:str, right_on:str, how='left'):
        combined_df = pd.merge(
            left_df, right_df, 
            how=how, left_on=left_on, right_on=right_on
        )
        return combined_df

    def rename_columns(self, df:pd.DataFrame, column_dict:dict):
        return df.rename(columns=column_dict)
    
    def select_columns(self, df, selected_columns: list):
        return df[selected_columns]
    
    def change_datatype():
        

    def run(self):
        base_restaurant_df = self.create_json_dataframe(Constants.q1_json_normalize_column)
        country_code_df = self.read_csv()
        self.restaurant_data = self.merge_dataframes(
            base_restaurant_df, country_code_df, 
            left_on= Constants.q1_left_on, 
            right_on=Constants.q1_right_on
        )
        renamed_df = self.rename_columns(self.restaurant_data, Constants.q1_column_dict)
        filtered_df = self.select_columns(renamed_df, Constants.q1_selected_columns)
        print(filtered_df)


q1 = QuestionOne()
q1.run()