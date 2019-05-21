from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.generic import View, ListView, CreateView, DetailView, UpdateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import UserUpdateForm, UserCreateForm
from django.urls import reverse_lazy
from django.views import generic
from django.db.models import Q
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin


# Create your views here.


class Index(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        return render(request, 'base.html')


class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('UserList')
    template_name = 'signup.html'


class UserList(LoginRequiredMixin, ListView):
    """
         系统用户列表
    """
    model = User
    template_name = 'users/userList.html'  # Default: <app_label>/<model_name>_list.html
    context_object_name = 'users'  # Default: object_list
    paginate_by = 12
    queryset = User.objects.all()  # Default: Model.objects.all()
    ordering = ['-id']

    def get_queryset(self, *args, **kwargs):
        """
            添加查询功能
        """
        context = super().get_queryset()
        keyword = self.request.GET.get('Searche', '')
        if keyword:
            context = User.objects.filter(Q(username__icontains=keyword) | Q(first_name__icontains=keyword))
        return context

    #     def get_context_data(self, **kwargs):
    #         context = {
    #             "name_active": "active",
    #             "name_list_active": "active",
    #         }
    #         kwargs.update(context)
    #         return super().get_context_data(**kwargs)


class UserCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    """
    CREATE USER
    """
    model = User
    template_name = 'users/UserCreate.html'
    form_class = UserCreateForm
    success_url = reverse_lazy('UserList')
    success_message = '用户创建成功'

    def form_valid(self, form):
        user = form.save(commit=False)
        if user.password and user.username != "admin":
            user.set_password(user.password)
        return super().form_valid(form)


class UserUpdate(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """
    User detail Update
    """
    model = User
    template_name = 'users/UserUpdate.html'
    # fields = ('first_name', 'last_name', 'email')
    context_object_name = 'UserUpdate'
    form_class = UserUpdateForm
    # success_message = '用户创建成功'

    def form_valid(self, form):
        user = form.save(commit=False)
        if user.password or user.username != "admin":
            user.set_password(user.password)
        else:
            messages.error(self.request, 'Admin用户禁止更新')
            return redirect(reverse_lazy('UserList'))
        user.save(update_fields=list(form.cleaned_data.keys()))
        messages.success(self.request, '用户信息更新成功')
        return redirect(reverse_lazy('UserList'))


class UserDetail(LoginRequiredMixin, DetailView):
    """
    用户详情&用户信息更新
    """
    model = User
    template_name = 'users/UserDetail.html'
    context_object_name = 'UserDetail'


@login_required
def UsersDeL(request):
    """
    单用户删除,批量删除
    :param request:
    :return: /UserList url ADN MESSAGES
    """
    if request.method == "GET":
        user_ids = request.GET.get('id', '')
        user_id_list = user_ids.split(',')
    elif request.method == "POST":
        user_ids = request.POST.get('id', '')
        user_id_list = user_ids.split(',')
        messages.success(request, '批量删除成功')
        return HttpResponseRedirect(reverse('UserList'))
    else:
        messages.error(request, '请求出错')
        return HttpResponseRedirect(reverse('UserList'))

    for user_id in user_id_list:
        user = User.objects.get(id=user_id)
        if user and user.username != 'admin':
            user.delete()
            messages.success(request, '删除成功')
        else:
            messages.error(request, 'admin用户无法删除')
    return HttpResponseRedirect(reverse('UserList'))


@login_required
def UserLocks(request):
    """
    禁用用户状态
    :param request:
    :return:
    """
    if request.method == 'GET':
        user_id = request.GET.get('id')
    user = User.objects.filter(id=user_id)
    if user and user.values_list('username', flat=True)[0] != 'admin':
        if not user.values_list('is_active', flat=True)[0]:
            user.update(is_active=True)
            messages.success(request, '解封成功')
        else:
            user.update(is_active=False)
        messages.success(request, '封停成功')
    else:
        messages.error(request, 'Admin用户无法禁用')
    return HttpResponseRedirect(reverse('UserList'))
