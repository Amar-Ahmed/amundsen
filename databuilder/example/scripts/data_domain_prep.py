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
import xlrd
import shutil
import subprocess
import datetime
from typing import  Tuple
### CMS IMports ###
from domain import Domain
from config import Config
from files_utils import File_Utils


# logging
LOGGER = logging.getLogger(__name__)
today=datetime.datetime.today()
date=str(str(today.month) + str("_") + str(today.day) + str("_") + str(today.year))
print ("today's date:" + date + "\n")


# Excel and CSV Files directories
amundsen_directory = Config.get_folder_name() 
source_file_dir= os.path.join(amundsen_directory, "source_files")
# ## Data directories
load_file_backup_dir= os.path.join(amundsen_directory, "load_file_backup")
sample_data_dir= os.path.join(amundsen_directory,"sample_data")
archive_file_dir= os.path.join(amundsen_directory, "archived_files")
get_domain_files_script= os.path.join(amundsen_directory, "scripts", "get-domain-files.sh")


def download_files():
    """ execututes shell script to download files from s3 to ec2"""
    sys.stdout.write("downloading files from s3...\n")
    subprocess.call(get_domain_files_script, shell=True)
 

def get_data(xlsx_files: bytes) -> Tuple[str, str]:
    """ Return the Excel file path, the file name and validate if the file has the tab Domains"""
    utils_file_obj = File_Utils(xlsx_files)
    # get the file name
    file_name= utils_file_obj.fetch_file_name()
    # Get the files full path 
    xls_path= utils_file_obj.read_xlsx(source_file_dir)
    # read sheet names into list
    xls = xlrd.open_workbook(xls_path, on_demand=True)
    sheet_names=xls.sheet_names()
    # Check if the file has a tab named Domains
    if 'Domains' not in sheet_names:
        raise Exception("There are no domains files")
    return xls_path, file_name

def get_domain_list(xls_path: str) -> list:
    """ Create a domains list with their properties"""
    domain_list = []
    df_domains= File_Utils.create_df(excel_path=xls_path, worksheet_name='Domains')
    for i in df_domains.index:
        domain = {
            'name': str(df_domains['name'][i]).lower(),
            'description': df_domains['description'][i],
            'updates': File_Utils.get_str_value(value= df_domains['updates'][i]),
            'contact': File_Utils.get_str_value(value= df_domains['contact'][i]),
            'data_asset': File_Utils.get_data_asset_list(df_domains['data_asset_profile'][i])
        }
        domain_list.append(domain)
    return domain_list

def main() -> None:
    
    """ Iterate through each file, creates a list of domains, 
        delete the existing domain and create a list of domains"""
    
    # call shell script to download source file from s3
    download_files()
    
    sys.stdout.write("begin processing source files\n")
    logging.basicConfig(level=logging.INFO)

    # read all the domains files from ec2 source file directory
    source_files= File_Utils.fetch_excel(source_file_dir)
    sys.stdout.write("number of source file to process:" + str(len(source_files))+ '\n')
    for xlsx_files in source_files:
        xls_path, file_name = get_data(xlsx_files=xlsx_files)
        domain_list = get_domain_list(xls_path)
        # Start the process to create the Domains nodes and relations    
        domain = Domain(domain_list)
        domain.upload_domains()
        # move .xlsx file from source_files to archive_files dir when processing is complete
        old_path=os.path.join(source_file_dir,file_name)
        new_path=os.path.join(archive_file_dir,file_name)
        shutil.move(old_path,new_path)
        # shutil.copy(old_path,new_path)
            
    sys.stdout.write("Domains processing source files it's done\n")

if __name__ == '__main__':
    main()

