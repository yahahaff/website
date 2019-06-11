
# Create your views here.
import os
from datetime import datetime
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.generic import View, ListView, CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Application, App_history
from assets.models import Platform
from django.shortcuts import get_object_or_404
from .forms import *
from django.shortcuts import render
from django.urls import reverse_lazy
from django.db.models import Q
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from .sshclient import SSHRrmote, SSHConnectException
from django_redis import get_redis_connection
import logging

logger = logging.getLogger('django')
redis_for_app_cli = get_redis_connection("default")

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
        #context = super().get_queryset()
        #通过 kwargs.get方法获取外部url中所定义的参数名成的参数值
        pt = self.kwargs.get('pt')
        keyword = self.request.GET.get('Searche', '')   #获取查询关键字
        if pt == 'All' or not keyword:
            context = Application.objects.all()
        else:
            context = Application.objects.filter(platform__platform_code=pt, items=keyword)
        # if keyword:
        #     context = Application.objects.filter(Q(items__icontains=keyword) | Q(platform__icontains=keyword))
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

class ApplicationGo(LoginRequiredMixin,SuccessMessageMixin,DetailView):
    model = Application
    template_name = 'application/ApplicationGOdetail.html'
    context_object_name = 'applicationGO'
    queryset = Application.objects.all()
    ordering = ['-update_time']


class HistoryList(LoginRequiredMixin, ListView):
    """
         发布历史列表
    """
    model = App_history
    template_name = 'application/ApplicationHistoryList.html'
    context_object_name = 'apphistory'
    paginate_by = 12
    queryset = App_history.objects.all()
    ordering = ['-update_time']

    def get_queryset(self, *args, **kwargs):
        """
            添加查询功能
        """
        context = super().get_queryset()
        keyword = self.request.GET.get('Searche', '')
        if keyword:
            context = App_history.objects.filter(Q(items__icontains=keyword) | Q(platform__icontains=keyword))
        return context


@login_required
def ApplicationStop(request, pk):
    if request.method == "GET":
        obj = Application.objects.get(pk=pk)
        pt = Platform.objects.get(pk=obj.platform_id)
        try:
            ssh = SSHRrmote(str(obj.ipaddress))
        except Exception as e:
            messages.error(request, '服务器连接失败, {}'.format(e))
            return HttpResponseRedirect(reverse('ApplicationList', kwargs={'pt': pt.platform_code}))
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
        try:
            ssh = SSHRrmote(str(obj.ipaddress))
        except Exception as e:
            messages.error(request, '服务器连接失败, {}'.format(e))
            return HttpResponseRedirect(reverse('ApplicationList', kwargs={'pt': pt.platform_code}))
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


@login_required
def ApplicationStaticGo(request, pk):
    #getUrl = '0.46.5.246'
    getUrl = 'ftp://10.46.5.246'  #FTP使用
    if request.method == "GET":
        obj = Application.objects.get(pk=pk)
        pt = Platform.objects.get(pk=obj.platform_id)
        dowload = '/tmp/{user}/'.format(user=request.user)
        dowload_name = obj.package_name
        date = datetime.now().strftime('%Y%m%d_%H%M%S')
        new_name = obj.package_name.split('.')[0]+"_{user}_{date}.zip".format(user=request.user, date=date)
        historyinfo = {'items': obj.items, 'platform': obj.platform, 'env': obj.env, 'type': obj.type,
                       'app_dir': obj.dst_path, 'ip': obj.ipaddress, 'opsuser':request.user}
        try:
            ssh = SSHRrmote(str(obj.ipaddress))
        except SSHConnectException as e:
            messages.error(request, '服务器连接失败, {}'.format(e))
            return HttpResponseRedirect(reverse('ApplicationList', kwargs={'pt': pt.platform_code}))
        ssh.Run_Cmmond("test {dowload}|mkdir -p {dowload}".format(dowload=dowload))
        #wget --ftp-user=USERNAME --ftp-password=PASSWORD url  使用FTP
        wget_result = ssh.Run_Cmmond(
            'wget -O {dowload}/{newname} {url}/{user}/{dowload_name} --ftp-user={ftpuser} --ftp-password={ftppassword}'.format(
                dowload=dowload, newname=new_name, dowload_name=dowload_name, url=getUrl, user=request.user,ftpuser='sys_pub', ftppassword='sys_pub123'))
        # 下载文件
        # wget_result = ssh.Run_Cmmond(
        #     "wget -O {dowload}/{newname} {url}/{user}/{dowload_name} ".format(dowload=dowload, newname=new_name,
        #                                                     dowload_name=dowload_name, url=getUrl, user=request.user))
        if wget_result[0] != 0:
            messages.error(request, '静态发布失败，{}'.format(wget_result[2]))
            ssh.client.close()
            return HttpResponseRedirect(reverse('ApplicationList', kwargs={'pt': pt.platform_code}))
        #备份文件
        bak_result = ssh.Run_Cmmond(
            "cp -r {dst_path} {backup}/{name}_{date}".format(dst_path=obj.dst_path, backup=obj.backup_path,
                                                           name=obj.dst_path.split('/')[-1], date=date))
        if bak_result[0] != 0:
            ssh.client.close()
            messages.error(request, '静态发布失败，{}'.format(bak_result[2]))
            return HttpResponseRedirect(reverse('ApplicationList', kwargs={'pt': pt.platform_code}))
        #解压覆盖文件
        unzip_result = ssh.Run_Cmmond(
            "unzip -o {path}/{filename} -d {dst_path}".format(path=dowload, filename=new_name,
                                                                               dst_path=obj.dst_path))
        if unzip_result[0] != 0:
            ssh.client.close()
            messages.error(request, '静态发布失败，{}'.format(unzip_result[2]))
            return HttpResponseRedirect(reverse('ApplicationList', kwargs={'pt': pt.platform_code}))
        messages.success(request, '静态发布成功')

        historyinfo['status'] = True
        historyinfo['backup'] = "{backup}/{name}_{date}".format(backup=obj.backup_path,
                                                                name=obj.dst_path.split('/')[-1], date=date)
        try:
            updateHistory(historyinfo)
        except Exception as e:
            messages.WARNING(request, '发布成功，数据库写入失败：{}'.format(e))
            return HttpResponseRedirect(reverse('ApplicationList', kwargs={'pt': pt.platform_code}))
        ssh.client.close()
    return HttpResponseRedirect(reverse('HistoryList'))



def updateHistory(info):
    obj = App_history()
    obj.items = info['items']
    obj.type = info['type']
    obj.platform = info['platform']
    obj.status = info['status']
    obj.ipaddress = info['ip']
    obj.app_dir = info['app_dir']
    obj.backup = info['backup']
    obj.env = info['env']
    obj.opsuser = info['opsuser']
    obj.save()

@login_required
def rollback(request, pk):
    if request.method == "GET":
        obj = App_history.objects.get(pk=pk)
    try:
        ssh = SSHRrmote(str(obj.ipaddress))
    except SSHConnectException as e:
        messages.error(request, '服务器连接失败, {}'.format(e))
        return HttpResponseRedirect(reverse('HistoryList'))
    result = ssh.Run_Cmmond(
        "rm -rf {app_path} && cp -r {back_path} {app_path}".format(app_path=obj.app_dir, back_path=obj.backup))
    if result[0] != 0:
        ssh.client.close()
        messages.error(request, '静态回滚失败，{}'.format(result[1]))
        return HttpResponseRedirect(reverse('HistoryList'))
    messages.success(request, '静态:{}回滚成功'.format(obj.backup))
    ssh.client.close()
    return HttpResponseRedirect(reverse('HistoryList'))