
from rest_framework import serializers
from ..models import Reports

class ReportsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reports
        fields = ['title', 'url_keywords', 'dc_description', 'report_display_title', 'report_description', 'table_of_contents', 'report_type', 'related_reports', 'video_link', 'meta_description', 'meta_title', 'meta_keywords', 'no_of_pages', 'published_date', 'author', 'continent', 'images', 'single_user_pdf_price', 'enterprise_pdf_price', 'five_user_pdf_price', 'site_pdf_price', 'add_report_scope']