import urllib.parse
import pandas as pd
import logging
import logging
import sys
import xlrd
from typing import Any, Tuple, Optional
import pandas as pd
from .files_utils import File_Utils
from .data_frame_utils import DataFrameTable, DataFrameColumn, DataFrameDataAsset, DataFrameSchemaDescription

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


class Data_Builder:

    tmp_data_dir: str

    def __init__(self, tmp_data_dir:str):
        self.tmp_data_dir = tmp_data_dir


    def _create_tables(self, xls_path: str, contributor_name: str, bucket_name: str, xls_full_path: str) -> pd.DataFrame:
        """ Extract the Tables information, transform the data to a new format and
            load the new Data Frame in a new CSV
        """
        logging.info(f"***create_tables***")
        data_frame_table = DataFrameTable(
            folder_data_dir= self.tmp_data_dir, 
            worksheet_name= 'Tables', 
            contributor_name= contributor_name,
            bucket_name= bucket_name
        )
        data_frame_table.create_dataframe(excel_path=xls_path)
        df_tables = data_frame_table.build_data_frame()
        data_frame_table.create_csv('data_table.csv', xls_full_path)
        return df_tables

    def _create_columns(self, xls_path: str, contributor_name: str, bucket_name: str, xls_full_path: str) -> None:
        """ Extract the Columns information, transform the data to a new format and
            load the new Data Frame in a new CSV
        """
        logging.info(f"***create_columns***")
        data_frame_column = DataFrameColumn(
            folder_data_dir= self.tmp_data_dir, 
            worksheet_name='Columns', 
            contributor_name= contributor_name,
            bucket_name= bucket_name
        )
        data_frame_column.create_dataframe(excel_path=xls_path)
        data_frame_column.build_data_frame()
        data_frame_column.create_csv('data_column.csv', xls_full_path)

    def _create_data_asset_profile(self, xls_path: str, contributor_name: str, df_tables: pd.DataFrame, bucket_name: str,  data_asset_title: str, xls_full_path: str) -> None:
        """ Extract the Data Asset Profile information, transform the data to a new format and
            load the new Data Frame in a new CSV
        """
        logging.info(f"***create_data_asset_profile***")
        data_frame_data_asset = DataFrameDataAsset(
            folder_data_dir= self.tmp_data_dir, 
            worksheet_name= 'Data Asset Profile', 
            contributor_name= contributor_name,
            bucket_name= bucket_name,
            data_asset_title= data_asset_title
        )
        data_frame_data_asset.create_dataframe(excel_path=xls_path)
        data_frame_data_asset.build_data_frame(df_tables= df_tables)
        data_frame_data_asset.create_csv('data_table_programmatic_source.csv', xls_full_path)

        # Generate the schema's description (data asset profile)
        # create an empty data frame
        # and the schema key, schema and description columns
        data_frame_description = DataFrameSchemaDescription(
            folder_data_dir=self.tmp_data_dir, 
            worksheet_name='', 
            contributor_name=contributor_name,
            bucket_name= bucket_name,
            data_asset_title= data_asset_title
        )
        data_asset_description = data_frame_data_asset.get_data_asset_description()
        data_frame_description.build_data_frame(data_asset_description= data_asset_description)
        data_frame_description.create_csv('data_schema_description.csv', xls_full_path)


    def _get_data(self, file: bytes) -> Tuple[str, str, str]:
        """ Return the excel file path, file name and contributor name"""
        logging.info(f"***get_data***")
        list_sheet_name = ['Tables', 'Columns', 'Data Asset Profile']    
        futils = File_Utils(file)
        contributor_name= futils.fetch_contributor_name()
        file_name = futils.fetch_file_name()
        xls_path= futils.read_xlsx(self.tmp_data_dir)
        sys.stdout.write("Now processing:" + str(contributor_name))
        # read sheet names into list
        xls = xlrd.open_workbook(xls_path, on_demand=True)
        sheet_names=xls.sheet_names()
        # validate if the xlsx file has the sheet required
        check =  all(item in list_sheet_name for item in sheet_names)
        if not check:
            raise Exception("Not all the sheet names are in the file")
        # Getting the Data Asset Profile title from the cell A1  
        sheet = xls.sheet_by_name('Data Asset Profile')
        data_asset_title= sheet.cell_value(rowx=0, colx=0)
        return xls_path, contributor_name, file_name, data_asset_title


    def data_builder(self, bucket_name: str, file_path: str, xls_full_path: str) -> str:

        # Get the path, file name and contributor
        xls_path, contributor_name, file_name, data_asset_title  = self._get_data(file_path)
        logging.info(f"File name: {file_name}")
        # create tables, columns, and data asset profile dataframes
        df_tables = self._create_tables(xls_path, contributor_name, bucket_name, xls_full_path)
        self._create_columns(xls_path, contributor_name, bucket_name, xls_full_path)
        self._create_data_asset_profile(xls_path, contributor_name, df_tables, bucket_name, data_asset_title, xls_full_path)
        return contributor_name
