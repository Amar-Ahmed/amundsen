# coment the boto3 to run locally
import boto3
import json
import urllib.parse
import logging
import os
import shutil
import uuid
from libraries.data_builder import Data_Builder

logging.basicConfig(level=logging.INFO)

s3 = boto3.client('s3')
ssm = boto3.client('ssm')
# Uncoment this to run locally
# project_directory = os.path.dirname( os.path.abspath(__file__))
tmp_file_dir = "/tmp" 

# Get the value from the System Manager Parameter Store
def get_parameter_store():
    parameter = ssm.get_parameter(Name='amundsen-mdm-bucket-path', WithDecryption=True)    
    mdm_bucket_path = parameter['Parameter']['Value']
    parameter = ssm.get_parameter(Name='amundsen-bic-bucket-path', WithDecryption=True)    
    bic_bucket_path = parameter['Parameter']['Value']
    parameter = ssm.get_parameter(Name='amundsen-transform-data-path', WithDecryption=True)    
    transform_data_path = parameter['Parameter']['Value']
    return mdm_bucket_path, bic_bucket_path, transform_data_path


# coment the function lammbda_handler  to run locally
def lambda_handler(event, context):
    logging.info("**Start Process Extract and Transform Schema**")
    
    # Get the object from the event and show its content type
    logging.info("Get the object from the event")
    print(event)
    event_detail = event["detail"]

    # get the bucket name
    bucket_name = event_detail["bucket"]["name"]
    logging.info(f"bucket name: {bucket_name}")

    # get the file name and the directory path
    file_name = urllib.parse.unquote_plus(event_detail['object']['key'], encoding='utf-8')
    logging.info(f"file name: {file_name}")

    # validate the file, it has to be a Excel and come from the subfolder mdm and data-dictionaries
    mdm_bucket_path, bic_bucket_path, bucket_name_data = get_parameter_store()
    file_full_path = str(os.path.dirname(file_name)).strip('/')    
    if str(file_name.split('.')[-1]).lower() == 'xlsx' and file_full_path in [mdm_bucket_path,bic_bucket_path]: 
        excel_file_path = os.path.join(tmp_file_dir,file_name.split('/')[-1])
        # Download the file in to a temp folder
        s3 = boto3.resource('s3')
        s3.Bucket(bucket_name).download_file(file_name, excel_file_path)
        # Run the code that extract and transfor the data
        obj_data_builder = Data_Builder(tmp_data_dir= tmp_file_dir)
        schema_name = obj_data_builder.data_builder(bucket_name_data, excel_file_path, "")
        logging.info('*****Process Done*****')
        return {
            "schema_name": schema_name,
            "bucket_name": bucket_name_data,
            "file_name": file_name.split('/')[-1]
        }


# # Uncoment this code when run the lambda function locally
# if __name__ == '__main__':
#     excel_file_name = 'mdm_pmi_spp_2021-07-30T1654.xlsx' # files name
#     excel_file_path = os.path.join(project_directory, excel_file_name)
#     tmp_file_path = f"{project_directory}{tmp_file_dir}"
#     excel_tmp_file_path = os.path.join(tmp_file_path,excel_file_name)
#     shutil.copy(excel_file_path, tmp_file_path)
#     obj_data_builder = Data_Builder(tmp_data_dir= tmp_file_path)
#     obj_data_builder.data_builder(bucket_name='', file_path= excel_tmp_file_path )