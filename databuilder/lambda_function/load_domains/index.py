### Imports ###
import boto3
import urllib.parse
import logging
import sys
import os
import shutil
import datetime
from libraries.data_builder_domain import Data_Builder_Domain

logging.basicConfig(level=logging.INFO)
ssm = boto3.client('ssm')
# # Comment this when the code is deploy in AWS
# project_directory = os.path.dirname( os.path.abspath(__file__))
tmp_file_dir = "/tmp" 

# Get the value from the System Manager Parameter Store
def get_parameter_store():
    parameter = ssm.get_parameter(Name='amundsen-domain-bucket-path', WithDecryption=True)    
    domain_bucket_path = parameter['Parameter']['Value']
    parameter = ssm.get_parameter(Name='amundsen-domain-subfolder-path', WithDecryption=True)    
    domain_subfolder_path = parameter['Parameter']['Value']
    return domain_bucket_path, domain_subfolder_path


def lambda_handler(event, context):
    logging.info("**Start Process Load Domains Information**")
    
    # Get the object from the event and show its content type
    logging.info("Get the object from the event")
    print(event)    

    domain_file = None    
    # check if the call came from the step function
    if event.get('run_domain_process', None) is not None:
        bucket_name, domain_subfolder_path = get_parameter_store()

        s3 = boto3.resource('s3')
        csv_bucket = s3.Bucket(bucket_name)
        last_modified_date = datetime.datetime(1939, 9, 1).replace(tzinfo=None)

        logging.info("Get the last domain file updated")
        # check the bucket to get the domain last updated file
        for file in csv_bucket.objects.filter(Prefix=domain_subfolder_path):            
            file_date = file.last_modified.replace(tzinfo=None)
            if last_modified_date < file_date:
                last_modified_date = file_date
                domain_file = file

        file_name = str(domain_file.key).split('/')[-1]
        logging.info(f"File name: {file_name}")

        # download file in tmp folder
        tmp_file_path = os.path.join(tmp_file_dir,file_name)
        csv_bucket.download_file(domain_file.key, tmp_file_path)
    else:
        # get the bucket and file name from the event
        object_get_context = event["Records"][0]
        s3_data = object_get_context["s3"]

        # Get the object from the event and show its content type
        bucket_name = s3_data['bucket']['name']
        logging.info(f"Bucket: {bucket_name}")
        
        file_name = urllib.parse.unquote_plus(s3_data['object']['key'], encoding='utf-8')
        logging.info(f"File name: {file_name}")

        if str(file_name.split('.')[-1]).lower() == 'xlsx': 
            domain_file = file_name
            s3 = boto3.resource('s3')
            excel_file_path = os.path.join(tmp_file_dir,file_name.split('/')[-1])
            # download the file to a temp directory
            s3.Bucket(bucket_name).download_file(file_name, excel_file_path)

    # check if there is a domain file to process
    if not domain_file:
        raise Exception(f"There is no domain file in the bucket {bucket_name}")

    logging.info("Run the code to load the domains")
    obj_data_builder_domain = Data_Builder_Domain(tmp_data_dir= tmp_file_dir)
    obj_data_builder_domain.load_domains()
    return {
        'response': 200
    } 


# # Uncoment this code when run the lambda function locally
# if __name__ == '__main__':
#     excel_file_name = 'DomainLoadFile_2021-10-20T1515.xlsx' # files name
#     excel_file_path = os.path.join(project_directory, excel_file_name)
#     tmp_file_path = f"{project_directory}{tmp_file_dir}"
#     excel_tmp_file_path = os.path.join(tmp_file_path,excel_file_name)
#     shutil.copy(excel_file_path, tmp_file_path)
#     obj_data_builder_domain = Data_Builder_Domain(tmp_data_dir= tmp_file_path)
#     obj_data_builder_domain.load_domains()