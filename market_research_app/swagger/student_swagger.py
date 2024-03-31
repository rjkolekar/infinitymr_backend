
# from drf_yasg.openapi import Parameter, IN_QUERY, IN_PATH
# from drf_yasg.utils import swagger_auto_schema
# import json

# response_list = {
#     "message": [
#         "Ok"
#     ],
#     "code": 200,
#     "success": True,
#     "data": [
#         {
#             "id": 1,
#             "name": "Rohini Mote",
#             "marks": 90.0,
#             "city": "Pune",
#             "status": 3,
#             "status_name": "active",
#             "gender": 1,
#             "gender_name": "male",
#             "email": "rohini@gmail.com",
#             "created_at": "2023-05-24T10:22:40.656038Z",
#             "updated_at": "2023-05-24T10:47:52.854618Z"
#         },
#         {
#             "id": 2,
#             "name": "Ashok Patil",
#             "marks": 88.0,
#             "city": "Pune",
#             "status": 1,
#             "status_name": "active",
#             "gender": 1,
#             "gender_name": "male",
#             "email": "ashok@gmail.com",
#             "created_at": "2023-05-24T10:44:08.861812Z",
#             "updated_at": "2023-05-24T10:44:08.861864Z"
#         }
#     ],
#     "paginator": {
#         "total_count": 2,
#         "total_pages": 1,
#         "current_page": 1,
#         "limit": 10
#     }
# }

# response_get = {
#     "message": [
#         "Ok"
#     ],
#     "code": 200,
#     "success": True,
#     "data": {
#         "id": 1,
#         "name": "Rohini Mote",
#         "marks": 90.0,
#         "city": "Pune",
#         "status": 3,
#         "status_name": "active",
#         "gender": 1,
#         "gender_name": "male",
#         "email": "rohini@gmail.com",
#         "created_at": "2023-05-24T10:22:40.656038Z",
#         "updated_at": "2023-05-24T10:47:52.854618Z"
#     }
# }

# response_post = {
#     "message": [
#         "Student created successfully."
#     ],
#     "code": 201,
#     "success": True,
#     "data": {
#         "name": "Ashok Patil",
#         "city": "Pune",
#         "email": "ashoka@gmail.com",
#         "marks": 88,
#         "gender": 1
#     }
# }

# response_update = {
#     "message": [
#         "Student updated"
#     ],
#     "code": 200,
#     "success": True,
#     "data": {
#         "id": 2,
#         "name": "Ashok Patil",
#         "city": "Pune",
#         "email": "ashokpatil@gmail.com",
#         "marks": 88,
#         "gender": 1
#     }
# }

# response_delete = {"message": ["Student deleted"], "code": 200, "success": True, "data": {}}

# response_unauthenticate = {
#     "message": ["Authentication credentials were not provided."],
#     "code": 403,
#     "success": True,
#     "data": {},
# }

# response_unauthorized = {"message": ["Unauthorized"], "code": 401, "success": True, "data": {}}

# response_bad_request = {"message": ["Student already exists."], "code": 400, "success": True, "data": {}}

# response_not_found = {"message": ["Student not found"], "code": 404, "success": True, "data": {}}

# swagger_auto_schema_list = swagger_auto_schema(
#     manual_parameters=[
#         Parameter('sort_by', IN_QUERY, description='sort by id', type='int'),
#         Parameter('sort_direction', IN_QUERY, description='sort_direction in ascending,descending', type='char'),
#         Parameter('id', IN_QUERY, description='id parameter', type='char'),
#         Parameter('keyword', IN_QUERY, description='keyword paramater', type='char'),
#         Parameter('page', IN_QUERY, description='page no. paramater', type='int'),
#         Parameter('limit', IN_QUERY, description='limit paramater', type='int'),
#         Parameter('type', IN_QUERY, description='All result set type=all', type='char'),
#         Parameter('status', IN_QUERY, description='status paramater', type='int'),
#         Parameter('gender', IN_QUERY, description='gender paramater', type='int'),

#         Parameter('start_date', IN_QUERY, description='start_date paramater', type='char'),

#         Parameter('end_date', IN_QUERY, description='end_date paramater', type='char'),

#     ],
#     responses={
#         '200': json.dumps(response_list),
#         '403': json.dumps(response_unauthenticate),
#         '401': json.dumps(response_unauthorized),
#     },

#     operation_id='list student',
#     operation_description='API to list student data',
# )

# swagger_auto_schema_post = swagger_auto_schema(
#     responses={
#         '201': json.dumps(response_post),
#         '403': json.dumps(response_unauthenticate),
#         '401': json.dumps(response_unauthorized),
#         '400': json.dumps(response_bad_request),
#     },

#     operation_id='Create student',
#     operation_description='API to add new student request::  {"name" : "Ashok Patil", "city" : "Pune", "email" : "ashoka@gmail.com", "marks" : 88, "gender" : 1}',
# )

# swagger_auto_schema_update = swagger_auto_schema(
#     responses={
#         '200': json.dumps(response_update),
#         '403': json.dumps(response_unauthenticate),
#         '401': json.dumps(response_unauthorized),
#         '400': json.dumps(response_bad_request),
#         '404': json.dumps(response_not_found),
#     },

#     operation_id='update student',
#     operation_description='API to add new student request::  {"id" : 2, "name" : "Ashok Patil", "city" : "Pune", "email" : "ashokpatil@gmail.com", "marks" : 88, "gender" : 1}',
# )

# swagger_auto_schema_delete = swagger_auto_schema(
#     responses={
#         '200': json.dumps(response_delete),
#         '403': json.dumps(response_unauthenticate),
#         '401': json.dumps(response_unauthorized),
#         '404': json.dumps(response_not_found),
#     },

#     operation_id='delete student',
#     operation_description='API to delete student',
# )

# swagger_auto_schema_bulk_delete = swagger_auto_schema(
#     responses={
#         '200': json.dumps(response_delete),
#         '403': json.dumps(response_unauthenticate),
#         '401': json.dumps(response_unauthorized),
#         '404': json.dumps(response_not_found),
#     },

#     operation_id='delete student',
#     operation_description='API to bulk delete student',
# )

# swagger_auto_schema = swagger_auto_schema(
#     responses={
#         '200': json.dumps(response_get),
#         '403': json.dumps(response_unauthenticate),
#         '401': json.dumps(response_unauthorized),
#         '404': json.dumps(response_not_found),
#     },

#     operation_id='Fetch student',
#     operation_description='API to fetch student',
# )
    