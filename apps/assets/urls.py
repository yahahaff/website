from django.urls import path, re_path
from .views import *



urlpatterns = [
    path('AssetsList/', AssetsList.as_view(), name='AssetsList'),
    path('AssetCreate/', AssetCreate.as_view(), name='AssetCreate'),
    path('AssetUpdate/<pk>/', AssetUpdate.as_view(), name='AssetUpdate'),
    path('AssetDel/', AssetDel, name='AssetDel'),



]
