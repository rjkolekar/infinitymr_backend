# import json
# import operator
# from oauth2_provider.contrib.rest_framework import OAuth2Authentication
# from rest_framework.permissions import IsAuthenticated
# from django.db.models import Q
# from functools import reduce
# from django.conf import settings
# from simple_search import search_filter
# from django.db import transaction

# ''' utility '''
# from rest_apiresponse.apiresponse import ApiResponse

# from utility.utils import MultipleFieldPKModelMixin, CreateRetrieveUpdateViewSet, get_serielizer_error, get_pagination_resp, transform_list
# from utility.constants import *

# ''' model imports '''
# from ..models import Student

# ''' serializers '''
# from ..serializers.student_serializer import StudentSerializer

# ''' swagger '''
# from ..swagger.student_swagger import swagger_auto_schema_list, swagger_auto_schema_post, swagger_auto_schema, swagger_auto_schema_update, swagger_auto_schema_delete, swagger_auto_schema_bulk_delete

# class StudentView(MultipleFieldPKModelMixin, CreateRetrieveUpdateViewSet, ApiResponse):
#     serializer_class = StudentSerializer
#     authentication_classes = [OAuth2Authentication, ]
#     permission_classes = [IsAuthenticated]
#     singular_name = 'Student'
#     model_class = Student.objects
    
#     search_fields = ['name', 'city', 'marks', 'email']

#     def get_object(self, pk):
#         try:
#             return self.model_class.get(pk=pk)
#         except:
#             return None

#     @swagger_auto_schema
#     def retrieve(self, request, *args, **kwargs):
#             '''
#             :To get the single record
#             '''
#             # capture data
#             get_id = self.kwargs.get('id')

#             # process/format on data
#             instance = self.get_object(get_id)
#             if instance:
#                 resp_dict = self.transform_single(instance)

#                 # return success
#                 return ApiResponse.response_ok(self, data=resp_dict)

#             return ApiResponse.response_not_found(self, message=self.singular_name + ' not found')

#     @swagger_auto_schema_post
#     @transaction.atomic()
#     def create(self, request, *args, **kwargs):
#             '''
#             :To create the new record
#             '''
#             sp1 = transaction.savepoint()
        
#             ''' capture data '''
#             req_data = request.data.copy()
#             email = req_data.get('email')
            
#             required_filed = ['name', 'city', 'email']
#             for key in required_filed:
#                 if not req_data.get(key):
#                     return ApiResponse.response_bad_request(self, message=f"{key} is required")
            
#             if email:
#                 is_email_exist = self.model_class.filter(email=req_data.get('email')).first()
#                 if is_email_exist:
#                     return ApiResponse.response_bad_request(self, message="Email is already exist")

#             serializer = self.serializer_class(data=req_data)

#             ''' validate serializer '''
#             if serializer.is_valid():
#                 serializer.save()
#                 serializer_instance = serializer.instance
                
#                 transaction.savepoint_commit(sp1)
#                 return ApiResponse.response_created(self, data=req_data,
#                                                     message=self.singular_name + ' created successfully.')

#             ''' serializer error '''
#             error_resp = get_serielizer_error(serializer)
#             transaction.savepoint_rollback(sp1)
#             return ApiResponse.response_bad_request(self, message=error_resp)

#     @swagger_auto_schema_update
#     @transaction.atomic()
#     def partial_update(self, request, *args, **kwargs):
#             '''
#             :To update the existing record
#             '''
#             sp1 = transaction.savepoint()
        
#             ''' capture data '''
#             req_data = request.data
#             get_id = self.kwargs.get('id')
#             instance = self.get_object(get_id)

#             email = req_data.get('email')

#             if instance is None:
#                 return ApiResponse.response_not_found(self, message=self.singular_name + ' not found')

#             if email:
#                 is_email_exist = self.model_class.filter(email=req_data.get('email')).first()
#                 if is_email_exist:
#                     return ApiResponse.response_bad_request(self, message="Email is already exist")               

#             ''' validate serializer '''
#             serializer = self.serializer_class(instance, data=req_data, partial=True)
#             if serializer.is_valid():
#                 serializer.save()
#                 serializer_instance = serializer.instance
                
