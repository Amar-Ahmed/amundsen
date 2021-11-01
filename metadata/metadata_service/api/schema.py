# Copyright Contributors to the Amundsen project.
# SPDX-License-Identifier: Apache-2.0

from http import HTTPStatus
from typing import Any, Iterable, Mapping, Tuple, Union

from flasgger import swag_from
from flask import current_app as app
from flask_restful import Resource, fields, marshal

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
