from django.http import HttpResponse
from django.conf import settings
import traceback
from rest_framework.renderers import JSONRenderer
from utility.response import ApiResponse


class ErrorHandlerMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def message_format(self, message):
        return message

    def process_exception(self, request, exception):
        if not settings.DEBUG:
            if exception:
                # Format your message here
                try:
                    message = [str(exception.args[0])]
                except:
                    message = ''

            response = ApiResponse.response_internal_server_error(self, message=message, code=500)
            response.accepted_renderer = JSONRenderer()
            response.accepted_media_type = "application/json"
            response.renderer_context = {}
            response.render()
            return response

import json
class TrimMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_view(self, request, view_fun, view_args, view_kwargs):

        if request.method == "POST":
            try:
                request_body = json.loads(request.body)
            except:
                request_body = {}

            try:
                for key in request_body:
                    try:
                        request_body[key] = request_body[key].strip()
                    except:
                        request_body[key] = request_body[key]
            except:
                pass

            if request_body:
                request._body = bytes(json.dumps(request_body), "utf-8")
