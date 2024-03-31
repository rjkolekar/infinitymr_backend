# from django.core.files.base import UploadedFile
from django.core.files.uploadedfile import UploadedFile

from rest_framework.response import Response
# from contract_portal.throttles import LightRateThrottle
from utility.constants import BYTES_PER_MB
from oauth2_provider.contrib.rest_framework import OAuth2Authentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from rest_framework import status
from utility.utils import *
from utility.response import ApiResponse

"""Serializers"""
from ..serializers.asstes_serializer import AssetsSerializer

"""Models"""
from ..models import Assets

class FileUploadView(MultipleFieldPKModelMixin, CreateRetrieveUpdateViewSet, ApiResponse , viewsets.ViewSet):
    serializer_class = AssetsSerializer
    authentication_classes = [OAuth2Authentication, ]
    permission_classes = [IsAuthenticated]
    # throttle_classes = [LightRateThrottle]

    singular_name = "File"
    model_class = Assets.objects

 
    def get_object(self, pk, instance=None):
        try:
            if instance:
                return self.model_class.get(pk=pk, employer_id=instance.id)
            else:
                return self.model_class.get(pk=pk)
        except:
            return None

    # def post(self, request):
    #     # Your post method logic here
    #     return Response({"message": "File uploaded successfully"})    

    def post(self, request, *args, **kwargs):
        file_type, file_size, file_name = None, None, None

        data = request.data
        file_meta = data.get("file_name")
    # Retrieve the file metadata
        if file_meta:
            if isinstance(file_meta, UploadedFile):  # Check if file_meta is an UploadedFile object
                file_meta = file_meta.__dict__  # Access the attributes using __dict__

                response = super(FileUploadView, self).create(request, *args, **kwargs)

                file_size = file_meta.get("size")
                file_type = file_meta.get("content_type")
                file_name = file_meta.get("_name")

                if file_instance := self.model_class.filter(id=response.data.get("id")).first():
                    file_instance.file_type = file_type
                    file_instance.file_size = convert_filesize_bits_to_mega_bytes(file_size)
                    file_instance.actual_file_name = file_name
                    file_instance.save()

                    response.data['file_name'] = str(file_instance.file_name)
                    response.data['file_type'] = file_instance.file_type
                    response.data['file_size'] = file_instance.file_size
                    response.data['actual_file_name'] = file_instance.actual_file_name

                    return ApiResponse.response_ok(self, data=response.data, message=f"{self.singular_name} uploaded.")
                else:
                    return ApiResponse.response_bad_request(self, message=f"{self.singular_name} metadata is invalid.")  # Handle invalid file metadata
            else:
                return ApiResponse.response_bad_request(self, message=f"{self.singular_name} metadata is invalid.")  # Handle invalid file metadata
        else:
            return ApiResponse.response_bad_request(self, message=f"{self.singular_name} metadata not found.")  # Handle missing file metadata
            
        
    def delete(self, request, employer_instance, *args, **kwargs):
        """
        :To delete the single record.
        """
        get_id = self.kwargs.get("id")

        """ get instance """
        instance = self.get_object(get_id, employer_instance)

        if not instance:
            return ApiResponse.response_not_found(self, message=f"{self.singular_name} not found.")

        instance.file_name.delete(save=False)
        instance.delete()

        """ return success """
        return ApiResponse.response_ok(self, message=f"{self.singular_name} deleted.")

def convert_filesize_bits_to_mega_bytes(bits):
    return round(bits / BYTES_PER_MB, 4)
