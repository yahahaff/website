from django.urls import path, re_path
from django.contrib.auth import views as auth
from .views import *



urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('login/', auth.LoginView.as_view(template_name='login/login.html'), name='login'),
    path('logout/', auth.LogoutView.as_view(next_page='/'), name='logout'),
    path('UserList/', UserList.as_view(), name='UserList'),
    path('UserList/add/', UsersDeL, name='UserAdd'),
    path('UserList/del/', UsersDeL, name='UserDel'),
    path('UserList/edit/', UsersDeL, name='UserEdit'),
    path('UserList/lock/', UserLocks, name='UserLocks'),
    path('UserList/create/', UserCreate.as_view(), name='UserCreate'),
    path('UserList/detail/<pk>/', UserDetail.as_view(), name='UserDetail'),
    path('UserList/update/<pk>/', UserUpdate.as_view(), name='UserUpdate'),
    path('signup/', SignUp.as_view(), name='signup'),
]




