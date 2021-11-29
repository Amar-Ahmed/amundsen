import boto3
import urllib.parse
import pandas as pd
import logging
import logging
import sys
import os
import shutil
import xlrd
from typing import Any, Tuple
import pandas as pd
from libraries.files_utils import File_Utils
from libraries.data_frame_utils import DataFrameTable, DataFrameColumn, DataFrameDataAsset, DataFrameSchemaDescription


logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

s3 = boto3.client('s3')

# project_directory = os.path.dirname( os.path.abspath(__file__))
source_file_dir = "/tmp" # os.path.join(project_directory, "tmp")
sample_data_dir = "/tmp" # os.path.join(project_directory, "tmp")



def create_tables(xls_path: str, contributor_name: str, bucket_name: str) -> pd.DataFrame:
    """ Extract the Tables information, transform the data to a new format and
        load the new Data Frame in a new CSV
    """
    logging.info(f"***create_tables***")
    data_frame_table = DataFrameTable(
        sample_data_dir= sample_data_dir, 
        worksheet_name= 'Tables', 
        contributor_name= contributor_name,
        bucket_name= bucket_name
    )
    data_frame_table.create_dataframe(excel_path=xls_path)
    df_tables = data_frame_table.build_data_frame()
    data_frame_table.create_csv('sample_table.csv')
    return df_tables

def create_columns(xls_path: str, contributor_name: str, bucket_name: str) -> None:
    """ Extract the Columns information, transform the data to a new format and
        load the new Data Frame in a new CSV
    """
    logging.info(f"***create_columns***")
    data_frame_column = DataFrameColumn(
        sample_data_dir= sample_data_dir, 
        worksheet_name='Columns', 
        contributor_name= contributor_name,
        bucket_name= bucket_name
    )
    data_frame_column.create_dataframe(excel_path=xls_path)
    data_frame_column.build_data_frame()
    data_frame_column.create_csv('sample_col.csv')

def create_data_asset_profile(xls_path: str, contributor_name: str, df_tables: pd.DataFrame, bucket_name: str) -> None:
    """ Extract the Data Asset Profile information, transform the data to a new format and
        load the new Data Frame in a new CSV
    """
    logging.info(f"***create_data_asset_profile***")
    data_frame_data_asset = DataFrameDataAsset(
        sample_data_dir= sample_data_dir, 
        worksheet_name= 'Data Asset Profile', 
        contributor_name= contributor_name,
        bucket_name= bucket_name
    )
    data_frame_data_asset.create_dataframe(excel_path=xls_path)
    data_frame_data_asset.build_data_frame(df_tables= df_tables)
    data_frame_data_asset.create_csv('sample_table_programmatic_source.csv')

    # Generate the schema's description (data asset profile)
    # create an empty data frame
    # and the schema key, schema and description columns
    data_frame_description = DataFrameSchemaDescription(
        sample_data_dir=sample_data_dir, 
        worksheet_name='', 
        contributor_name=contributor_name,
        bucket_name= bucket_name
    )
    data_asset_description = data_frame_data_asset.get_data_asset_description()
    data_frame_description.build_data_frame(data_asset_description= data_asset_description)
    data_frame_description.create_csv('sample_schema_description.csv')

def get_data(file: bytes) -> Tuple[str, str, str]:
    """ Return the excel file path, file name and contributor name"""
    logging.info(f"***get_data***")
    list_sheet_name = ['Tables', 'Columns', 'Data Asset Profile']    
    futils = File_Utils(file)
    contributor_name= futils.fetch_contributor_name()
    file_name = futils.fetch_file_name()
    xls_path= futils.read_xlsx(source_file_dir)
    sys.stdout.write("Now processing:" + str(contributor_name))
    # read sheet names into list
    xls = xlrd.open_workbook(xls_path, on_demand=True)
    sheet_names=xls.sheet_names()
    # validate if the xlsx file has the sheet required
    check =  all(item in list_sheet_name for item in sheet_names)
    if not check:
        raise Exception("Not all the sheet names are in the file")
    return xls_path, contributor_name, file_name


def data_builder(bucket_name: str, file_path: str) -> None:

    # Get the path, file name and contributor
    xls_path, contributor_name, file_name  = get_data(file_path)
    logging.info(f"File name: {file_name}")
    # create tables, columns, and data asset profile dataframes
    df_tables = create_tables(xls_path, contributor_name, bucket_name)
    create_columns(xls_path, contributor_name, bucket_name)
    create_data_asset_profile(xls_path, contributor_name, df_tables, bucket_name)


def lambda_handler(event, context):
    print("**Start Lambda Function**")
    object_get_context = event["Records"][0]
    s3_data = object_get_context["s3"]
    object = s3_data["object"]
    # Get the object from the event and show its content type
    bucket_name = s3_data['bucket']['name']
    file_name = urllib.parse.unquote_plus(s3_data['object']['key'], encoding='utf-8')
    print(f"Bucket: {bucket_name}")
    print(f"File name: {file_name}")
    print(f"Extension: {file_name.split('.')[-1]}")
    if str(file_name.split('.')[-1]).lower() == 'xlsx': 
        try:
            s3 = boto3.resource('s3')
            excel_file_path = os.path.join(source_file_dir,file_name)
            s3.Bucket(bucket_name).download_file(file_name, excel_file_path)
            data_builder(bucket_name, excel_file_path)
            print('*****Process Done*****')
            return {'bucket_name': bucket_name} 
        except Exception as e:
            print(e)
            print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(file_name, bucket))
            raise e



# Uncoment this code when run the lambda function locally
# if __name__ == '__main__':
#     excel_file_name = '' # files name
#     excel_file_path = os.path.join(source_file_dir, excel_file_name)
#     shutil.copy(excel_file_name, excel_file_path)
#     data_builder(excel_file_path)