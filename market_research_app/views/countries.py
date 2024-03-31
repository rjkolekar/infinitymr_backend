from functools import reduce
import operator
from django.db.models import Q
from simple_search import search_filter
from rest_framework.permissions import IsAuthenticated
from oauth2_provider.contrib.rest_framework import OAuth2Authentication
from django.db import transaction
# from job_portal.permissions import has_permissions, is_super_user, super_user_or_employer_job_seeker

""" utility """
from utility.response import ApiResponse
from utility.utils import (
    MultipleFieldPKModelMixin,
    CreateRetrieveUpdateViewSet,
    create_or_update_serializer,
    filter_date,
    get_pagination_resp,
    transform_list,
    validate_empty_strings,
)
from utility.constants import *

""" model imports """
from ..models import Countries

''' serializers '''
from ..serializers.countries_serializer import CountriesSerializer


"""swagger"""
# from ..swagger.countries_swagger import (
#     swagger_auto_schema_list,
#     swagger_auto_schema_post,
#     swagger_auto_schema,
#     swagger_auto_schema_update,
#     swagger_auto_schema_delete,
#     swagger_auto_schema_bulk_delete
# )


class CountryView(MultipleFieldPKModelMixin, CreateRetrieveUpdateViewSet, ApiResponse):
    authentication_classes = [OAuth2Authentication]
    permission_classes = [IsAuthenticated]
    serializer_class = CountriesSerializer
    singular_name = "Country"
    model_class = Countries.objects.filter(status__in=[STATUS_ACTIVE, STATUS_INACTIVE])

    search_fields = ["name"]

    def get_object(self, pk):
        try:
            return self.model_class.get(pk=pk)
        except:
            return None

    # @swagger_auto_schema
    def retrieve(self, request, *args, **kwargs):
        """
        :To get the single record
        """
        """ capture data """
        get_id = self.kwargs.get("id")

        """ process/format on data """
        instance = self.get_object(get_id)
        if instance:
            if request.query_params.get("is_all_data"):
                resp_dict = self.transform_single_with_to_dict(instance)
            else:    
                resp_dict = self.transform_single(instance)

            # return success
            return ApiResponse.response_ok(self, data=resp_dict)

        return ApiResponse.response_not_found(self, message=self.singular_name + " not found.")

    # @swagger_auto_schema_post
    # @transaction.atomic()
    def create(self, request, *args, **kwargs):
        """
        :To create the new record
        """
        sp1 = transaction.savepoint()

        """ capture data """
        req_data = request.data.copy()
        if not req_data:
            return ApiResponse.response_bad_request(self, message=MESSAGES['all_fields_should_not_empty'])
        
        name = req_data.get("name")
        # phone_code = req_data.get("phone_code")

        if not name:
            return ApiResponse.response_bad_request(self, message="Name is required.")

        if error_message := validate_empty_strings({"name":name}, req_data):
            return ApiResponse.response_bad_request(self, message=error_message)
        
        if self.model_class.filter(name__iexact=name.strip()).exists():
            return ApiResponse.response_bad_request(self, message="Country already exists.")

        req_data["status"] = STATUS_ACTIVE
        req_data["name"] = name.strip()        

        """ validate serializer """
        country_instance, error = create_or_update_serializer(self.serializer_class, req_data, sp1)
        if error:
            return ApiResponse.response_bad_request(self, message=error)

        """ success response """
        transaction.savepoint_commit(sp1)
        return ApiResponse.response_created(self, data=req_data, message=self.singular_name + MESSAGES["created"])

    # @swagger_auto_schema_update
    @transaction.atomic()
    def partial_update(self, request, *args, **kwargs):
        """
        :To update the existing record
        """
        sp1 = transaction.savepoint()

        """ capture data """
        req_data = request.data
        if not req_data:
            return ApiResponse.response_bad_request(self, message=MESSAGES['all_fields_should_not_empty'])
        
        get_id = self.kwargs.get("id")
        instance = self.get_object(get_id)
        if not instance:
            return ApiResponse.response_not_found(self, message=self.singular_name + " not found.")
        
        name = req_data.get("name")
        # phone_code = req_data.get("phone_code")
        status = req_data.get("status")
        
        if error_message := validate_empty_strings({"name":name}, req_data):
            return ApiResponse.response_bad_request(self, message=error_message)

        if status and status not in [STATUS_ACTIVE, STATUS_INACTIVE]:
            return ApiResponse.response_bad_request(self, message="Invalid status.")
        
        if name:
            if self.model_class.filter(name__iexact=name.strip()).exclude(id=instance.id).exists():
                return ApiResponse.response_bad_request(self, message="Country already exists.")
        
            req_data["name"] = name.strip()        
                
        """ validate serializer """
        country_instance, error = create_or_update_serializer(self.serializer_class, req_data, sp1, instance)
        if error:
            return ApiResponse.response_bad_request(self, message=error)

        """ success response """
        transaction.savepoint_commit(sp1)
        return ApiResponse.response_ok(self, data=req_data, message=self.singular_name + MESSAGES["updated"])

    # @swagger_auto_schema_list
    def list(self, request, *args, **kwargs):
        """
        :To get the all records
        """
        where_array = request.query_params

        # capture data
        sort_by = where_array.get("sort_by") if where_array.get("sort_by") else "id"

        sort_direction = where_array.get("sort_direction") if where_array.get("sort_direction") else "ascending"

        if sort_direction == "descending":
            sort_by = "-" + sort_by

        obj_list = []

        if where_array.get("id"):
                obj_list.append(("id", where_array.get("id")))  

        if status := where_array.get("status"):
            status = int(status)
            if status in [STATUS_INACTIVE, STATUS_ACTIVE]:
                obj_list.append(("status", status))
            else:
                return ApiResponse.response_bad_request(self, message="Invalid status.")

        start_date = where_array.get("start_date")
        end_date = where_array.get("end_date")
        obj_list = filter_date(start_date, end_date, obj_list)

        q_list = [Q(x) for x in obj_list]
        if q_list:
            queryset = self.model_class.filter(reduce(operator.and_, q_list)).order_by(sort_by)
        else:
            queryset = self.model_class.order_by(sort_by)

        """Search for keyword"""
        if where_array.get("keyword"):
            queryset = queryset.filter(search_filter(self.search_fields, where_array.get("keyword")))

        resp_data = get_pagination_resp(queryset, request)

        if is_all_data:=request.query_params.get("is_all_data"):
            response_data = transform_list(self, resp_data.get("data"), is_all_data)
            
        else:
            response_data = transform_list(self, resp_data.get("data"))

        return ApiResponse.response_ok(self, data=response_data, paginator=resp_data.get("paginator"))

    # @swagger_auto_schema_delete
    def delete(self, request, *args, **kwargs):
        """
        :To delete the single record.
        """
        get_id = self.kwargs.get("id")

        """ get instance """
        instance = self.get_object(get_id)
        if not instance:
            return ApiResponse.response_not_found(self, message=self.singular_name + " not found.")

        instance.status=STATUS_DELETED
        instance.save()

        """ return success """
        return ApiResponse.response_ok(self, message=self.singular_name + " deleted.")

    # @swagger_auto_schema_bulk_delete
    def bulk_delete(self, request, *args, **kwargs):
        """
        :To delete the multiple record.
        """
        """ capture data """
        req_data = request.data
        ids = req_data.get("ids")

        if not ids or type(ids) != list:
            return ApiResponse.response_bad_request(self, message="Please select " + self.singular_name.lower())

        """ get instance """
        queryset = self.model_class.filter(id__in=ids)
        if not queryset:
            return ApiResponse.response_not_found(self, message=self.singular_name + " not found.")

        queryset.update(status=STATUS_DELETED)

        """ return success """
        return ApiResponse.response_ok(self, message="Country deleted.")

    # Generate the response
    def transform_single(self, instance):
        resp_dict = {}
        if instance:
            resp_dict['id'] = instance.id
            resp_dict['name'] = instance.name
        
        return resp_dict


    # Generate the response
    def transform_single_with_to_dict(self, instance):
        resp_dict = {}
        resp_dict = Countries.to_dict(instance)
        
        return resp_dict  