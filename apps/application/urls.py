from django.urls import path, re_path
from .views import *



urlpatterns = [
     path('Application/List/<str:pt>/', ApplicationList.as_view(), name='ApplicationList'),
     path('Application/Create/', ApplicationCreate.as_view(), name='ApplicationCreate'),
     path('Application/Update/<pk>/', ApplicationUpdate.as_view(), name='ApplicationUpdate'),
     # path('DomainDel/<pk>/', DomainDel, name='DomainDel'),
     # path('Domain/<pk>/', Get_domainInfo, name='get_domain'),


]
