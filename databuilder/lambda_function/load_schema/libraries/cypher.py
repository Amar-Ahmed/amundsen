from neo4j import GraphDatabase
import logging
import textwrap
import time
from typing import (
    Any, Dict, Iterable, Optional,
)
from .config import Config


LOGGER = logging.getLogger(__name__)

#establish the connection
neo_host = Config.get_neo4j_host()
neo_port = Config.get_neo4j_port()
neo4j_endpoint = f'bolt://{neo_host}:{neo_port}'
neo4j_user = Config.get_neo4j_user()
neo4j_password = Config.get_neo4j_password()

"""
    This class makes the connection with Neo4j and execute the queries
"""
class Cypher:

    def __init__(self) -> None:
        self._driver= GraphDatabase.driver(uri=neo4j_endpoint, auth=(neo4j_user, neo4j_password))
        self.dry_run = False

    # Create the node in the Data Base recivin the node label and the properties
    def create_node(self, label: str, param_dictionary: Dict, str_parameters: str) -> None:
        statement =  textwrap.dedent("""
            MERGE (d: {label} {str_parameters})
            ON CREATE
            SET d.created = timestamp()
            RETURN d.name, d.created
        """)
        statement = statement.format(label=label, str_parameters=str_parameters)
        self._execute_cypher_query(
            statement=statement,
            param_dictionary=param_dictionary,
            dry_run=self.dry_run)
        LOGGER.info(f"Create node: {label} it's done")

    # Create the relationship between 2 nodes and add properties to the relationship
    def create_relationship(self, param_dictionary: Dict, dic_parameters: dict)-> None:
        statement = """
            MATCH
            (n1:{node1}),
            (n2:{node2})
            {where}
            CREATE (n1)-[:{relation} {properties}]->(n2)       
            CREATE (n2)-[:{relation_of} {properties}]->(n1)
        """
        statement = statement.format(**dic_parameters)
        self._execute_cypher_query(
            statement=statement,
            param_dictionary=param_dictionary,
            dry_run=self.dry_run
        )
        LOGGER.info(f"Create relationship between node: {dic_parameters.get('node1')} and node: {dic_parameters.get('node2')} it's done")

    # Delete the nodes that match the label and the schema 
    def delete_nodes(self, label: str, schema: Optional[str] = None) -> None:
        statement = textwrap.dedent("""
            MATCH (n:{label})
            {where}
            DETACH DELETE (n)
            RETURN COUNT(*) as count;
        """)
        where = ''
        if schema:
            where = f"WHERE n.key CONTAINS '{schema}'"
        statement = statement.format(label=label, where=where)
        self._execute_cypher_query(
            statement=statement,
            param_dictionary= {},
            dry_run=self.dry_run
        )
        LOGGER.info(f"Delete node: {label} it's done")
    
    # Delete the nodes that match the label and does not have schema in the properties
    def delete_stale_nodes_no_schema(self, label: str, schema: Optional[str] = None) -> None:
        statement = textwrap.dedent("""
            MATCH (n:{label})-[r]-(c)
            {where}
            DETACH DELETE (n)
            RETURN COUNT(*) as count;
        """)
        where = ''
        if schema:
            where = f"WHERE c.key CONTAINS '{schema}'"
        statement = statement.format(label=label, where=where)
        self._execute_cypher_query(
            statement=statement,
            param_dictionary= {},
            dry_run=self.dry_run
        )
        LOGGER.info(f"Delete node: {label} it's done")

    # Delete the relationship between nodes whit schema or without
    def delete_relationship(self, label: str, schema: Optional[str] = None) -> None:
        statement = textwrap.dedent("""
            MATCH ()-[r:{label}]-(c)
            {where}
            DELETE (r)
            RETURN COUNT(*) as count;
        """)
        where = ''
        if schema:
            where = f"WHERE c.key CONTAINS '{schema}'"
        statement = statement.format(label=label, where=where)
        self._execute_cypher_query(
            statement=statement,
            param_dictionary= {},
            dry_run=self.dry_run
        )
        LOGGER.info(f"Delete relationship for node: {label} it's done")

    # Execute any query that receive as parameter in Neo4j
    def _execute_cypher_query(self,
                              statement: str,
                              param_dictionary: Dict[str, Any] = {},
                              dry_run: bool = False
                              ) -> Iterable[Dict[str, Any]]:
        LOGGER.info('Executing Cypher query: %s with params %s: ', statement, param_dictionary)

        if dry_run:
            LOGGER.info('Skipping for it is a dryrun')
            return []

        start = time.time()
        try:
            with self._driver.session() as session:
                return session.run(statement, **param_dictionary)

        finally:
            LOGGER.debug('Cypher query execution elapsed for %i seconds', time.time() - start)