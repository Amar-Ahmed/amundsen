
import attr
from marshmallow3_annotations.ext.attrs import AttrsSchema
from typing import List, Optional
from metadata_service.entity.schema_detail import SchemaDetail

@attr.s(auto_attribs=True, kw_only=True)
class Domain:
    domain_name: str = attr.ib()
    domain_description: str = attr.ib()
    domain_data_asset: bool = attr.ib(default=False)


@attr.s(auto_attribs=True, kw_only=True)
class DomainDetail:
    domain_name: str = attr.ib()
    domain_description: str = attr.ib()
    domain_updates: Optional[str] = attr.ib(default='')
    domain_contact: Optional[str] = attr.ib(default='')
    domain_data_asset: Optional[List[SchemaDetail]] = attr.ib(default=[])

class DomainSchema(AttrsSchema):
    class Meta:
        target = DomainDetail
        register_as_scheme = True