
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
from ..models import Reports, Countries

''' serializers '''
from ..serializers.reports_serializer import ReportsSerializer

''' swagger '''
# from ..swagger.reports_swagger import swagger_auto_schema_list, swagger_auto_schema_post, swagger_auto_schema, swagger_auto_schema_update, swagger_auto_schema_delete, swagger_auto_schema_bulk_delete

class ReportsListView(MultipleFieldPKModelMixin, CreateRetrieveUpdateViewSet, ApiResponse):
    serializer_class = ReportsSerializer
    singular_name = 'Reports'
    model_class = Reports.objects.filter(status = STATUS_ACTIVE)
    
    search_fields = ['title', 'url_keywords', 'dc_description', 'report_display_title', 'report_description', 'table_of_contents', 'video_link', 'meta_description', 'meta_title', 'meta_keywords', 'no_of_pages', 'published_date', 'single_user_pdf_price', 'enterprise_pdf_price', 'five_user_pdf_price', 'site_pdf_price', 'add_report_scope']

    def get_object(self, pk):
        try:
            return self.model_class.get(pk=pk)
        except:
            return None

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
        
        related_reports = where_array.get('related_reports')
        if related_reports:
            obj_list.append(('related_reports_id', related_reports))
            
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
        