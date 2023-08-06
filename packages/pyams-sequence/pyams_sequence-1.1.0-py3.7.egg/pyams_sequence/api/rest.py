#
# Copyright (c) 2015-2021 Thierry Florac <tflorac AT ulthar.net>
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#

"""PyAMS_sequence.api.reference module

This modules defines REST API used to search internal references.
"""

import sys

from colander import MappingSchema, SchemaNode, SequenceSchema, String, drop
from cornice import Service
from cornice.validators import colander_querystring_validator
from pyramid.httpexceptions import HTTPOk

from pyams_security.interfaces.base import VIEW_SYSTEM_PERMISSION
from pyams_sequence.interfaces import ISequentialIntIds, REST_REFERENCES_SEARCH_ROUTE
from pyams_sequence.sequence import get_sequence_dict
from pyams_utils.registry import query_utility


__docformat__ = 'restructuredtext'

from pyams_sequence import _  # pylint: disable=ungrouped-imports


TEST_MODE = sys.argv[-1].endswith('/test')


class ReferencesSearchQuerySchema(MappingSchema):
    """Internal references search schema"""
    term = SchemaNode(String(),
                      title=_("References search string"),
                      description=_("Query can be an internal reference OID, eventually "
                                    "prefixed with a \"+\", or a text query which should "
                                    "match contents title"))
    content_type = SchemaNode(String(),
                              title=_("Content type"),
                              description=_("References search can be restricted to a given "
                                            "content type"),
                              missing=drop)


class ReferenceResultSchema(MappingSchema):
    """Reference result schema"""
    id = SchemaNode(String(),
                    description=_("Reference ID"))
    text = SchemaNode(String(),
                      description=_("Reference title"))


class ReferencesSearchResults(SequenceSchema):
    """References search results"""
    result = ReferenceResultSchema()


class ReferencesSearchResultsSchema(MappingSchema):
    """References search results schema"""
    results = ReferencesSearchResults(description=_("Results list"))


search_responses = {
    HTTPOk.code: ReferencesSearchResultsSchema(description=_("Search results")),
}
if TEST_MODE:
    service_params = {}
else:
    service_params = {
        'response_schemas': search_responses
    }

service = Service(name=REST_REFERENCES_SEARCH_ROUTE,
                  pyramid_route=REST_REFERENCES_SEARCH_ROUTE,
                  description="Internal references management")


@service.get(permission=VIEW_SYSTEM_PERMISSION,
             schema=ReferencesSearchQuerySchema(),
             validators=(colander_querystring_validator,),
             **service_params)
def find_references(request):
    """Returns list of references matching given query"""
    if TEST_MODE:
        query = request.params.get('term')
        content_type = request.params.get('content_type')
    else:
        query = request.validated.get('term')
        content_type = request.validated.get('content_type')
    if not query:
        return []
    sequence = query_utility(ISequentialIntIds)
    return {
        'results': sorted([
            get_sequence_dict(result)
            for result in sequence.find_references(query, content_type, request)
        ], key=lambda x: x['text'])
    }
