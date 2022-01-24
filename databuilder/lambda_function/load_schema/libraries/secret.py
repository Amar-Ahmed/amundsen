import logging
import boto3
import json

def get_secret(secret_name, region_name):
    logging.info("Start AWS Session")

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )
    try:
        # pull the secret value
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
        logging.info("Get Secret Value")
        credetencials = get_secret_value_response['SecretString']
        logging.info("End AWS Session")
        return json.loads(credetencials)
    except Exception as error:
        logging.warning("Error getting the secrete manager")
        logging.exception(error)
        return None