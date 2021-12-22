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
# import boto3
# import urllib.parse
import logging
import sys
import os
import shutil
import datetime
### CMS IMports ###
from libraries.data_builder_domain import Data_Builder_Domain


# logging
logger = logging.getLogger(__name__)
today=datetime.datetime.today()
date=str(str(today.month) + str("_") + str(today.day) + str("_") + str(today.year))
print ("today's date:" + date + "\n")


# Comment this when the code is deploy in AWS
project_directory = os.path.dirname( os.path.abspath(__file__))
tmp_file_dir = "/tmp" 

# Uncomment this code when is deployed in AWS
# def lambda_handler(event, context):
#     print("**Start Lambda Function Load-Domain**")
#     print(event)
#     if event.get('run_domain_process', None) is not None:
#         # download transfor data
#         bucket_name = 'cms-domain'
#         s3 = boto3.resource('s3')
#         csv_bucket = s3.Bucket(bucket_name)
#         last_modified_date = datetime.datetime(1939, 9, 1).replace(tzinfo=None)
#         domain_file = None
#         for file in csv_bucket.objects.all():
#             file_date = file.last_modified.replace(tzinfo=None)
#             if last_modified_date < file_date:
#                 last_modified_date = file_date
#                 domain_file = file
#         print(domain_file.key)
#         # download file in tmp folder
#         tmp_file_path = os.path.join(tmp_file_dir,domain_file.key)
#         csv_bucket.download_file(domain_file.key, tmp_file_path)
#         obj_data_builder_domain = Data_Builder_Domain(tmp_data_dir= tmp_file_dir)
#         obj_data_builder_domain.load_domains()
#     else:
#         object_get_context = event["Records"][0]
#         s3_data = object_get_context["s3"]
#         object = s3_data["object"]
#         # Get the object from the event and show its content type
#         bucket_name = s3_data['bucket']['name']
#         file_name = urllib.parse.unquote_plus(s3_data['object']['key'], encoding='utf-8')
#         print(f"Bucket: {bucket_name}")
#         print(f"File name: {file_name}")
#         print(f"Extension: {file_name.split('.')[-1]}")
#         if str(file_name.split('.')[-1]).lower() == 'xlsx': 
#             s3 = boto3.resource('s3')
#             excel_file_path = os.path.join(tmp_file_dir,file_name)
#             s3.Bucket(bucket_name).download_file(file_name, excel_file_path)
#             obj_data_builder_domain = Data_Builder_Domain(tmp_data_dir= tmp_file_dir)
#             obj_data_builder_domain.load_domains()
#     return {
#         'response': 200
#     } 



# Uncoment this code when run the lambda function locally
if __name__ == '__main__':
    excel_file_name = 'DomainLoadFile_2021-10-20T1515.xlsx' # files name
    excel_file_path = os.path.join(project_directory, excel_file_name)
    tmp_file_path = f"{project_directory}{tmp_file_dir}"
    excel_tmp_file_path = os.path.join(tmp_file_path,excel_file_name)
    shutil.copy(excel_file_path, tmp_file_path)
    obj_data_builder_domain = Data_Builder_Domain(tmp_data_dir= tmp_file_path)
    obj_data_builder_domain.load_domains()
    