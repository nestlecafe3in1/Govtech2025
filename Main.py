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
        # Rename columns to be more presentable
        self.restaurant_df = self.restaurant_df.rename(columns=Q1Constants.columns_to_rename)

        df_to_export = self.restaurant_df[Q1Constants.column_selection]
        self.export_df_to_csv(df_to_export, Q1Constants.output_file_path)

class Q2Constants:
    output_file_path = "output/restaurant_events.csv"
    event_column_to_unpack = 'restaurant.zomato_events'
    column_start_date = 'event.start_date'
    column_end_date = 'event.end_date'
    specified_month = 4
    specified_year = 2019
    photos_column_to_unpack = "event.photos"
    column_selection = [
        "event.event_id", "Restaurant Id", 
        "Restaurant Name", "restaurant.photos_url",
        "event.title", "event.start_date", 
        "event.end_date"
        ]
    columns_to_rename = {
        "event.event_id": "Event Id", 
        "restaurant.photos_url": "Photo URL",
        "event.title": "Event Title", 
        "event.start_date": "Event Start Date",
        "event.end_date": "Event End Date"
        }   


class QuestionTwo(QuestionOne):    
    def __init__(self, restaurant_df):
        super().__init__()
        self.restaurant_df = restaurant_df


    def column_unpacker(self, df:pd.DataFrame, column_to_unpack:str):
        # Expand the lists within the column vertically
        expanded_df = df.explode(column_to_unpack)
        # Unpack the dictionaries within the specified column horizontally
        flattened_df = pd.json_normalize(
            expanded_df[column_to_unpack]
            )
        # Join both dataframes back together
        merged_df = expanded_df.join(flattened_df)
        return merged_df
    
    def month_filter(
            self, df:pd.DataFrame, 
            column_start_date:str, column_end_date:str,
            year:int, month:int): 
        # Convert both columns to datetime  
        df[column_start_date] = pd.to_datetime(df[column_start_date])
        df[column_end_date] = pd.to_datetime(df[column_end_date])

        # Condition for event to take place within specified month
        before_year = (df[column_start_date].dt.year < year)
        before_or_in_month_year = (
            (df[column_start_date].dt.year == year) & (df[column_start_date].dt.month <= month)
            )
        starts_before_date = (before_year | before_or_in_month_year)

        after_year = (df[column_end_date].dt.year > year)
        after_or_in_month_year = (
            (df[column_end_date].dt.year == year) & (df[column_end_date].dt.month >= month)
            )
        ends_after_date = (after_year | after_or_in_month_year)

        condition = (ends_after_date & starts_before_date)
        return df[condition]

    def run(self):
        events_unpacked_df = self.column_unpacker(self.restaurant_df, Q2Constants.event_column_to_unpack)
        filtered_event_df = self.month_filter(
            events_unpacked_df, Q2Constants.column_start_date,
            Q2Constants.column_end_date, Q2Constants.specified_year,
            Q2Constants.specified_month
        )
        photos_unpacked_df = self.column_unpacker(filtered_event_df, Q2Constants.photos_column_to_unpack)
        df_to_export = (photos_unpacked_df[Q2Constants.column_selection]
                                          .rename(Q2Constants.columns_to_rename)
        )
        super().export_df_to_csv(df_to_export, Q2Constants.output_file_path)  

q1 = QuestionOne()
q1.run()
q2 = QuestionTwo(q1.restaurant_df)
q2.run()
