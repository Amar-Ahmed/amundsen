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
step_function = boto3.client('stepfunctions')
# Uncoment this to run locally
# project_directory = os.path.dirname( os.path.abspath(__file__))
tmp_file_dir = "/tmp" 

# coment the function lammbda_handler  to run locally
def lambda_handler(event, context):
    logging.info("**Start Process Extract and Transform Schema**")
    # Get the object from the event and show its content type
    logging.info("Get the object from the event")
    print(event)
    object_get_context = event["Records"][0]
    s3_data = object_get_context["s3"]
    object = s3_data["object"]
    # get the bucket name
    bucket_name = s3_data['bucket']['name']
    # get the file name and the directory path
    file_name = urllib.parse.unquote_plus(s3_data['object']['key'], encoding='utf-8')
    file_full_path = str(os.path.dirname(file_name)).strip('/')
    # validate the file, it has to be a Excel and come from the subfolder mdm and data-dictionaries
    if str(file_name.split('.')[-1]).lower() == 'xlsx' and file_full_path in ['amundsen/mdm','amundsen/data-dictionaries']: 
        excel_file_path = os.path.join(tmp_file_dir,file_name.split('/')[-1])
        if file_full_path:
            file_full_path = f"{file_full_path}/transform_data"
        else:
            file_full_path='transform_data'
        # Download the file in to a temp folder
        s3 = boto3.resource('s3')
        s3.Bucket(bucket_name).download_file(file_name, excel_file_path)
        # Run the code that extract and transfor the data
        obj_data_builder = Data_Builder(tmp_data_dir= tmp_file_dir)
        schema_name = obj_data_builder.data_builder(bucket_name, excel_file_path, file_full_path)
        # Call the step function
        # The transaction id is the step function's name
        transaction_id = str(uuid.uuid1())
        input = {
            "schema_name": schema_name,
            "bucket_name": bucket_name,
            "data_full_path": file_full_path,
            "file_name": file_name.split('/')[-1]
        }
        # call the step function
        response = step_function.start_execution(
            stateMachineArn= 'arn:aws:states:us-east-1:310946103770:stateMachine:Amundsen-DataBuilder-StepFunction',
            name= transaction_id,
            input= json.dumps(input)
        )
        return {
            'bucket_name': bucket_name,
            'data_full_path': file_full_path,
            'schema_name': schema_name,
            'file_name': file_name.split('/')[-1],
            'response': 200
        } 
        logging.info('*****Process Done*****')

# # Uncoment this code when run the lambda function locally
# if __name__ == '__main__':
#     excel_file_name = 'mdm_pmi_spp_2021-07-30T1654.xlsx' # files name
#     excel_file_path = os.path.join(project_directory, excel_file_name)
#     tmp_file_path = f"{project_directory}{tmp_file_dir}"
#     excel_tmp_file_path = os.path.join(tmp_file_path,excel_file_name)
#     shutil.copy(excel_file_path, tmp_file_path)
#     obj_data_builder = Data_Builder(tmp_data_dir= tmp_file_path)
#     obj_data_builder.data_builder(bucket_name='', file_path= excel_tmp_file_path )