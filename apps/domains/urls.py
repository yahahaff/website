
from django.urls import path, re_path
from .views import *



urlpatterns = [
    path('DomainList/', DomainList.as_view(), name='DomainList'),
    path('Domainssl/', Domainssl.as_view(), name='Domainssl'),
    path('DomainCreate/', DomainCreate.as_view(), name='DomainCreate'),
    path('DomainUpdate/<pk>/', DomainUpdate.as_view(), name='DomainUpdate'),
    path('DomainDel/<pk>/', DomainDel, name='DomainDel'),
    path('Domain/<pk>/', Get_domainInfo, name='get_domain'),



]
