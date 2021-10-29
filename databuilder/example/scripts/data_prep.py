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

# Download/Install NLP Dependencies
import nltk
import textblob
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('brown')

# Databuilder imports
import logging
import os
import sys
import data_loader

### Imports ###
import subprocess
import sys
import os
import pandas as pd
import numpy as np
import textblob
import xlrd
import shutil
import subprocess
from elasticsearch import Elasticsearch
import datetime
import re
### global variables  ###

# logging
LOGGER = logging.getLogger(__name__)
today=datetime.datetime.today()
date=str(str(today.month) + str("_") + str(today.day) + str("_") + str(today.year))
print ("today's date:" + date + "\n")

# elastic search
es_host = os.getenv('CREDENTIALS_ELASTICSEARCH_PROXY_HOST', 'localhost')
es_port = os.getenv('CREDENTIALS_ELASTICSEARCH_PROXY_PORT', 9200)
es = Elasticsearch([
    {'host': es_host, 'port': es_port},
])




# # local testing directories
# folder_name = os.path.dirname(os.path.dirname( os.path.abspath(__file__)))
# source_file_dir=rf"{folder_name}\source_files"
# load_file_backup_dir=rf"{folder_name}\load_file_backup"
# get_contributor_files_script=rf"{folder_name}\scripts\get-contributer-files.sh"
# sample_data_dir=rf"{folder_name}\sample_data"
# archive_file_dir=rf"{folder_name}\archived_files"
# sample_data_loader_script=rf"{folder_name}\scripts\sample_data_loader.py"
# get_contributor_files_script=rf"{folder_name}\scripts\get-contributer-files.sh"


## location on ec2 instance of Contributor .xlsx file downloaded from s3.
source_file_dir=r"/home/ec2-user/amundsendatabuilder/example/source_files"
## Data directories
archive_file_dir=r"/home/ec2-user/amundsendatabuilder/example/archived_files"
sample_data_dir=r"/home/ec2-user/amundsendatabuilder/example/sample_data"
load_file_backup_dir=r"/home/ec2-user/amundsendatabuilder/example/load_file_backup"
## Dependent scripts
get_contributor_files_script=r"/home/ec2-user/amundsendatabuilder/example/scripts/get-contributer-files.sh"


def download_files(shell_script):
    """ execututes shell script to download files from s3 to ec2"""
    
    sys.stdout.write("downloading files from s3...\n")
    subprocess.call(get_contributor_files_script, shell=True)
    return
    
def fetch_contributor_name(xlsx_file):
    """ parses contributor name from filename"""
 
    file_name=str((os.path.basename(xlsx_file)))
    contributor_name=str(file_name).split("_")[0]
    
    return contributor_name


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
    #xlsx_obj=pd.ExcelFile(xlsx_file)
    return xlsx

def create_df(excelObject, worksheet_name):
    """ requires pandas excel object and worksheet name and returns a 
        dataframe of the worksheet"""
    
    xls=excelObject
    name=worksheet_name
    
    df=pd.read_excel(excelObject,worksheet_name)
    return df

def check_tags(table_dataframe):
    """ Check for presence of tags for each table. Creates tags for tables that are missing
        returns the tables dataframe with updated tags column"""
    
    df=table_dataframe
    for x in df.index:
       
        tags=df['tags'][x]
        row=str(df['description'][x])   
        table_name=str(df['name'][x]).lower()
        table_comment=str(row)
        logging.info(f"Position: {x}, Table= {table_name},  tags = {tags}")
        # checks to see if tags are missing for a table and creates them if they are
        if not tags or pd.isna(tags) or tags.replace(' ','') == '':
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

def check_badges(columns_dataframe):
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


def remove_brackets(list_data):
    """ removes brackets from list of lists """
       
    x=list_data
    new_tags=[]
    for row in x:
        row=str(row).replace('[','').replace(']','')
        new_tags.append(row)
    return new_tags
    
def find_badges (df_column_of_badges):
    badges_list=[]
    badges=df_column_of_badges
    for x in badges:
        if str('Is Nullable: Yes') in str(x):
            badges_list.append('Nullable')
        if str('Is Primary Key: Yes') in str(x):
            badges_list.append('Primary Key')
       
        else:
            badges_list.append("")
            continue
    return badges_list        

def find_all_badges(columns_dataframe):
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

     
      
