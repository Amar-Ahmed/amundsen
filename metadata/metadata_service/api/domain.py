# Copyright Contributors to the Amundsen project.
# SPDX-License-Identifier: Apache-2.0

from http import HTTPStatus
from typing import Any, Iterable, Mapping, Tuple, Union

from flasgger import swag_from
from flask import current_app as app
from flask_restful import Resource, fields, marshal, reqparse
from metadata_service.entity.domain import DomainSchema
from metadata_service.exception import NotFoundException
from metadata_service.proxy import get_proxy_client

domain_fields = {
    'domain_name': fields.String,
    'domain_description': fields.String,
    'domain_data_asset': fields.Boolean,
}

list_domain_fields = {
    'domains': fields.List(fields.Nested(domain_fields))
}

class DomainAPI(Resource):
    """
    Domain List
    """
    def __init__(self) -> None:
        self.client = get_proxy_client()
        super(DomainAPI, self).__init__()

    def get(self) -> Iterable[Union[Mapping, int, None]]:
        """
        API to fetch all the existing domain sort by date added
        """
        domain_list = self.client.get_domains()
        return marshal({'domains': domain_list}, list_domain_fields), HTTPStatus.OK


class DomainDetailAPI(Resource):
    """
    Domain Detail API
    """

    def __init__(self) -> None:
        self.client = get_proxy_client()
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('domain_name', type=str, required=True)
        super(DomainDetailAPI, self).__init__()

    def get(self, domain_name: str) -> Iterable[Union[Mapping, int, None]]:
        """
        API to fetch a specific domain information with the data asset profile related
        """
        try:
            domain = self.client.get_domain_detail(domain_name=domain_name)
            schema = DomainSchema()
            return  {'domains': [schema.dump(domain)]}, HTTPStatus.OK

        except NotFoundException:
            return {'message': 'Domain name {} does not exist'.format(domain_name)}, HTTPStatus.NOT_FOUND