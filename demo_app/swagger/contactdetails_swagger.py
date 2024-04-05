
from drf_yasg.openapi import Parameter, IN_QUERY, IN_PATH
from drf_yasg.utils import swagger_auto_schema
import json

response_list = {
    'message': [
        'Ok'
    ],
    'code': 200,
    'success': True,
    'data': []
}

response_get = {
    'message': [
        'Ok'
    ],
    'code': 200,
    'success': True,
    'data': {}
}

response_post = {
    'message': [
        'Contactdetails created'
    ],
    'code': 201,
    'success': True,
    'data': {}
}


response_update = {
    'message': [
        'Contactdetails updated'
    ],
    'code': 200,
    'success': True,
    'data': {}
}

response_delete = {
    'message': [
        'Contactdetails deleted'
    ],
    'code': 200,
    'success': True,
    'data': {}
}

response_unauthenticate = {
    'message': [
        "Authentication credentials were not provided."
    ],
    'code': 401,
    'success': True,
    'data': {}
}

response_unauthorized = {
    'message': [
        "You do not have permission to perform this action."
    ],
    'code': 403,
    'success': True,
    'data': {}

}

response_bad_request = {
    'message': [
        'Contactdetails already exists.'
    ],
    'code': 400,
    'success': True,
    'data': {}
}

response_not_found = {
    'message': [
        'Contactdetails not found'
    ],
    'code': 404,
    'success': True,
    'data': {}
}

swagger_auto_schema_list = swagger_auto_schema(
    manual_parameters=[
        Parameter('sort_by', IN_QUERY, description='sort by id', type='int'),
        Parameter('sort_direction', IN_QUERY, description='sort_direction in ascending,descending', type='char'),
        Parameter('id', IN_QUERY, description='id parameter', type='char'),
        Parameter('keyword', IN_QUERY, description='keyword paramater', type='char'),
        Parameter('page', IN_QUERY, description='page no. paramater', type='int'),
        Parameter('limit', IN_QUERY, description='limit paramater', type='int'),
        Parameter('type', IN_QUERY, description='All result set type=all', type='char'),
        

    ],
    responses={
        '200': json.dumps(response_list),
        '401': json.dumps(response_unauthorized),
        '403': json.dumps(response_unauthenticate),
        '404': json.dumps(response_not_found)
    },

    operation_id='list contactdetails',
    operation_description='API to list contactdetails data',
)

swagger_auto_schema_post = swagger_auto_schema(
    responses={
        '201': json.dumps(response_post),
        '400': json.dumps(response_bad_request),
        '401': json.dumps(response_unauthorized),
        '403': json.dumps(response_unauthenticate),
    },

    operation_id='Create contactdetails',
    operation_description='API to add new contactdetails request :: {}',
)

swagger_auto_schema_update = swagger_auto_schema(
    responses={
        '200': json.dumps(response_update),
        '400': json.dumps(response_bad_request),
        '401': json.dumps(response_unauthorized),
        '403': json.dumps(response_unauthenticate),
        '404': json.dumps(response_not_found),
    },

    operation_id='update contactdetails',
    operation_description='API to update contactdetails request :: {}',
)

swagger_auto_schema_delete = swagger_auto_schema(
    responses={
        '200': json.dumps(response_delete),
        '401': json.dumps(response_unauthorized),
        '403': json.dumps(response_unauthenticate),
        '404': json.dumps(response_not_found),
    },

    operation_id='delete contactdetails',
    operation_description='API to delete contactdetails',
)

swagger_auto_schema_bulk_delete = swagger_auto_schema(
    responses={
        '200': json.dumps(response_delete),
        '401': json.dumps(response_unauthorized),
        '403': json.dumps(response_unauthenticate),
        '404': json.dumps(response_not_found),
    },

    operation_id='delete contactdetails',
    operation_description='API to bulk delete contactdetails',
)

swagger_auto_schema = swagger_auto_schema(
    responses={
        '200': json.dumps(response_get),
        '403': json.dumps(response_unauthenticate),
        '401': json.dumps(response_unauthorized),
        '404': json.dumps(response_not_found),
    },

    operation_id='Fetch contactdetails',
    operation_description='API to fetch contactdetails',
)
    