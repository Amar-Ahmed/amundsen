# coment the boto3 to run locally
import boto3
import urllib.parse
import logging
import os
import shutil
import uuid
from libraries.data_builder import Data_Builder

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# coment the netx two lines  to run locally
s3 = boto3.client('s3')

# Uncoment this to run locally
# project_directory = os.path.dirname( os.path.abspath(__file__))
tmp_file_dir = "/tmp" 


# coment the function lammbda_handler  to run locally
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
            excel_file_path = os.path.join(tmp_file_dir,file_name)
            s3.Bucket(bucket_name).download_file(file_name, excel_file_path)
            obj_data_builder = Data_Builder(tmp_data_dir= tmp_file_dir)
            schema_name = obj_data_builder.data_builder(bucket_name, excel_file_path)
            print('*****Process Done*****')

            return {
                'schema_name': schema_name,
                'response': 200
            } 
        except Exception as e:
            print(e)
            print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(file_name, bucket_name))
            raise e



# # Uncoment this code when run the lambda function locally
# if __name__ == '__main__':
#     excel_file_name = 'mdm_pmi_spp_2021-07-30T1654.xlsx' # files name
#     excel_file_path = os.path.join(project_directory, excel_file_name)
#     tmp_file_path = f"{project_directory}{tmp_file_dir}"
#     excel_tmp_file_path = os.path.join(tmp_file_path,excel_file_name)
#     shutil.copy(excel_file_path, tmp_file_path)
#     obj_data_builder = Data_Builder(tmp_data_dir= tmp_file_path)
#     obj_data_builder.data_builder(bucket_name='', file_path= excel_tmp_file_path )