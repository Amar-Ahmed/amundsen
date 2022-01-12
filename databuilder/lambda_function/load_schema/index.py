import boto3 # comment this package when is running local or install the package
import json
import os
import logging
import sys
from libraries.data_loader import Data_Loader

tmp_dir = "/tmp/" 

# This code has to be active when is deploy to the AWS in the lambda funtion
def lambda_handler(event, context):
    try:
        schema_name = event['schema_name']  
        region = os.environ.get('AWS_REGION')
        project_folder = os.environ.get('FOLDER_NAME')
        es_host = os.environ.get('CREDENTIALS_ELASTICSEARCH_PROXY_HOST')
        es_port = os.environ.get('CREDENTIALS_ELASTICSEARCH_PROXY_PORT')
        print(schema_name)
        print(region)
        print(f"folder with data: {project_folder}")
        
        # download transfor data
        bucket_name = f"cms-{schema_name}"
        s3 = boto3.resource('s3')
        csv_bucket = s3.Bucket(bucket_name)
        csv_dir = "transform_data"
        list_files_s3 = list(csv_bucket.objects.filter(Prefix=csv_dir))
        # files list that are required for the load process
        list_files = [
            'data_table.csv',
            'data_col.csv',
            'data_table_programmatic_source.csv',
            'data_schema_description.csv',
            'data_dashboard_table.csv'
            ]
        # check if the files exists in the bucket
        # download the file in the tmp directory
        for file_name in list_files:
            csv_file_path = f"{csv_dir}/{file_name}"
            if any(file.key == csv_file_path for file in list_files_s3):
                csv_tmp_path = f"{tmp_dir}{file_name}"
                csv_bucket.download_file(csv_file_path, csv_tmp_path)
            else:
                raise Exception(f"{csv_file_path} does not exists")
        # run the data loader process
        data_loader = Data_Loader(csv_folder='')
        data_loader.run_data_loader(schema_name)
        return { 
            'statusCode': 200,
            'message' : schema_name
        }
    except Exception as error:
        return {
            'statusCode': 404,
            'message': str(error)
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