from django.db import models
from ..model.base import Base
                    
from ..models import Countries, Assets

class Reports(Base):
    ''' Model Fields '''
            
    title = models.TextField(unique=False, null=True, blank=True, db_index=True)
    url_keywords = models.TextField(unique=False, null=True, blank=True, db_index=True)
    dc_description = models.TextField(unique=False, null=True, blank=True, db_index=True)
    report_display_title = models.TextField(unique=False, null=True, blank=True, db_index=True)
    report_description = models.TextField(unique=False, null=True, blank=True, db_index=True)
    table_of_contents = models.TextField(unique=False, null=True, blank=True, db_index=True)
    REPORT_TYPE_BY = ((1, 'Aerospace&Defense'),(2, 'Agriculture'),(3, 'Automotive&Transportation'),(4, 'Building&Construction'),(5, 'Chemicals&Materials'),(6, 'ConsumerGoods'),(7, 'Electronics&Semiconductors'),(8, 'Energy&NaturalResources'),(9, 'Food&Beverages'),(10, 'Healthcare&LifeSciences'),(11, 'HeavyEngineering'),)
    report_type = models.IntegerField(choices=REPORT_TYPE_BY)
    related_reports = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='related_reports_reports', db_index=True)
    video_link = models.CharField(unique=False, null=True, blank=True, max_length=255, db_index=True)
    meta_description = models.TextField(unique=False, null=True, blank=True, db_index=True)
    meta_title = models.CharField(unique=False, null=True, blank=True, max_length=255, db_index=True)
    meta_keywords = models.TextField(unique=False, null=True, blank=True, db_index=True)
    no_of_pages = models.IntegerField(unique=False, null=True, blank=True, db_index=True)
    published_date = models.DateField(unique=False, null=True, blank=True, db_index=True)
    # country = models.ForeignKey(Countries, on_delete=models.SET_NULL, null=True, blank=True, related_name='country_reports', db_index=True)
    is_published = models.BooleanField(default= False, null=True, blank=True, db_index=True)
    AUTHOR_BY = ((1, 'Infinitymarketresearch'),(2, 'Gajanan'),)
    author = models.IntegerField(choices=AUTHOR_BY)

    report_id = models.CharField(unique=True, null=True, blank=True, max_length=25, db_index=True)

    CONTINENT_BY = ((1, 'Asia'),(2, 'Africa'),(3, 'NorthAmerica'),)
    continent = models.IntegerField(choices=CONTINENT_BY)
    images = models.ForeignKey(Assets, on_delete=models.SET_NULL, null=True, blank=True, db_index=True)
    single_user_pdf_price = models.FloatField(null=True, blank=True, default=0.0, db_index=True)
    enterprise_pdf_price = models.FloatField(null=True, blank=True, default=0.0, db_index=True)
    five_user_pdf_price = models.FloatField(null=True, blank=True, default=0.0, db_index=True)
    site_pdf_price = models.FloatField(null=True, blank=True, default=0.0, db_index=True)
    add_report_scope = models.TextField(unique=False, null=True, blank=True, db_index=True)

    STATUS_CHOICES = ((1, 'active'),(2, 'inactive'),(3,'deleted'))
    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES, default=1)

    class Meta:
        db_table = 'reports'

    def __str__(self):
        return str(self.pk)
    
    @staticmethod    
    def to_dict(instance):
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
        resp_dict['video_link'] = instance.video_link
        resp_dict['meta_description'] = instance.meta_description
        resp_dict['meta_title'] = instance.meta_title
        resp_dict['meta_keywords'] = instance.meta_keywords
        resp_dict['no_of_pages'] = instance.no_of_pages
        resp_dict['published_date'] = instance.published_date
        resp_dict['is_published'] = instance.is_published
        
        if instance.report_id:
            resp_dict['report_id'] = instance.report_id
            
        resp_dict['author'] = instance.author
        resp_dict['author_name'] = instance.get_author_display()
        resp_dict['continent'] = instance.continent
        resp_dict['continent_name'] = instance.get_continent_display()
        resp_dict['status'] = instance.continent
        resp_dict['status_name'] = instance.get_status_display()
        if instance.images_id:
            resp_dict['images'] = instance.images_id
            resp_dict['image_name'] = instance.images_id.file_name
        resp_dict['single_user_pdf_price'] = instance.single_user_pdf_price
        resp_dict['enterprise_pdf_price'] = instance.enterprise_pdf_price
        resp_dict['five_user_pdf_price'] = instance.five_user_pdf_price
        resp_dict['site_pdf_price'] = instance.site_pdf_price
        resp_dict['add_report_scope'] = instance.add_report_scope
        resp_dict['created_at'] = instance.created_at
        resp_dict['updated_at'] = instance.updated_at
        return resp_dict
        