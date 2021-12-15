# Copyright Contributors to the Amundsen project.
# SPDX-License-Identifier: Apache-2.0

from http import HTTPStatus
from typing import Any, Dict, Iterable, Mapping, Tuple, Union, Optional

from flasgger import swag_from
from flask import current_app as app
from flask_restful import Resource, fields, marshal, reqparse
from metadata_service.entity.schema_detail import SchemaSchema
from metadata_service.entity.resource_type import ResourceType
from metadata_service.exception import NotFoundException
from metadata_service.proxy import get_proxy_client
from metadata_service.proxy.base_proxy import BaseProxy

schema_fields = {
    'schema': fields.String,
    'schema_title': fields.String,
    'schema_description': fields.String
}

list_schema_fields = {
    'schemas': fields.List(fields.Nested(schema_fields))
}


class SchemaAPI(Resource):
    def __init__(self) -> None:
        self.client = get_proxy_client()
        super(SchemaAPI, self).__init__()

    def get(self) -> Iterable[Union[Mapping, int, None]]:
        """
        API to fetch all the existing schemas.
        """
        schema_list = self.client.get_schemas()
        return marshal({'schemas': schema_list}, list_schema_fields), HTTPStatus.OK


class SchemaDetailAPI(Resource):
    """
    Schema Detail API
    """

    def __init__(self) -> None:
        self.client = get_proxy_client()
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('schema_name', type=str, required=True)
        super(SchemaDetailAPI, self).__init__()

    def get(self, schema_name: str) -> Optional[Dict]:
        """
        API to fetch a specific schema information 
        """
        try:
            schema_detail = self.client.get_schema_detail(schema_name=schema_name)
            schema = SchemaSchema()
            return  {'schemas': [schema.dump(schema_detail)]}, HTTPStatus.OK

        except NotFoundException:
            return {'message': 'Schema name {} does not exist'.format(schema_name)}, HTTPStatus.NOT_FOUND