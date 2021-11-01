# from pyhocon import ConfigFactory, ConfigTree
import logging
from cypher import Cypher
import json
from typing import  Dict
import datetime
# import time

LOGGER = logging.getLogger(__name__)


class Domain:

    def __init__(self, domain_list: list)-> None:
        self.domain_list = domain_list
        self.cypher = Cypher()

    @staticmethod
    def get_param_dicitonary(param_dictionary: Dict) -> str:
        str_parameters = {}
        for key in param_dictionary.keys():
            str_parameters[key] = f"${key}"
        str_parameters = json.dumps(str_parameters)
        return str_parameters.replace('"','')

    def create_relationship(self, domain_name: str, schema_key: str)-> None:
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

        self.cypher.create_relationship(param_dictionary=param_dictionary, str_parameters=str_parameters)

    def create_domain(self, param_dictionary: dict)-> None:
        label = 'Domain'
        str_parameters = self.get_param_dicitonary(param_dictionary)
        self.cypher.create_node(label=label, param_dictionary=param_dictionary, str_parameters=str_parameters)

    def delete_stale_data(self)-> None:
        label = 'Domain'
        self.cypher.delete_nodes(label=label)
        label = 'DOMAIN'
        self.cypher.delete_relationship(label=label)        
        label = 'DOMAIN_OF'
        self.cypher.delete_relationship(label=label)        

    def upload_domains(self):
        # delete the stale data (nodes and relationshipd)
        self.delete_stale_data()
        # create database, cluster, schema columns
        database= "hive"
        cluster= "gold"
        for domain in self.domain_list:
            param_dictionary = {
                "name": domain.get('name'),
                "description": domain.get('description'),
                "updates": domain.get('updates'),
                "contact": domain.get('contact'),
                "data_asset": domain.get('data_asset')
            }
            self.create_domain(param_dictionary=param_dictionary)
            for data_asset in domain.get('data_asset'):
                schema_key = f"{database}://{cluster}.hive_{data_asset}"
                self.create_relationship(domain_name=domain.get('name'), schema_key=schema_key)
