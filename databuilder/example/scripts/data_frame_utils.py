import sys
import pandas as pd
import datetime
from files_utils import File_Utils
from typing import Optional

"""
    This class contains all the methos that are necessary
    to read the data from the Excel file and create the
    CSV file that are consume for the data loader process
"""

class DataFrameCSV():

    sample_data_dir: str
    load_file_backup_dir: str
    contributor_name: str
    worksheet_name: str
    data_asset_title: str

    def __init__(self, sample_data_dir: str, load_file_backup_dir: str, worksheet_name: str, contributor_name: str, data_asset_title: Optional[str] = None):
        self.worksheet_name = worksheet_name
        self.sample_data_dir = sample_data_dir
        self.load_file_backup_dir = load_file_backup_dir
        self.contributor_name = contributor_name
        self.data_asset_title= data_asset_title


    def create_dataframe(self, excel_path: str) -> pd.DataFrame:
        """ requires pandas excel path and worksheet name and returns a 
            dataframe of the worksheet"""
        self.data_frame=pd.read_excel(excel_path, self.worksheet_name)
        return self.data_frame


    def create_csv(self, csv_file_name: str) -> pd.DataFrame:
        """ With the new data frame create the CSV file in the folder where will
            be consume for the data loader process
        """
        # write file to sample_data dir
        sample_data_path = f"{self.sample_data_dir}/{csv_file_name}"
        self.data_frame.to_csv(sample_data_path,encoding='utf-8',index=False)
        # write file to back_up_load_file dir
        today = datetime.datetime.today()
        date = f"{str(today.month)}_{str(today.day)}_{str(today.year)}"
        load_file_path = f"{self.load_file_backup_dir}/{self.contributor_name}_{date}{csv_file_name}"
        self.data_frame.to_csv(load_file_path,encoding='utf-8',index=False)
        return self.data_frame

    def set_database_attributes(self):
        # create database, cluster, schema columns
        self.data_frame['database']= "hive"
        self.data_frame['cluster']= "gold"
        self.data_frame['schema']= str(self.contributor_name).lower()

    def build_dataframe(self):
        pass

"""
    This class inherits the attributes and methos from DataFraCSV
    And implement the method that extract and validate the data from the Excel file
    and create a new Data Frame with the information
"""
class DataFrameTable(DataFrameCSV):

    def build_data_frame(self) -> pd.DataFrame:
        # check for null is_view values
        self.data_frame['is_view'].fillna('table',inplace=True)
        self.data_frame['name']= [x.lower() for x in self.data_frame['name']]
        # check for missing tags
        self.data_frame= File_Utils.check_tags(self.data_frame)
        self.set_database_attributes()
        return self.data_frame


class DataFrameColumn(DataFrameCSV):

    def build_data_frame(self) -> None:
        # check badges
        self.data_frame['badges']=File_Utils.find_all_badges(self.data_frame)
        # check for null is_view values
        self.data_frame['is_view'].fillna('table',inplace=True)
        self.data_frame['table_name']=[x.lower() for x in self.data_frame['table_name']]
        self.data_frame['name']=[x.lower() for x in self.data_frame['name']]
        # upper case column type
        self.data_frame['col_type'] = [column.upper() for column in self.data_frame['col_type']]
        self.set_database_attributes()
        # assign position int for sort_order
        self.data_frame['sort_order']=[i for i in range(0,self.data_frame.shape[0])]


class DataFrameDataAsset(DataFrameCSV):

    data_asset_description: str

    def build_data_frame(self, df_tables: pd.DataFrame) -> None:
        # rename column to match load file requirements
        s = self.data_frame.columns.to_series()
        s.iloc[0] = 'description_source'
        self.data_frame.columns = s
        # get the data asset profile from the descrition
        self.data_asset_description = self.data_frame.iloc[0]['description_source']
        # add all other necessary columns required in sample_table_programmatic_source.csv from df_tables
        df_temp=pd.DataFrame(df_tables)
        description_source2=[]
        for row in df_temp.iterrows():
            description_source2.append(self.data_frame.values.copy())
        df_temp['description_source']= File_Utils.remove_brackets(description_source2)
        df_temp['description_source']=[e[1:-1] for e in df_temp['description_source']]
        df_temp['description']=""
        self.data_frame = df_temp
        self.set_database_attributes()
    
    def get_data_asset_description(self) -> pd.DataFrame:
        return  self.data_asset_description



class DataFrameSchemaDescription(DataFrameCSV):

    def build_data_frame(self, data_asset_description: str):
        # Generate the schema's description (data asset profile)
        # create an empty data frame
        # and the schema key, schema and description columns
        self.data_frame = pd.DataFrame()
        self.data_frame['schema_key']= [f"hive://gold.{str(self.contributor_name).lower()}"]
        self.data_frame['schema']= [str(self.contributor_name).lower()]
        self.data_frame['description']= [f"{self.data_asset_title}|{data_asset_description}"]