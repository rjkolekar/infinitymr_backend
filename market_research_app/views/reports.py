
import operator
from oauth2_provider.contrib.rest_framework import OAuth2Authentication
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from functools import reduce
from django.conf import settings
from simple_search import search_filter
from django.db import transaction

''' utility '''
from rest_apiresponse.apiresponse import ApiResponse
from utility.utils import MultipleFieldPKModelMixin, CreateRetrieveUpdateViewSet, get_serielizer_error, get_pagination_resp, transform_list
from utility.constants import *

''' model imports '''
from ..models import Reports

''' serializers '''
from ..serializers.reports_serializer import ReportsSerializer

''' swagger '''
# from ..swagger.reports_swagger import swagger_auto_schema_list, swagger_auto_schema_post, swagger_auto_schema, swagger_auto_schema_update, swagger_auto_schema_delete, swagger_auto_schema_bulk_delete

class ReportsView(MultipleFieldPKModelMixin, CreateRetrieveUpdateViewSet, ApiResponse):
    serializer_class = ReportsSerializer
    authentication_classes = [OAuth2Authentication, ]
    permission_classes = [IsAuthenticated]
    singular_name = 'Reports'
    model_class = Reports.objects.filter(status = STATUS_ACTIVE)
    
    search_fields = ['title', 'url_keywords', 'dc_description', 'report_display_title', 'report_description', 'table_of_contents', 'video_link', 'meta_description', 'meta_title', 'meta_keywords', 'no_of_pages', 'published_date', 'single_user_pdf_price', 'enterprise_pdf_price', 'five_user_pdf_price', 'site_pdf_price', 'add_report_scope']

    def get_object(self, pk):
        try:
            return self.model_class.get(pk=pk)
        except:
            return None

    # @swagger_auto_schema
    def retrieve(self, request, *args, **kwargs):
        '''
        :To get the single record
        '''
    
        ''' capture data '''
        get_id = self.kwargs.get('id')

        ''' process/format on data '''
        instance = self.get_object(get_id)
        if instance:
            resp_dict = self.transform_single(instance)

            # return success
            return ApiResponse.response_ok(self, data=resp_dict)

        return ApiResponse.response_not_found(self, message=self.singular_name + ' not found')

    # @swagger_auto_schema_post
    @transaction.atomic()
    def create(self, request, *args, **kwargs):
        '''
        :To create the new record
        '''
        sp1 = transaction.savepoint()
    
        ''' capture data '''
        req_data = request.data.copy()
        
        req_data["images"] = req_data.get("images_id")
        report_id = req_data.get('report_id')
        related_reports = req_data.get('related_reports')
        if related_reports:
            for related_report in related_reports:
                if not Reports.objects.filter(report_id=related_report, status = STATUS_ACTIVE).exists():
                    return ApiResponse.response_bad_request(self, message="Please add valid related report id.")
                
        if not report_id:
            # Get the latest report object
            latest_report = Reports.objects.order_by('-id').first()
            if not latest_report:
                new_report_id = "IMR1001" # Initial report ID if no reports exist
                
            else:
                last_report_id_str = latest_report.report_id
                if last_report_id_str is not None and last_report_id_str.startswith("IMR"):
                    last_report_id = int(last_report_id_str[3:])  # Extract the numeric part
                    new_report_id = "IMR" + str(last_report_id + 1).zfill(4)  # Increment by 1  
                else:
                    # Handle invalid report_id format
                    new_report_id = "IMR1001" 
            req_data['report_id'] = new_report_id
        serializer = self.serializer_class(data=req_data)

        ''' validate serializer '''
        if serializer.is_valid():
            serializer.save()
            serializer_instance = serializer.instance
            
            transaction.savepoint_commit(sp1)

            return ApiResponse.response_created(self, data=req_data,
                                                message=self.singular_name + ' created successfully.')

        ''' serializer error '''
        error_resp = get_serielizer_error(serializer)
        transaction.savepoint_rollback(sp1)
        return ApiResponse.response_bad_request(self, message=error_resp)

        

    # @swagger_auto_schema_update
    @transaction.atomic()
    def partial_update(self, request, *args, **kwargs):
        '''
        :To update the existing record
        '''
        sp1 = transaction.savepoint()
    
        ''' capture data '''
        req_data = request.data
        is_published = req_data.get('is_published')
        get_id = self.kwargs.get('id')
        instance = self.get_object(get_id)
        related_reports = req_data.get('related_reports')

        if instance is None:
            return ApiResponse.response_not_found(self, message=self.singular_name + ' not found')

        if is_published == True:
            req_data['is_published'] = True
        
        if related_reports:
            for related_report in related_reports:
                if not Reports.objects.filter(report_id=related_report, status = STATUS_ACTIVE).exists():
                    return ApiResponse.response_bad_request(self, message="Please add valid related report id.")
                
        ''' validate serializer '''
        serializer = self.serializer_class(instance, data=req_data, partial=True)
        if serializer.is_valid():
            serializer.save()
            serializer_instance = serializer.instance
            
            ''' success response '''
            response_data = self.transform_single(serializer_instance)
            transaction.savepoint_commit(sp1)

            return ApiResponse.response_ok(self, data=response_data, message=self.singular_name + ' updated')

        error_resp = get_serielizer_error(serializer)
        transaction.savepoint_rollback(sp1)
        return ApiResponse.response_bad_request(self, message=error_resp)

    # @swagger_auto_schema_list
    def list(self, request, *args, **kwargs):
        '''
        :To get the all records
        '''
    
        ''' capture data '''
        sort_by = request.query_params.get('sort_by') if request.query_params.get('sort_by') else 'id'
        
        sort_direction = request.query_params.get('sort_direction') if request.query_params.get(
            'sort_direction') else 'ascending'

        if sort_direction == 'descending':
            sort_by = '-' + sort_by

        where_array = request.query_params
        
        ''' filters '''
        obj_list = []
        
        report_type = where_array.get('report_type')
        obj_list = [('report_type__in',[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11] )]
        if report_type:
            report_type = int(report_type)
            if report_type in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]:
                obj_list = [('report_type__in', [report_type])]
            else:
                return ApiResponse.response_bad_request(self, message='Invalid report_type')
        author = where_array.get('author')
        obj_list = [('author__in',[1, 2] )]
        if author:
            author = int(author)
            if author in [1, 2]:
                obj_list = [('author__in', [author])]
            else:
                return ApiResponse.response_bad_request(self, message='Invalid author')
        continent = where_array.get('continent')
        obj_list = [('continent__in',[1, 2, 3] )]
        if continent:
            continent = int(continent)
            if continent in [1, 2, 3]:
                obj_list = [('continent__in', [continent])]
            else:
                return ApiResponse.response_bad_request(self, message='Invalid continent')
            
        # country = where_array.get('country')
        # if country:
        #     obj_list.append(('country_id', country))
            
        if where_array.get('is_published') == 'true':
            obj_list.append(('is_published', True))

        if where_array.get('report_id'):
            obj_list.append(('report_id', where_array.get('report_id')))
        
        start_date = where_array.get('start_date')
        end_date = where_array.get('end_date')
        if start_date and end_date:
            from datetime import datetime
            end_date = datetime.strptime(end_date, '%Y-%m-%d')
            end_date = datetime.combine(end_date, datetime.max.time())
            obj_list.append(['created_at__range', [start_date, end_date]])
        
        elif start_date:
            obj_list.append(['created_at__startswith', start_date])

        elif end_date:
            obj_list.append(['created_at__endswith', end_date])
        
        q_list = [Q(x) for x in obj_list]
        queryset = self.model_class.order_by(sort_by)
        if q_list:
            queryset = self.model_class.filter(reduce(operator.and_, q_list)).order_by(sort_by)
        
        if related_reports := where_array.get('related_reports'):
            if related_reports_list := [related_report for related_report in related_reports.split(',')]:
                queryset = queryset.filter(related_reports__contains = related_reports_list)

        ''' Search for keyword '''
        if where_array.get('keyword'):
            queryset = queryset.filter(search_filter(self.search_fields, where_array.get('keyword')))

        resp_data = get_pagination_resp(queryset, request)

        response_data = transform_list(self, resp_data.get('data'))

        return ApiResponse.response_ok(self, data=response_data, paginator=resp_data.get('paginator'))

    # @swagger_auto_schema_delete
    def delete(self, request, *args, **kwargs):
        '''
        :To delete the single record.
        '''
    
        get_id = self.kwargs.get('id')

        ''' get instance '''
        instance = self.get_object(get_id)
        if instance is None:
            return ApiResponse.response_not_found(self, message=self.singular_name + ' not found')

        instance.status = 3
        instance.save()

        ''' return success '''
        return ApiResponse.response_ok(self, message=self.singular_name + ' deleted')
    

    # @swagger_auto_schema_bulk_delete
    def bulk_delete(self, request, *args, **kwargs):
        '''
        :To delete the multiple record.
        '''
    
        ''' capture data '''
        req_data = request.data
        ids = req_data.get('ids')

        if ids is None or type(ids) != list:
            return ApiResponse.response_bad_request(self, message='Please select '+ self.singular_name)

        ''' get instance '''    
        queryset = self.model_class.filter(id__in=ids)
        if not queryset:
            return ApiResponse.response_not_found(self, message=self.singular_name + ' not found')

        queryset.update(status = 3)

        ''' return success '''
        return ApiResponse.response_ok(self, message=self.singular_name + ' deleted.')
    

    ##Generate the response
    def transform_single(self, instance):
        resp_dict = dict()
        resp_dict['id'] = instance.id
        resp_dict['title'] = instance.title
        resp_dict['url_keywords'] = instance.url_keywords
        resp_dict['dc_description'] = instance.dc_description
        resp_dict['report_display_title'] = instance.report_display_title
        resp_dict['report_description'] = instance.report_description
        resp_dict['table_of_contents'] = instance.table_of_contents
        resp_dict['report_type'] = instance.report_type
        resp_dict['report_type_name'] = instance.get_report_type_display()
        resp_dict['status'] = instance.status
        resp_dict['status_name'] = instance.get_status_display() 
        resp_dict['video_link'] = instance.video_link
        resp_dict['meta_description'] = instance.meta_description
        resp_dict['meta_title'] = instance.meta_title
        resp_dict['meta_keywords'] = instance.meta_keywords
        resp_dict['no_of_pages'] = instance.no_of_pages
        resp_dict['published_date'] = instance.published_date
        resp_dict['is_published'] = instance.is_published
        
        if instance.related_reports:
            resp_dict['related_reports'] = instance.related_reports

        if instance.report_id:
            resp_dict['report_id'] = instance.report_id

        # if instance.country.id:
        #     resp_dict['country_id'] = instance.country_id
        #     resp_dict['country_name'] = instance.country_name

        resp_dict['author'] = instance.author
        resp_dict['author_name'] = instance.get_author_display()

        resp_dict['continent'] = instance.continent
        resp_dict['continent_name'] = instance.get_continent_display()
        
        if instance.images_id:
            resp_dict['images'] = instance.images_id
            # resp_dict['image_name'] = str(instance.images.file_name)
            resp_dict['image_name_url'] = f"http://localhost:8000//media/{instance.images.file_name}"

        resp_dict['single_user_pdf_price'] = instance.single_user_pdf_price
        resp_dict['enterprise_pdf_price'] = instance.enterprise_pdf_price
        resp_dict['five_user_pdf_price'] = instance.five_user_pdf_price
        resp_dict['site_pdf_price'] = instance.site_pdf_price
        resp_dict['add_report_scope'] = instance.add_report_scope
        resp_dict['created_at'] = instance.created_at
        resp_dict['updated_at'] = instance.updated_at
        return resp_dict
        