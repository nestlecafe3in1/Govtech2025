import pandas as pd
import json
import requests
import numpy as np


class Q1Constants:
    restaurant_url = "https://raw.githubusercontent.com/Papagoat/brain-assessment/main/restaurant_data.json"
    country_code_file = "Country-Code.xlsx"
    normalize_record_path = "restaurants"
    left_join_key = 'restaurant.location.country_id'
    right_join_key = 'Country Code'
    columns_to_rename = {
        'restaurant.R.res_id': 'Restaurant Id',
        'restaurant.name': 'Restaurant Name',
        'restaurant.location.city': 'City',
        'restaurant.user_rating.votes': 'User Rating Votes',
        'restaurant.user_rating.aggregate_rating': 'User Aggregate Rating',
        'restaurant.cuisines': 'Cuisines'
    }
    column_convert = "restaurant.user_rating.aggregate_rating"
    column_selection = [
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
        self.restaurant_url = Q1Constants.restaurant_url
        self.country_code_file = Q1Constants.country_code_file
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

    def read_csv(self, csv):
        try:
            return pd.read_excel(csv)
        except FileNotFoundError:
            print(f"File not found: {csv}")

    def merge_dataframes(
            self, left_df:pd.DataFrame, 
            right_df:pd.DataFrame, left_on:str, 
            right_on:str, how='left'):

        combined_df = pd.merge(
            left_df, right_df, 
            how=how, left_on=left_on, right_on=right_on
        )
        return combined_df
    
    def convert_column_datatype(self, df:pd.DataFrame,column, datatype:str):
        df[column] = df[column].astype(datatype)
        return df

    def run(self):
        base_restaurant_df = self.create_json_dataframe(Q1Constants.normalize_record_path)
        country_code_df = self.read_csv(self.country_code_file)
        self.restaurant_data = self.merge_dataframes(
            base_restaurant_df, country_code_df, 
            left_on= Q1Constants.left_join_key, right_on=Q1Constants.right_join_key
        )
        self.restaurant_data = self.convert_column_datatype(self.restaurant_data, Q1Constants.column_convert, 'float64')
        df_to_export = (self.restaurant_data.rename(columns=Q1Constants.columns_to_rename)
                                            [Q1Constants.column_selection]
        )
        print(df_to_export.info())

q1 = QuestionOne()
q1.run()