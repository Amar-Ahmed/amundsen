import boto3 
import json
import os
import logging
import sys
from libraries.data_loader import Data_Loader
from libraries.email import Email

logging.basicConfig(level=logging.INFO)
tmp_dir = "/tmp/" 

# This code has to be active when is deploy to the AWS in the lambda funtion
def lambda_handler(event, context):
    logging.info("**Start Process that Load the Schema**")
    # Get the object from the event and show its content type
    logging.info("Get the object from the event")
    print(event)
    # Get the bucket name
    bucket_name = event['bucket_name']
    logging.info(f"Bucket name: {bucket_name}")
    # Get the schema name
    schema_name = event['schema_name']  
    logging.info(f"Schema name: {schema_name}")
    # Get the transform data directory path
    data_full_path = event['data_full_path']
    logging.info(f"Transform data folder:: {data_full_path}")
    # Get the excel file name
    excel_file_name = event['file_name']
    # download transfor data
    s3 = boto3.resource('s3')
    csv_bucket = s3.Bucket(bucket_name)
    list_files_s3 = list(csv_bucket.objects.filter(Prefix=data_full_path))
    # files list that are required for the load process
    list_files = [
        'data_table.csv',
        'data_column.csv',
        'data_table_programmatic_source.csv',
        'data_schema_description.csv',
        'data_dashboard_table.csv'
        ]
    # check if the files exists in the bucket
    for file_name in list_files:
        csv_file_path = f"{data_full_path}/{file_name}"
        if any(file.key == csv_file_path for file in list_files_s3):
            # download the file in the tmp directory
            csv_tmp_path = f"{tmp_dir}{file_name}"
            csv_bucket.download_file(csv_file_path, csv_tmp_path)
        else:
            raise Exception(f"{csv_file_path} does not exists")
    # run the data loader process
    data_loader = Data_Loader(csv_folder='')
    data_loader.run_data_loader(schema_name)
    # Sending the email alert
    email = Email(schema_name=schema_name, file_name=excel_file_name)
    email.send_email()
    return { 
        "statusCode": 200,
        "run_domain_process": True,
        "bucket_name": bucket_name
    }


# this code is to run the process locally
# it does not have to be deploy in the lambda function
def main(schema_name: str, csv_folder: str):
    data_loader = Data_Loader(csv_folder)
    data_loader.run_data_loader(schema_name)

if __name__ == '__main__':
    csv_folder = os.path.dirname(os.path.abspath(__file__))
    main(schema_name= 'mdm', csv_folder= csv_folder)
    print("Done")