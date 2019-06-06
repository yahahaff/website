
# Create your views here.
import os
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.generic import View, ListView, CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Application
from assets.models import Platform
from django.shortcuts import get_object_or_404
from .forms import *
from django.shortcuts import render
from django.urls import reverse_lazy
from django.db.models import Q
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from .restart import SSHRrmote
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

class ApplicationGo(LoginRequiredMixin,SuccessMessageMixin,View):
    """

    """

    def get(self, request, *args, **kwargs):
        return render(request, 'application/xterm.html')

@login_required
def ApplicationStop(request, pk):
    if request.method == "GET":

        obj = Application.objects.get(pk=pk)
        pt = Platform.objects.get(pk=obj.platform_id)
        ssh = SSHRrmote(str(obj.ipaddress))
        grestr = os.path.dirname(obj.dst_path)
        proResult = ssh.Run_Cmmond("ps -ef|grep '{}/conf'|grep -v grep|grep -v tail".format(grestr))
        logger.info(proResult)
        killcmd = "ps -ef|grep '{}/conf'|grep -v grep|grep -v tail".format(grestr) + "|awk '{print $2}'|xargs kill -9"
        #killcmd = "ps -ef|grep '{}/conf'|grep -v grep|grep -v tail".format(grestr) + "|awk '{print $2}'"
        result = ssh.Run_Cmmond(killcmd)
        if result[1]:
            logger.error("应用进程不存在，{}".format(result[1]))
            messages.error(request, '应用进程不存在，{}'.format(result[1]))
            return HttpResponseRedirect(reverse('ApplicationList', kwargs={'pt': pt.platform_code}))
        ssh.client.close()
        obj.status = False
        obj.save()
        messages.success(request, '应用停止成功')
    return HttpResponseRedirect(reverse('ApplicationList', kwargs={'pt': pt.platform_code}))


@login_required
def ApplicationStart(request, pk):

    if request.method == "GET":
        obj = Application.objects.get(pk=pk)
        pt = Platform.objects.get(pk=obj.platform_id)
        ssh = SSHRrmote(str(obj.ipaddress))
        startUp = os.path.dirname(obj.dst_path)
        grestr = os.path.dirname(obj.dst_path)
        wcl = ssh.Run_Cmmond("ps -ef|grep '{}/conf'|grep -v grep|grep -v tail|wc -l".format(grestr))
        number = wcl[0].split('\n')[0]
        if wcl[0] and int(number) >= 1:
            messages.error(request, '应用已经启动，请勿重复启动')
            return HttpResponseRedirect(reverse('ApplicationList', kwargs={'pt': pt.platform_code}))
        result = ssh.Run_Cmmond("{}/bin/startup.sh".format(startUp))
        print(result)
        if result[1]:
            logger.error("应用启动失败，{}".format(result[1]))
            messages.error(request, '应用启动失败，{}'.format(result[1]))
            return HttpResponseRedirect(reverse('ApplicationList', kwargs={'pt': pt.platform_code}))
        logger.info("{}/bin/startup.sh 执行完毕".format(startUp))
        ssh.client.close()
        messages.success(request, '应用启动成功')
        obj.status = True
        obj.save()
    return HttpResponseRedirect(reverse('ApplicationList', kwargs={'pt': pt.platform_code}))


