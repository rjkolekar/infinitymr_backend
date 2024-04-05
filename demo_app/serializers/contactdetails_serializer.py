
from rest_framework import serializers
from ..models import Contactdetails

class ContactdetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contactdetails
        fields = ['name', 'company_name', 'job_title', 'mobile', 'email', 'message']
        