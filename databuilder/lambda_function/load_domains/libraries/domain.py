# from pyhocon import ConfigFactory, ConfigTree
import logging
import json
from typing import  Dict
import datetime
from .cypher import Cypher


LOGGER = logging.getLogger(__name__)

"""
    This class generate the script from the domains list to
    create the nodes and relationship in Neo4j
"""
class Domain:

    def __init__(self, domain_list: list)-> None:
        self.domain_list = domain_list
        self.cypher = Cypher()

    @staticmethod
    def get_param_dicitonary(param_dictionary: Dict) -> str:
        """ Get the domains name and properties """
        dict_parameters = {}
        for key in param_dictionary.keys():
            dict_parameters[key] = f"${key}"
        str_parameters = json.dumps(dict_parameters)
        return str_parameters.replace('"','')

    def create_relationship(self, domain_name: str, schema_key: str)-> None:
        """ Generate and execute the relationship script """
        str_parameters = {
            "node1": "Schema",
            "node2": "Domain",
            "relation": "DOMAIN",
            "relation_of": "DOMAIN_OF",
            "properties": """{
                publisher_last_updated_epoch_ms: $publisher_last_updated_epoch_ms,
                published_tag: $published_tag
                }
            """,
            "where": "WHERE n1.key = $key AND n2.name = $name"
        }

        param_dictionary = {
            "key": schema_key,
            "name": domain_name,
            "publisher_last_updated_epoch_ms": int(datetime.datetime.now().timestamp()),
            "published_tag": "unique_tag"
        }

        self.cypher.create_relationship(param_dictionary=param_dictionary, dic_parameters=str_parameters)

    def create_domain(self, param_dictionary: dict)-> None:
        """ Generate and execute the domains nodes"""
        str_parameters = self.get_param_dicitonary(param_dictionary)
        self.cypher.create_node(label='Domain', param_dictionary=param_dictionary, str_parameters=str_parameters)

    def delete_stale_data(self)-> None:
        """ Delete the nodes and relationship """
        self.cypher.delete_nodes(label='Domain')
        self.cypher.delete_relationship(label='DOMAIN')        
        self.cypher.delete_relationship(label='DOMAIN_OF')        

    def upload_domains(self):
        """ Execute all the necessary methods to start the domains creation """
        # delete the stale data (nodes and relationshipd)
        self.delete_stale_data()
        # create database, cluster, schema columns
        database= "hive"
        cluster= "gold"
        # read from the domain list and create the scripts
        # to create nodes and relationships
        for domain in self.domain_list:
            param_dictionary = {
                "name": domain.get('name'),
                "description": domain.get('description'),
                "updates": domain.get('updates'),
                "contact": domain.get('contact'),
                "data_asset": domain.get('data_asset')
            }
            # create the script for the noes
            self.create_domain(param_dictionary=param_dictionary)
            for data_asset in domain.get('data_asset'):
                schema_key = f"{database}://{cluster}.{data_asset}"
                # create the script for the relationship
                self.create_relationship(domain_name=domain.get('name'), schema_key=schema_key)
