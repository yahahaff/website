from django.urls import path, re_path
from .views import *



urlpatterns = [
     path('Application/List/<str:pt>/', ApplicationList.as_view(), name='ApplicationList'),
     path('Application/Create/', ApplicationCreate.as_view(), name='ApplicationCreate'),
     path('Application/Update/<pk>/', ApplicationUpdate.as_view(), name='ApplicationUpdate'),
     path('Application/stop/<pk>/', ApplicationStop, name='ApplicationStop'),
     path('Application/start/<pk>/', ApplicationStart, name='ApplicationStart'),
     path('Application/GO/<pk>/', ApplicationGo.as_view(), name='ApplicationGo')


]
