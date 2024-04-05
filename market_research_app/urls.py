from django.urls import re_path,path
from django.conf.urls import include 
from django.conf import settings

from market_research_app.views.change_password import ChangePasswordView
from market_research_app.views.file_upload import FileUploadView
from .views.login import LoginViewSet
from .views.forget_password import ForgotPasswordView
from .views.verify_otp import VerifyPasswordView
from .views.reset_password import ResetPasswordView
from .views.logout import LogoutView
from .views.user_impersonate import ImpersonateView
from .views.login_verify_otp import LoginVerifyView

""" User login/ add/ logout profile urls"""
urlpatterns = [
    re_path(r'^login/$', LoginViewSet.as_view()),
    re_path(r'^logout/$', LogoutView.as_view()),
]

""" User forget_password/ verify_otp/ reset_password/ profile urls"""
urlpatterns += [
    re_path(r'^forget-password/$', ForgotPasswordView.as_view()),
    re_path(r'^verify-otp/$', VerifyPasswordView.as_view()),
    re_path(r"^change-password/$", ChangePasswordView.as_view({"post": "change_password"})),
    re_path(r'^reset-password/$', ResetPasswordView.as_view()),
]

""" User impersonate"""
urlpatterns += [
    re_path(r'^user-impersonate/(?P<id>.+)/$', ImpersonateView.as_view({'get': 'retrieve'})),
]

""" login-verify-otp"""
urlpatterns += [
    re_path(r'^login-verify-otp/$', LoginVerifyView.as_view({'get': 'retrieve'})),
]

        

# from .views.student import StudentView

# ''' Student '''
# urlpatterns += [
#     re_path(r'^student/$', StudentView.as_view({'get': 'list', 'post': 'create', 'delete': 'bulk_delete'})),
#     re_path(r'^student/(?P<id>.+)/$', StudentView.as_view({'get': 'retrieve', 'delete': 'delete', 'put': 'partial_update'})),
# ]


from .views.reports import ReportsView

''' Reports '''
urlpatterns += [
    re_path(r'^reports/$', ReportsView.as_view({'get': 'list', 'post': 'create', 'delete': 'bulk_delete'})),
    re_path(r'^reports/(?P<id>.+)/$', ReportsView.as_view({'get': 'retrieve' , 'put': 'partial_update', 'delete': 'delete'})),
]

from .views.report_list import ReportsListView
''' Reports '''
urlpatterns += [
    re_path(r'^reports-list/$', ReportsListView.as_view({'get': 'list'})),
    re_path(r'^reports-list/(?P<id>.+)/$', ReportsListView.as_view({'get': 'retrieve'})),
]
from .views.countries import CountryView

""" Countries"""
urlpatterns += [
    re_path(r'^countries/$', CountryView.as_view({'get': 'list', 'post': 'create', 'delete': 'bulk_delete'})),
    re_path(r'^countries/(?P<id>.+)/$', CountryView.as_view({'get': 'retrieve' , 'put': 'partial_update', 'delete': 'delete'})),
]


""" FileUpload """
urlpatterns += [
    re_path(r"^upload/$", FileUploadView.as_view({"post": "post"})),
    re_path(r"^upload/(?P<id>.+)/$",FileUploadView.as_view({"delete": "delete"})),
]

from .views.contactdetails import ContactdetailsView
''' Reports '''
urlpatterns += [
    re_path(r'^contact-details/$', ContactdetailsView.as_view({'get': 'list', 'post': 'create', 'delete': 'bulk_delete'})),
    re_path(r'^contact-details/(?P<id>.+)/$', ContactdetailsView.as_view({'get': 'retrieve' , 'put': 'partial_update', 'delete': 'delete'})),
]