from django.db import models
from .base import Base


class Countries(Base):
    ''' Model Fields '''

    # Fields
    name = models.CharField(max_length=255, null=True, blank=True, db_index=True)
    # phone_code = models.CharField(max_length=255, null=True, blank=True, db_index=True)

    STATUS_CHOICES = ((1, 'Active'),(2, 'Inactive'),(3,'Deleted'))
    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES, default=1)

    class Meta:
        db_table = "countries"

    def __str__(self):
        return self.name

    @property
    def get_name(self):
        return self.name.capitalize()

    @staticmethod
    def to_dict(instance):
        resp_dict = {}
        resp_dict['id'] = instance.id
        resp_dict['name'] = instance.name
        # resp_dict['phone_code'] = instance.phone_code
        resp_dict['status'] = instance.status
        resp_dict['status_name'] = instance.get_status_display()
        resp_dict['created_at'] = instance.created_at
        resp_dict['updated_at'] = instance.updated_at
        return resp_dict
