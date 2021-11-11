#!/usr/bin/env python
# coding: utf-8

###### Amundsen Data Prep and Validation Script ######

"""
    Reads Contributor metadata file (.xlsx), creates seperate dataframes, checks for 'tags', 'badges', missing
    and/or null values. Creates tags and badges as needed and writes 3 .csv files as output to the sample_data directory
    used by Amundsen.  Steps to run:
    1. Save/Pull data_prep.py file to the following directory of ec2-user:
       
       /home/ec2-user/amundsendatabuilder/example/scripts
    2. cd into /amundsendatabuilder   
    2. Create virtual environment: python3 -m venv venv
    3. Activate virtual environment: source venv/bin/activate
    4. Install Amundsen requirements: pip3 install -r requirements.txt
    5. Install data_prep.py requirements: pip3 install -3 data_prep_requirements.txt
    6. Run setup.py
    4. Run data_prep script: python3 data_prep.py

Troubleshooting:

    - sample_data_loader.py runs, but log message in console indicates that elastic search received no data
      Possible causes/fixes:
          1.  Elastic Search and Neo4j proxy hosts have not been added to ec2 environment variables
              run:
"""

# Databuilder imports
import logging
import os
import sys
import subprocess
import xlrd
import shutil
import datetime
from typing import Any, Tuple
import pandas as pd
### CMS Imports ###
import data_loader
from files_utils import File_Utils
from data_frame_utils import DataFrameTable, DataFrameColumn, DataFrameDataAsset, DataFrameSchemaDescription
from config import Config



# logging
LOGGER = logging.getLogger(__name__)
today=datetime.datetime.today()
date=str(str(today.month) + str("_") + str(today.day) + str("_") + str(today.year))
print ("today's date:" + date + "\n")


# local testing directories
amundsen_directory = Config.get_folder_name() 
source_file_dir= os.path.join(amundsen_directory, "source_files")
# ## Data directories
load_file_backup_dir= os.path.join(amundsen_directory, "load_file_backup")
sample_data_dir= os.path.join(amundsen_directory,"sample_data")
archive_file_dir= os.path.join(amundsen_directory, "archived_files")
# ## Dependent scripts
get_contributor_files_script= os.path.join(amundsen_directory, "scripts", "get-contributer-files.sh")


def download_files() -> None:
    """ execututes shell script to download files from s3 to ec2"""
    sys.stdout.write("downloading files from s3...\n")
    subprocess.call(get_contributor_files_script, shell=True)


def create_tables(xls_path: str, contributor_name: str) -> pd.DataFrame:
    """ Extract the Tables information, transform the data to a new format and
        load the new Data Frame in a new CSV
    """
    data_frame_table = DataFrameTable(
        sample_data_dir=sample_data_dir, 
        load_file_backup_dir=load_file_backup_dir, 
        worksheet_name='Tables', 
        contributor_name=contributor_name
    )
    data_frame_table.create_dataframe(excel_path=xls_path)
    df_tables = data_frame_table.build_data_frame()
    data_frame_table.create_csv('sample_table.csv')
    return df_tables

def create_columns(xls_path: str, contributor_name: str) -> None:
    """ Extract the Columns information, transform the data to a new format and
        load the new Data Frame in a new CSV
    """
    data_frame_column = DataFrameColumn(
        sample_data_dir=sample_data_dir, 
        load_file_backup_dir=load_file_backup_dir, 
        worksheet_name='Columns', 
        contributor_name=contributor_name
    )
    data_frame_column.create_dataframe(excel_path=xls_path)
    data_frame_column.build_data_frame()
    data_frame_column.create_csv('sample_col.csv')

def create_data_asset_profile(xls_path: str, contributor_name: str, df_tables: pd.DataFrame) -> None:
    """ Extract the Data Asset Profile information, transform the data to a new format and
        load the new Data Frame in a new CSV
    """
    data_frame_data_asset = DataFrameDataAsset(
        sample_data_dir=sample_data_dir, 
        load_file_backup_dir=load_file_backup_dir, 
        worksheet_name='Data Asset Profile', 
        contributor_name=contributor_name
    )
    data_frame_data_asset.create_dataframe(excel_path=xls_path)
    data_frame_data_asset.build_data_frame(df_tables= df_tables)
    data_frame_data_asset.create_csv('sample_table_programmatic_source.csv')

    # Generate the schema's description (data asset profile)
    # create an empty data frame
    # and the schema key, schema and description columns
    data_frame_description = DataFrameSchemaDescription(
        sample_data_dir=sample_data_dir, 
        load_file_backup_dir=load_file_backup_dir, 
        worksheet_name='', 
        contributor_name=contributor_name
    )
    data_asset_description = data_frame_data_asset.get_data_asset_description()
    data_frame_description.build_data_frame(data_asset_description= data_asset_description)
    data_frame_description.create_csv('sample_schema_description.csv')

def get_data(file: bytes) -> Tuple[str, str, str]:
    """ Return the excel file path, file name and contributor name"""
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



def main() -> None:
    """ Iterate through each contributor file, create sample_tables, sample_col, and sample_table_programmatic_source 
        (data asset profile).csv files, delete the existing es index, and run sample_data_loader.py script, before 
        returning to the top of the loop and processing the next file """
    
    # call Nipun's shell script to download source file from s3
    # download_files(get_contributor_files_script)
    sys.stdout.write("begin processing source files\n")
    logging.basicConfig(level=logging.INFO)

    # read all contributor files from ec2 source file directory
    source_files=File_Utils.fetch_excel(source_file_dir)
    sys.stdout.write("number of source file to process:" + str(len(source_files))+ '\n')
    
    # to keep track of processing progress and control when to exit
    for file in source_files:
        # Get the path, file name and contributor
        xls_path, contributor_name, file_name  = get_data(file)
        # create tables, columns, and data asset profile dataframes
        df_tables = create_tables(xls_path, contributor_name)
        create_columns(xls_path, contributor_name)
        create_data_asset_profile(xls_path, contributor_name, df_tables)

        # move .xlsx file from source_files to archive_files dir when processing is complete
        old_path= os.path.join(source_file_dir,file_name)
        new_path= os.path.join(archive_file_dir,file_name)
        shutil.move(old_path,new_path)
        # shutil.copy(old_path,new_path)
    
        # Start the load process from the CSV file to Neo4j
        schema = f"hive_{contributor_name.lower()}"
        data_loader.run_data_loader(schema=schema)
            
           
if __name__ == '__main__':
    main()

