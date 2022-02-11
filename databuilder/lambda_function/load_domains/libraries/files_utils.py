import os
import logging
import pandas as pd
import re
from typing import List, Union, Any


class File_Utils:

    file_name: str

    def __init__(self, file_path: str):
        self.file_name = os.path.basename(file_path)
    
    def fetch_file_name(self) -> str:
        """ returns filename from file being processed """
        return str(self.file_name)

    def read_xlsx (self, source_path: str) -> str:
        """ creates python Obj from tables, columns and data_asset_profile worksheets
            in source file"""
        xlsx_path=os.path.join(source_path,self.file_name)
        return xlsx_path

    @staticmethod
    def fetch_excel (directory: str) -> list:
        """ returns list of excel files from a given directory"""
        file_list=[]
        for path, subdirs, files in os.walk(directory):
            for file in files:
                if (file.endswith('.xlsx') or file.endswith('.xls') or file.endswith('.XLS')):
                    file_list.append(os.path.join(path, file))
        return file_list

    @staticmethod
    def create_df(excel_path: str, worksheet_name: str) -> pd.DataFrame:
        """ requires pandas excel object and worksheet name and returns a 
            dataframe of the worksheet"""
        df=pd.read_excel(excel_path,worksheet_name)
        return df
    
    @staticmethod
    def isNaN(num: Any) -> bool:
        """ Validate if a values id NAN and return True"""
        return num != num

    @staticmethod
    def get_str_value(value: Union[float, str], message: str = '')-> str:
        """ Return the value from the cell or empty if the values is NAN"""
        if not(File_Utils.isNaN(value)) and str(value).strip():
            return str(value)
        return message


    @staticmethod
    def get_data_asset_list(data_assets: str)-> List:
        """ Generate a Data Asset list for each domain"""
        data_asset_list = []
        if not(type(data_assets) == float and File_Utils.isNaN(data_assets)) and str(data_assets).strip():
            data_asset_list_raw = data_assets.split(',')
            for data_asset in data_asset_list_raw:
                data_asset_list.append(data_asset.strip().lower())
        return data_asset_list