import os
import logging
import pandas as pd
import re
from typing import List, Union, Any
# Download/Install NLP Dependencies
import nltk
import textblob
# nltk.download('punkt')
# nltk.download('stopwords')
# nltk.download('brown')

nltk.data.path.append("/tmp")
nltk.download("punkt", download_dir = "/tmp")
nltk.download('stopwords', download_dir="/tmp")
nltk.download('brown', download_dir="/tmp")


class File_Utils:

    file_name: str

    def __init__(self, file_path: str):
        self.file_name = os.path.basename(file_path)
    
    
    def fetch_contributor_name(self) -> str:
        """ parses contributor name from filename"""
        contributor_name=str(self.file_name).split("_")[0]
        return contributor_name


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
    def check_tags(table_dataframe: pd.DataFrame) -> pd.DataFrame:
        """ Check for presence of tags for each table. Creates tags for tables that are missing
            returns the tables dataframe with updated tags column"""
        
        df=table_dataframe
        for x in df.index:
            tags=df['tags'][x]
            row=str(df['description'][x])   
            table_name=str(df['name'][x]).lower()
            table_comment=str(row)
            # logging.info(f"Position: {x}, Table= {table_name},  tags = {tags}")
            # checks to see if tags are missing for a table and creates them if they are
            if not tags or File_Utils.isNaN(tags) or tags.replace(' ','') == '':
                table_comment = re.sub(r"('|’)(s|S)","", table_comment)  
                blob=textblob.TextBlob(table_comment)
                noun_phrases=blob.noun_phrases
                noun_phrases=list(set(noun_phrases))
                noun_phrases.append('MDM')
                # add tags to the tag column for that row (table)
                df['tags'][x] = ','.join(noun_phrases).title()
            else:
                continue
        return df

    @staticmethod
    def check_badges(columns_dataframe: pd.DataFrame) -> pd.DataFrame:
        """ checks for the presence of badges. Creates badges if they are missing.
            returns the columns dataframe with updated badges column"""
            
        df=columns_dataframe
        for x in df.index:
            badges=df['badges'][x]
            row=df['description'][x]   
            table_comment=str(row)
            #checks to see if badges are missing and creates them if they are
            if not badges:
                blob=textblob.TextBlob(table_comment)
                noun_phrases=blob.noun_phrases
                noun_phrases=list(set(noun_phrases))
                df['badges'][x] = ','.join(noun_phrases).title()
            else:
                continue
        return df

    @staticmethod
    def remove_brackets(list_data: list) -> list:
        """ removes brackets from list of lists """
        x=list_data
        new_tags=[]
        for row in x:
            row=str(row).replace('[','').replace(']','')
            new_tags.append(row)
        return new_tags
        
    @staticmethod
    def find_all_badges(columns_dataframe: pd.DataFrame) -> list:
        """ Generate a list of badges for each row"""
        df=columns_dataframe
        badge_list = []
        # check to find columns that are primary keys
        for i in df.index:
            badge = []
            if str('Yes') in str(df['is_primary_key'][i]):
                badge.append('Primary Key')
            # check if the column is foreign key
            if str('Yes') in str(df['is_foreign_key'][i]):
                badge.append('Foreign Key')
            if str('Yes') in str(df['is_nullable'][i]):
                badge.append('Nullable')
            badge_list.append('-'.join(badge))
        return badge_list    

    @staticmethod
    def get_data_asset_list(data_assets: str)-> List:
        """ Generate a Data Asset list for each domain"""
        data_asset_list = []
        if not(type(data_assets) == float and File_Utils.isNaN(data_assets)) and str(data_assets).strip():
            data_asset_list_raw = data_assets.split(',')
            for data_asset in data_asset_list_raw:
                data_asset_list.append(data_asset.strip().lower())
        return data_asset_list
    

    
