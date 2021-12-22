import os
from dotenv import load_dotenv
load_dotenv()

"""
    Config class that get the values from an Enviroment File if is running in the server side
    if is running locally does not have to have a Environment File
"""

class Config:

    # Return the path where the application is running
    @staticmethod
    def get_folder_name() -> str:
        folder_name = os.getenv('FOLDER_NAME',os.path.dirname( os.path.abspath(__file__)))
        return folder_name

    # return the hostname for the Elastic Search service
    @staticmethod
    def get_elastic_search_host() -> str:
        return  os.getenv('CREDENTIALS_ELASTICSEARCH_PROXY_HOST','localhost')

    # return the port where is running  the Elastic Search service
    @staticmethod
    def get_elastic_search_port() -> int:
        return  int(os.getenv('CREDENTIALS_ELASTICSEARCH_PROXY_PORT',9200))

    # return the hostname for the Neo4j Data Base server
    @staticmethod
    def get_neo4j_host() -> str:
        return  os.getenv('CREDENTIALS_NEO4J_PROXY_HOST','localhost')

    # return the port where the Neo4j Server is running
    @staticmethod
    def get_neo4j_port() -> int:
        return  int(os.getenv('CREDENTIALS_NEO4J_PROXY_PORT',7687))

    # return the Neo4j data base user
    @staticmethod
    def get_neo4j_user() -> str:
        return  os.getenv('CREDENTIALS_NEO4J_PROXY_USER','neo4j')

    # return the password from the Neo4j Data base user
    @staticmethod
    def get_neo4j_password() -> str:
        return  os.getenv('CREDENTIALS_NEO4J_PROXY_PASSWORD','test')


