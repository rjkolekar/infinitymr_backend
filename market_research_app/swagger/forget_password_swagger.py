from drf_yasg.utils import swagger_auto_schema
import json

response_ok = {
    "message": ["Link successfully sent to yor email."],
    "code": 200,
    "success": True,
    "data": {},
}

response_bad_request = {
    "message": ["Email not provided."],
    "code": 400,
    "success": False,
    "data": {},
}

response_not_found = {
    "message": ["User with this email does not exist."], 
    "code": 404, 
    "success": False, 
    "data": {}
    }

swagger_auto_schema = swagger_auto_schema(
    responses={
        "200": json.dumps(response_ok),
        "400": json.dumps(response_bad_request),
        "404": json.dumps(response_not_found),
    },
    operation_id="forget password",
    operation_description='API to forget password \n \n request:: {"email": "anup@gmail.com"}',
)
