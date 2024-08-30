import pandas as pd
import requests

def extract_json(self, json_url):
    response = requests.get(json_url)
    if response.ok:
        return response.json()
    else:
        response.raise_for_status()

def load_and_normalize_json(self,json_url:str, column_to_normalize:str):
    json_data = self.extract_json(json_url)
    return pd.json_normalize(json_data, column_to_normalize)

def export_df_to_csv(self, df:pd.DataFrame, file_path:str):
    try:
        df.to_csv(file_path, index=False)
        print(f"Restaurant Data exported successfully to {file_path}")
    except Exception as e:
        print(f"Error exporting data: {e}")

def read_excel(self, path:str):
    try:
        return pd.read_excel(path)
    except FileNotFoundError:
        print(f"File not found: {path}")