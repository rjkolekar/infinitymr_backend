
from .views.contactdetails import ContactdetailsView

''' Contactdetails '''
urlpatterns += [
    re_path(r'^contactdetails/$', ContactdetailsView.as_view({'get': 'list', 'post': 'create', 'delete': 'bulk_delete'})),
    re_path(r'^contactdetails/(?P<id>.+)/$', ContactdetailsView.as_view({'get': 'retrieve' , 'put': 'partial_update', 'delete': 'delete'})),
]
        