def main():
    
    """ Iterate through each contributor file, create sample_tables, sample_col, and sample_table_programmatic_source 
        (data asset profile).csv files, delete the existing es index, and run sample_data_loader.py script, before 
        returning to the top of the loop and processing the next file """
    
    # call Nipun's shell script to download source file from s3
    download_files(get_contributor_files_script)
    
    
    sys.stdout.write("begin processing source files\n")
    
    logging.basicConfig(level=logging.INFO)

    # read all contributor files from ec2 source file directory
    source_files=fetch_excel(source_file_dir)

    sys.stdout.write("number of source file to process:" + str(len(source_files))+ '\n')
    
    # to keep track of processing progress and control when to exit
    # length=len(source_files)
    
    for x in source_files:
        contributor_name=fetch_contributor_name(x)
        xls_obj=read_xlsx(x)

        sys.stdout.write("Now processing:" + str(contributor_name))
        # read sheet names into list
        xls = xlrd.open_workbook(xls_obj, on_demand=True)
        sheet_names=xls.sheet_names()
    
        # create tables, columns, and data asset profile dataframes
        for sheet in sheet_names:
    
            # tables
            if sheet=='Tables':
        
                df_tables= create_df(xls_obj,'Tables')
        
                # check for null is_view values
                df_tables['is_view'].fillna('table',inplace=True)
                df_tables['name']=[x.lower() for x in df_tables['name']]
                # check for missing tags
                # it was commented
                df_tables=check_tags(df_tables)
        
                # create database, cluster, schema columns
                df_tables['database']="hive"
                df_tables['cluster']="gold"
                df_tables['schema']="hive_" + str(contributor_name).lower()
        
                sys.stdout.write(str(df_tables))
        
                # write file to sample_data dir
                df_tables.to_csv(sample_data_dir + "/" + "sample_table.csv",encoding='utf-8',index=False)
            
                # write file to back_up_load_file dir
                df_tables.to_csv(load_file_backup_dir + "/" + contributor_name + "_" + date + "_" + 'sample_table.csv',encoding='utf-8',index=False)
                # columns
            elif sheet=='Columns':
                
                df_columns= create_df(xls_obj,'Columns')
                # check badges
                #df_columns['badges']=pd.Series(find_all_badges(df_columns))
                df_columns['badges']=find_all_badges(df_columns)
                
                # check for null is_view values
                df_columns['is_view'].fillna('table',inplace=True)
                df_columns['table_name']=[x.lower() for x in df_columns['table_name']]
                df_columns['name']=[x.lower() for x in df_columns['name']]
                # check for null badges
                # The option to generate Badges whith the NLP is won't be implemented
                # df_columns=check_badges(df_columns)
        
                # create database, cluster, schema columns
                df_columns['database']="hive"
                df_columns['cluster']="gold"
                df_columns['schema']="hive_" + str(contributor_name).lower()
                    
                # assign position int for sort_order
                df_columns['sort_order']=[i for i in range(0,df_columns.shape[0])]
            
                sys.stdout.write(str(df_columns))
                
                # write to sample_data dir
                df_columns.to_csv(sample_data_dir + "/" + 'sample_col.csv', encoding='utf-8',index=False)
            
                # write file to back_up_load_file dir
                df_columns.to_csv(load_file_backup_dir + "/" + contributor_name + "_" + date + "_" + 'sample_col.csv',encoding='utf-8',index=False)
    
        # data asset profile
            elif sheet=='Data Asset Profile':
    
                df_data_asset_profile=create_df(xls_obj,'Data Asset Profile')

                # rename column to match load file requirements
                s = df_data_asset_profile.columns.to_series()
                s.iloc[0] = 'description_source'
                df_data_asset_profile.columns = s
                # get the data asset profile from the descrition
                data_asset_profile = df_data_asset_profile.iloc[0]['description_source']
                # add all other necessary columns required in sample_table_programmatic_source.csv from df_tables
                df_temp=pd.DataFrame(df_tables)
                description_source2=[]
        
                for row in df_temp.iterrows():
                    description_source2.append(df_data_asset_profile.values.copy())
                df_temp['description_source']=remove_brackets(description_source2)
                df_temp['description_source']=[e[1:-1] for e in df_temp['description_source']]
                df_temp['description']=""
                sys.stdout.write(str(df_temp))
            
                # write to sample_data dir
                df_temp.to_csv(sample_data_dir + "/" + 'sample_table_programmatic_source.csv', encoding='utf-8',index=False)
            
                # write file to back_up_load_file dir
                df_temp.to_csv(load_file_backup_dir + "/" + contributor_name + "_" + date + "_" + 'sample_table_programmatic_source.csv',encoding='utf-8',index=False)

                # Generate the schema's description (data asset profile)
                # create an empty data frame
                # and the schema key, schema and description columns
                df_temp_data_asset_profile = pd.DataFrame()
                df_temp_data_asset_profile['schema_key']=["hive://gold.hive_" + str(contributor_name).lower()]
                df_temp_data_asset_profile['schema']=["hive_" + str(contributor_name).lower()]
                df_temp_data_asset_profile['description']=[data_asset_profile]
                # write to sample_data dir
                df_temp_data_asset_profile.to_csv(sample_data_dir + "/" + 'sample_schema_description.csv', encoding='utf-8',index=False)
                # write file to back_up_load_file dir
                df_temp_data_asset_profile.to_csv(load_file_backup_dir + "/" + contributor_name + "_" + date + "_" + 'sample_schema_description.csv',encoding='utf-8',index=False)

            else:
                # create sample_table_owner load file         
                continue

        # move .xlsx file from source_files to archive_files dir when processing is complete
        file_name=fetch_file_name(x)
        old_path=os.path.join(source_file_dir,file_name)
        new_path=os.path.join(archive_file_dir,file_name)
        shutil.move(old_path,new_path)
        # shutil.copy(old_path,new_path)

        # delete elastic search index
        #es = Elasticsearch('localhost:9200')
        es.indices.delete(index='_all', ignore=[400, 404])
    
        # setting the schema that will be deleted and upload the new data
        schema = f"hive_{contributor_name.lower()}"
        data_loader.run_data_loader(schema=schema)
            
    print("Data Prep Done")
           
if __name__ == '__main__':
    main()

