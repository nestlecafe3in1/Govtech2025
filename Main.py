import pandas as pd
import json
import requests
import numpy as np

class Q1Constants:
    restaurant_url = "https://raw.githubusercontent.com/Papagoat/brain-assessment/main/restaurant_data.json"
    country_code_file = "Country-Code.xlsx"
    output_file_path = "output/restaurants.csv"
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
        self.restaurant_df = None

    def extract_json(self):
        response = requests.get(self.restaurant_url)
        if response.ok:
            return response.json()
        else:
            response.raise_for_status()

    def create_json_dataframe(self, column_to_normalize:str):
        json_data = self.extract_json()
        return pd.json_normalize(json_data, column_to_normalize)

    def read_csv(self, csv:str):
        try:
            return pd.read_excel(csv)
        except FileNotFoundError:
            print(f"File not found: {csv}")

    def export_df_to_csv(self, df:pd.DataFrame, file_path:str):
        try:
            df.to_csv(file_path, index=False)
            print(f"Restaurant Data exported successfully to {file_path}")
        except Exception as e:
            print(f"Error exporting data: {e}")

    def run(self):
        base_restaurant_df = self.create_json_dataframe(Q1Constants.normalize_record_path)
        country_code_df = self.read_csv(self.country_code_file)
        self.restaurant_df = pd.merge(
            base_restaurant_df, country_code_df, 
            left_on= Q1Constants.left_join_key, right_on=Q1Constants.right_join_key,
            how = "left"
        )
        # Convertion of column datatype to float
        self.restaurant_df[Q1Constants.column_convert] = self.restaurant_df[Q1Constants.column_convert].astype('float64')
        # Rename and select columns before export
        df_to_export = (self.restaurant_df.rename(columns=Q1Constants.columns_to_rename)
                                            [Q1Constants.column_selection]
        )
        self.export_df_to_csv(df_to_export, Q1Constants.output_file_path)

class Q2Constants:
    event_column_to_unpack = 'restaurant.zomato_events'

class QuestionTwo:    
    def __init__(self, restaurant_df):
        self.restaurant_df = restaurant_df

    def column_unpacker(self, df, column_to_unpack):
        # Expand the lists within the column vertically
        expanded_df = df.explode(column_to_unpack)
        # Unpack the dictionaries within the specified column horizontally
        flattened_df = pd.json_normalize(
            expanded_df[column_to_unpack]
        )
        # Join both dataframes back together
        merged_df = (expanded_df.drop("column_to_unpack")
                                .join(flattened_df)
        )
        return merged_df
    
    def month_filter(self)

    def run(self):
        events_unpacked_df = self.column_unpacker(self.restaurant_df, Q2Constants.event_column_to_unpack)
        