from drf_yasg.utils import swagger_auto_schema
import json

response_ok = {
    "message": ["Password changed successfully"], 
    "code": 200, 
    "success": True, 
    "data": {}
    }

response_bad_request = {
    "message": ["Password and confirm password not match"], 
    "code": 400, 
    "success": False, 
    "data": {}}

response_unauthenticate = {
    "message": [
        "Authentication credentials were not provided."
    ],
    "code": 401,
    "success": False,
    "data": {},
    "paginator": {}
}

response_unauthorized={
    "message": [
            "You do not have permission to perform this action."
        ],
        "code": 403,
        "success": False,
        "data": []
}


swagger_auto_schema = swagger_auto_schema(
    responses={
        "200": json.dumps(response_ok),
        "400": json.dumps(response_bad_request),
        '401': json.dumps(response_unauthenticate),
        '403': json.dumps(response_unauthorized),
    },
    operation_id="change password",
    operation_description='API to change password \n \n requests::   {"old_password":"reset123","password": "123456","confirm_password": "123456"}',)
