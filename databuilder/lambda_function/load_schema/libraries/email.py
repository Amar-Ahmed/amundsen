import boto3
from .config import Config

         

class Email:
    config = Config()
    aws_region = config.get_aws_region()
    sender = config.get_sender_alert()
    recipient = config.get_recipient_alert().split(',')
    charset = "UTF-8"
    client = boto3.client('ses',region_name=aws_region)
    
    def __init__(self, schema_name, file_name):
        self.schema_name = schema_name
        self.file_name = file_name
        print(f"sender: {self.sender}")
        print(f"recipient {self.recipient}")

    def send_email(self):
        try:
            subject = f"Contributor file {self.file_name} ingested"
            body  = (f"A new contributor's file was uploded and ingested, file name: {self.file_name}, schema: {self.schema_name}")
            body_html = f"""
            <html>
                <body>
                	<head>File Ingest Process</head>
            	    <h2 style='text-align:center'>New file was ingested</h1>
            	    <p>File name: <b>{self.file_name}</b></p>
            	    <p>Schema name: <b>{self.schema_name}<b></p>
            	</body>
            </html>
            """   
            response = self.client.send_email(
                Destination={
                    'ToAddresses': self.recipient
                },
                Message={
                    'Body': {
                        'Html': {
                            'Charset': self.charset,
                            'Data': body_html,
                        }
                    },
                    'Subject': {
                        'Charset': self.charset,
                        'Data': subject,
                    },
                },
                Source=self.sender,
            )
        # Display an error if something goes wrong.	
        except Exception as error:
            print(error)