#                 ''' success response '''
#                 response_data = self.transform_single(serializer_instance)
#                 transaction.savepoint_commit(sp1)

#                 return ApiResponse.response_ok(self, data=req_data, message=self.singular_name + ' updated')

#             error_resp = get_serielizer_error(serializer)
#             transaction.savepoint_rollback(sp1)
#             return ApiResponse.response_bad_request(self, message=error_resp)


#     @swagger_auto_schema_list
#     def list(self, request, *args, **kwargs):
#             '''
#             :To get the all records
#             '''
#             # capture data
#             sort_by = request.query_params.get('sort_by') if request.query_params.get('sort_by') else 'id'
            
#             sort_direction = request.query_params.get('sort_direction') if request.query_params.get(
#                 'sort_direction') else 'ascending'

#             if sort_direction == 'descending':
#                 sort_by = '-' + sort_by

#             where_array = request.query_params

#             obj_list = []
            
#             if where_array.get("status"):
#                 status = int(where_array.get("status"))
#                 if status in [STATUS_INACTIVE, STATUS_ACTIVE]:
#                     obj_list.append(("status", status))
#                 else:
#                     return ApiResponse.response_bad_request(self, message='invalid status')
            
#             if where_array.get("gender"):
#                 gender = int(where_array.get("gender"))
#                 if gender in [MALE, FEMALE, OTHER]:
#                     obj_list.append(("gender", gender))
#                 else:
#                     return ApiResponse.response_bad_request(self, message="invalid gender")


#             start_date = where_array.get('start_date')
#             end_date = where_array.get('end_date')
#             if start_date and end_date:
#                 from datetime import datetime
#                 end_date = datetime.strptime(end_date, '%Y-%m-%d')
#                 end_date = datetime.combine(end_date, datetime.max.time())
#                 obj_list.append(['created_at__range', [start_date, end_date]])
            
#             elif start_date:
#                 obj_list.append(['created_at__startswith', start_date])

#             elif end_date:
#                 obj_list.append(['created_at__endswith', end_date])
            
#             q_list = [Q(x) for x in obj_list]
#             queryset = self.model_class.order_by(sort_by)
#             if q_list:
#                 queryset = self.model_class.filter(reduce(operator.and_, q_list)).order_by(sort_by)

#             '''Search for keyword'''
#             if where_array.get('keyword'):
#                 queryset = queryset.filter(search_filter(self.search_fields, where_array.get('keyword')))

#             resp_data = get_pagination_resp(queryset, request)

#             response_data = transform_list(self, resp_data.get('data'))

#             return ApiResponse.response_ok(self, data=response_data, paginator=resp_data.get('paginator'))

#     @swagger_auto_schema_delete
#     def delete(self, request, *args, **kwargs):
#             '''
#             :To delete the single record.
#             '''
        
#             get_id = self.kwargs.get('id')

#             ''' get instance '''
#             instance = self.get_object(get_id)
#             if instance is None:
#                 return ApiResponse.response_not_found(self, message=self.singular_name + ' not found')

#             instance.status = STATUS_DELETED
#             instance.save()

#             ''' return success '''
#             return ApiResponse.response_ok(self, message=self.singular_name + ' deleted')

#     @swagger_auto_schema_bulk_delete
#     def bulk_delete(self, request, *args, **kwargs):
#             '''
#             :To delete the multiple record.
#             '''
        
#             ''' capture data '''
#             req_data = request.data
#             print(req_data)
#             ids = req_data.get('ids')

#             if ids is None or type(ids) != list:
#                 return ApiResponse.response_bad_request(self, message='Please select '+ self.singular_name)

#             queryset = self.model_class.filter(id__in=ids)

#             if not queryset:
#                 return ApiResponse.response_not_found(self, message=self.singular_name + ' not found')

#             queryset.update(status = 3)

#             ''' return success '''
#             return ApiResponse.response_ok(self, message=self.singular_name + ' deleted.')

#     # Generate the response
#     def transform_single(self, instance):
#         resp_dict = Student.to_dict(instance)
#         return resp_dict
        