
# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.generic import View, ListView, CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Application
from django.shortcuts import get_object_or_404
from .forms import *
from django.urls import reverse_lazy
from django.db.models import Q
from django.contrib.messages.views import SuccessMessageMixin
import logging
logger = logging.getLogger('django')


# Create your views here.
class ApplicationList(LoginRequiredMixin, ListView):
    """
         项目列表
    """
    model = Application
    template_name = 'application/ApplicationList.html'  # Default: <app_label>/<model_name>_list.html
    context_object_name = 'applications'  # Default: object_list
    paginate_by = 12
    queryset = Application.objects.all()  # Default: Model.objects.all()
    ordering = ['-update_time']



    def get_queryset(self,*args, **kwargs):

        #通过 kwargs.get方法获取外部url中所定义的参数名成的参数值

        pt = self.kwargs.get('pt')
        if pt == 'All':
            context = Application.objects.all()
        else:
            context = Application.objects.filter(platform__platform_code=pt)
        return context


class ApplicationCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    """
    CREATE Hosts
    """
    model = Application
    template_name = 'application/ApplicationCreate.html'
    form_class = ApplicationCreateForm
    success_message = '应用创建成功'

    def get_success_url(self):
        if 'pt' in self.kwargs:
            pt = self.kwargs['pt']
        else:
            pt = 'All'
        return reverse('ApplicationList', kwargs={'pt': pt})


class ApplicationUpdate(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """
    User detail Update
    """
    model = Application
    template_name = 'application/ApplicationUpdate.html'
    #fields = ('first_name', 'last_name', 'email')
    context_object_name = 'ApplicationUpdate'
    form_class = ApplicationUpdateForm
    success_message = '应用更新成功'

    def get_success_url(self):
        if 'pt' in self.kwargs:
            pt = self.kwargs['pt']
        else:
            pt = 'All'
        return reverse('ApplicationList', kwargs={'pt': pt})



