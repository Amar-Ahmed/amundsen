import os
from dotenv import load_dotenv
from .secret import get_secret


"""
    Config class that get the values from an Enviroment File if is running in the server side
    if is running locally does not have to have a Environment File
"""


class Config:

    def __init__(self):
        load_dotenv()
        secret_name = "arn:aws:secretsmanager:us-east-1:310946103770:secret:edl-eudc-neo4j-db-jZwBQ9"
        region_name = "us-east-1"
        self.config = get_secret(secret_name, region_name)
        if self.config is None:
            self.config = {}

    # Return the path where the application is running
    def get_folder_name(self) -> str:
        folder_name = os.getenv('FOLDER_NAME',os.path.dirname( os.path.abspath(__file__)))
        return folder_name

    # return the hostname for the Neo4j Data Base server
    def get_neo4j_host(self) -> str:
        # return  os.getenv('CREDENTIALS_NEO4J_PROXY_HOST','localhost')
        return  self.config.get('host','localhost')

    # return the port where the Neo4j Server is running
    def get_neo4j_port(self) -> int:
        # return  int(os.getenv('CREDENTIALS_NEO4J_PROXY_PORT',7687))
        return  int( self.config.get('port',7687))

    # return the Neo4j data base user
    def get_neo4j_user(self) -> str:
        # return  os.getenv('CREDENTIALS_NEO4J_PROXY_USER','neo4j')
        return  self.config.get('user','neo4j')

    # return the password from the Neo4j Data base user
    def get_neo4j_password(self) -> str:
        # return  os.getenv('CREDENTIALS_NEO4J_PROXY_PASSWORD','test')
        return  self.config.get('password','test')