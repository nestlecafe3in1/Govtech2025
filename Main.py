import pandas as pd
import json
import requests
import numpy as np
from constants import Q1Constants, Q2Constants, Q3Constants
from utils import extract_json, load_and_normalize_json, export_df_to_csv, read_excel


class QuestionOne:
    def __init__(self):
        self.restaurant_url = Q1Constants.RESTAURANT_URL
        self.country_code_path = Q1Constants.COUNTRY_CODEFILE
        self.restaurant_df = None

    def run(self):
        base_restaurant_df = load_and_normalize_json(self.restaurant_url, Q1Constants.NORMALIZE_RECORD_PATH)
        country_code_df = read_excel(self.country_code_path)
        self.restaurant_df = pd.merge(  
            base_restaurant_df, country_code_df, 
            left_on= Q1Constants.LEFT_JOIN_KEY, right_on=Q1Constants.RIGHT_JOIN_KEY,
            how = "left"
            )
        # Convertion of column datatype to float
        self.restaurant_df[Q1Constants.COLUMN_CONVERT] = self.restaurant_df[Q1Constants.COLUMN_CONVERT].astype('float64')
        # Rename columns to be more presentable
        self.restaurant_df = self.restaurant_df.rename(columns=Q1Constants.COLUMNS_TO_RENAME)

        df_to_export = self.restaurant_df[Q1Constants.COLUMN_SELECTION]
        export_df_to_csv(df_to_export, Q1Constants.OUTPUT_FILE_PATH)


class QuestionTwo:    
    def __init__(self, restaurant_df):
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
        events_unpacked_df = self.column_unpacker(self.restaurant_df, Q2Constants.EVENT_COLUMN_TO_UNPACK)
        filtered_event_df = self.month_filter(
            events_unpacked_df, Q2Constants.COLUMN_START_DATE,
            Q2Constants.COLUMN_END_DATE, Q2Constants.SPECIFIED_YEAR,
            Q2Constants.SPECIFIED_MONTH
        )
        photos_unpacked_df = self.column_unpacker(filtered_event_df, Q2Constants.PHOTOS_COLUMN_TO_UNPACK)
        df_to_export = (photos_unpacked_df[Q2Constants.COLUMN_SELECTION]
                                          .rename(Q2Constants.COLUMNS_TO_RENAME)
        )
        export_df_to_csv(df_to_export, Q2Constants.OUTPUT_FILE_PATH)  

class QuestionThree:
    def __init__(self, restaurant_df:pd.DataFrame):
        self.restaurant_df = restaurant_df

    def dataframe_filter(self, df:pd.DataFrame, column:str,ratings:list):
        filtered_df = df[
            df[column].isin(ratings)
            ]
        return filtered_df
    
    def aggregator(self, 
                   df:pd.DataFrame, column:str, 
                   ratings:list, aggregates:list
                   ):
         rating_threshold_df = (df.groupby(column, as_index=False)
                                  .agg(aggregates)
            )
         return rating_threshold_df

    def run(self):
        rated_restaurants_df = self.dataframe_filter(
            self.restaurant_df, Q3Constants.COLUMN_TO_AGGREGATE, Q3Constants.SPECIFIED_RATINGS
            )
        rating_threshold_df = self.aggregator(
            rated_restaurants_df, Q3Constants.COLUMN_TO_AGGREGATE, 
            Q3Constants.SPECIFIED_RATINGS, Q3Constants.AGGREGATES)
        print(rating_threshold_df.sort_values(Q3Constants.SORT_VARIABLE))

    
q1 = QuestionOne()
q1.run()
q2 = QuestionTwo(q1.restaurant_df)
q2.run()
q3 = QuestionThree()
q3.run()
