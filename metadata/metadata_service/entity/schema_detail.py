# Copyright Contributors to the Amundsen project.
# SPDX-License-Identifier: Apache-2.0

import attr
from marshmallow3_annotations.ext.attrs import AttrsSchema


@attr.s(auto_attribs=True, kw_only=True)
class SchemaDetail:
    schema: str = attr.ib()
    schema_title: str = attr.ib()
    schema_description: str = attr.ib()



class SchemaSchema(AttrsSchema):
    class Meta:
        target = SchemaDetail
        register_as_scheme = True