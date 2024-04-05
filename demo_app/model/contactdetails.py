from django.db import models
from ..model.base import Base
                    
class Contactdetails(Base):
    ''' Model Fields '''
            
    name = models.CharField(unique=False, null=True, blank=True, max_length=255, db_index=True)
    company_name = models.CharField(unique=False, null=True, blank=True, max_length=255, db_index=True)
    job_title = models.CharField(unique=False, null=True, blank=True, max_length=500, db_index=True)
    mobile = models.CharField(unique=False, null=True, blank=True, max_length=20, db_index=True)
    email = models.EmailField(unique=False, null=True, blank=True, max_length=100, db_index=True)
    message = models.TextField(unique=False, null=True, blank=True, db_index=True)

    class Meta:
        db_table = 'contactdetails'

    def __str__(self):
        return str(self.pk)
    
    @staticmethod    
    def to_dict(instance):
        resp_dict = dict()
        resp_dict['id'] = instance.id
        resp_dict['name'] = instance.name
        resp_dict['company_name'] = instance.company_name
        resp_dict['job_title'] = instance.job_title
        resp_dict['mobile'] = instance.mobile
        resp_dict['email'] = instance.email
        resp_dict['message'] = instance.message
        resp_dict['created_at'] = instance.created_at
        resp_dict['updated_at'] = instance.updated_at
        return resp_dict
        