#!/usr/bin/env python
# coding: utf-8

###### Amundsen Data Prep for Domain  ######

"""
    Reads Domains metadata file (.xlsx), creates seperate dataframes, checks for the domain's information. 
    After extract the information it creates a domain instance to save the information in neo4j
    Steps to run:
    1. Save/Pull data_prep.py file to the following directory of ec2-user:
       
       /home/ec2-user/amundsendatabuilder/example/scripts
    2. cd into /amundsendatabuilder   
    2. Create virtual environment: python3 -m venv venv
    3. Activate virtual environment: source venv/bin/activate
    4. Install Amundsen requirements: pip3 install -r requirements.txt
    5. Install data_prep.py requirements: pip3 install -3 data_prep_requirements.txt
    6. Run setup.py
    4. Run data_prep script: python3 data_domain_prep.py
"""


### Imports ###
import subprocess
import logging
import sys
import os
from typing import List
import pandas as pd
import numpy as np
import xlrd
import shutil
import subprocess
import datetime
from typing import Union
from domain import Domain


# logging
LOGGER = logging.getLogger(__name__)
today=datetime.datetime.today()
date=str(str(today.month) + str("_") + str(today.day) + str("_") + str(today.year))
print ("today's date:" + date + "\n")


# # local testing directories
# folder_name = os.path.dirname(os.path.dirname( os.path.abspath(__file__)))
# source_file_dir=rf"{folder_name}\source_files"
# load_file_backup_dir=rf"{folder_name}\load_file_backup"
# archive_file_dir=rf"{folder_name}\archived_files"
# get_contributor_files_script=rf"{folder_name}\get-domain-files.sh"


## location on ec2 instance of Contributor .xlsx file downloaded from s3.
source_file_dir=r"/home/ec2-user/amundsendatabuilder/example/source_files"
## Data directories
archive_file_dir=r"/home/ec2-user/amundsendatabuilder/example/archived_files"
sample_data_dir=r"/home/ec2-user/amundsendatabuilder/example/sample_data"
load_file_backup_dir=r"/home/ec2-user/amundsendatabuilder/example/load_file_backup"
## Dependent scripts
get_contributor_files_script=r"/home/ec2-user/amundsendatabuilder/example/scripts/get-domain-files.sh"


def download_files(shell_script):
    """ execututes shell script to download files from s3 to ec2"""
    
    sys.stdout.write("downloading files from s3...\n")
    subprocess.call(get_contributor_files_script, shell=True)
    return
    

def fetch_file_name(xlsx_file):
    """ returns filename from file being processed """
    
    file_name=str((os.path.basename(xlsx_file)))
    return file_name

def fetch_excel (directory):
    """ returns list of excel files from a given directory"""
   
    file_list=[]
    
    for path, subdirs, files in os.walk(directory):
        for file in files:
            if (file.endswith('.xlsx') or file.endswith('.xls') or file.endswith('.XLS')):
                file_list.append(os.path.join(path, file))
                
    return file_list

def read_xlsx (xlsx_file):
    """ creates python Obj from tables, columns and data_asset_profile worksheets
        in source file"""
      
    source_path=source_file_dir
    file_name=(os.path.basename(xlsx_file))
    
    xlsx=os.path.join(source_path,file_name)
    # xlsx_obj=pd.ExcelFile(xlsx_file)
    return xlsx

def create_df(excelObject, worksheet_name):
    """ requires pandas excel object and worksheet name and returns a 
        dataframe of the worksheet"""
    xls=excelObject
    name=worksheet_name
    df=pd.read_excel(excelObject,worksheet_name)
    return df

def get_data_asset_list(data_assets: str)-> List:
    data_asset_list = []
    if not(type(data_assets) == float and np.isnan(data_assets)) and str(data_assets).strip():
        data_asset_list_raw = data_assets.split(',')
        for data_asset in data_asset_list_raw:
            data_asset_list.append(data_asset.strip().lower())
    return data_asset_list


def get_str_value(value: Union[float, str])-> List:
    if not(type(value) == float and np.isnan(value)) and str(value).strip():
        return value
    return ''

def main():
    
    """ Iterate through each file, creates a list of domains, 
        delete the existing domain and create a list of domains"""
    
    # call Nipun's shell script to download source file from s3
    # download_files(get_contributor_files_script)
    
    
    sys.stdout.write("begin processing source files\n")
    
    logging.basicConfig(level=logging.INFO)

    # read all contributor files from ec2 source file directory
    source_files=fetch_excel(source_file_dir)

    sys.stdout.write("number of source file to process:" + str(len(source_files))+ '\n')
    
    # to keep track of processing progress and control when to exit
    # length=len(source_files)
    
    for xlsx_files in source_files:
        xls_obj=read_xlsx(xlsx_files)
        # read sheet names into list
        xls = xlrd.open_workbook(xls_obj, on_demand=True)
        sheet_names=xls.sheet_names()
        domain_list = []
        # create tables, columns, and data asset profile dataframes
        if 'Domains' in sheet_names:
            df_domains= create_df(xls_obj,'Domains')
            for i in df_domains.index:
                domain = {
                    'name': str(df_domains['name'][i]).lower(),
                    'description': df_domains['description'][i],
                    'updates': get_str_value(df_domains['updates'][i]),
                    'contact': get_str_value(df_domains['contact'][i]),
                    'data_asset': get_data_asset_list(df_domains['data_asset_profile'][i])
                }
                domain_list.append(domain)
        
    
            # move .xlsx file from source_files to archive_files dir when processing is complete
            file_name=fetch_file_name(xlsx_files)
            old_path=os.path.join(source_file_dir,file_name)
            new_path=os.path.join(archive_file_dir,file_name)
            shutil.move(old_path,new_path)
            # shutil.copy(old_path,new_path)

    
            domain = Domain(domain_list)
            domain.upload_domains()
            
           
if __name__ == '__main__':
    main()

