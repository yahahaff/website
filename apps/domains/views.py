
# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.generic import View, ListView, CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import  Domains
from assets.models import Assets
from .forms import *
from django.urls import reverse_lazy
from datetime import datetime
from django.db.models import Q
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from .dns_tools import get_dns_resolver, get_ssl
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job
from .dns_tools import task
import logging
logger = logging.getLogger('django')


# Create your views here.
class DomainList(LoginRequiredMixin, ListView):
    """
         全部域名列表
    """
    model = Domains
    template_name = 'domains/DomainsList.html'  # Default: <app_label>/<model_name>_list.html
    context_object_name = 'domains'  # Default: object_list
    paginate_by = 1
    queryset = Domains.objects.all()  # Default: Model.objects.all()
    ordering = ['-update_time']

    def get_queryset(self, *args, **kwargs):
        """
            添加查询功能
        """
        context = super().get_queryset()
        keyword = self.request.GET.get('Searche', '')
        if keyword:
            #context = Domains.objects.filter(domain__icontains=keyword)
            context = Domains.objects.filter(
                Q(domain__icontains=keyword) | Q(resolve__platform_name__contains=keyword))
        return context

class Domainssl(LoginRequiredMixin, ListView):
    """
         SSL域名列表
    """
    model = Domains
    template_name = 'domains/Domainssl.html'  # Default: <app_label>/<model_name>_list.html
    context_object_name = 'domains'  # Default: object_list
    paginate_by = 12
    queryset = Domains.objects.filter(is_encryption=True)  # Default: Model.objects.all()
    ordering = ['remainder_days']

    def get_queryset(self, *args, **kwargs):
        """
            添加查询功能
        """
        context = super().get_queryset()
        keyword = self.request.GET.get('Searche', '')
        if keyword:
            #context = Domains.objects.filter(domain__icontains=keyword)
            context = Domains.objects.filter(
                Q(domain__icontains=keyword) | Q(resolve__platform_name__contains=keyword))

        return context



class DomainCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    """
    CREATE Hosts
    """
    model = Domains
    template_name = 'domains/DomainCreate.html'
    # template_name = 'domains/111.html'
    form_class = DomainCreateForm
    success_url = reverse_lazy('DomainList')
    success_message = '域名创建成功'


class DomainUpdate(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """
    User detail Update
    """
    model = Domains
    template_name = 'domains/DomainUpdate.html'
    #fields = ('first_name', 'last_name', 'email')
    context_object_name = 'DomainUpdate'
    form_class = DomainUpdateForm
    success_message = '域名信息更新成功'
    success_url = reverse_lazy('DomainList')


@login_required
def DomainDel(request, pk):
    """
    单域名删除,批量域名删除
    :param request:
    :return: /DomainList url ADN MESSAGES
    """
    try:
        AssetsObj = Domains.objects.get(pk=pk)
        AssetsObj.delete()
        messages.success(request, '删除成功')
    except Exception as err:
        logger.error(err)
        messages.error(request, '删除失败')
    return HttpResponseRedirect(reverse('DomainList'))


@login_required
def Get_domainInfo(request, pk):
    """
    单域名更新 Domain信息
    :param request:
    :param pk:
    :return: massage
    """
    try:
        Domains_obj = Domains.objects.get(pk=pk)
        result_nds = get_dns_resolver(Domains_obj.domain)
        if 'A' in result_nds.keys():
            ass_ip = Assets.objects.get(ip=result_nds['A'])
            if ass_ip.pk:
                obj_info = Domains.objects.get(domain=result_nds['domain'])
                obj_info.resolve = ass_ip
                obj_info.save()
                logger.info('*****单域名更新*******域名{} A 数据库操作完成'.format(Domains_obj.domain))
            else:
                obj_info = Domains.objects.get(domain=result_nds['domain'])
                obj_info.resolve = None
                obj_info.save()
                logger.info('*****单域名更新*******域名{} CNAME 数据库操作完成'.format(Domains_obj.domain))
    except Exception as err:
        logger.error('*****单域名更新*******获取域名%s DNS解析失败'.format(Domains_obj.domain), err)

    #获取SSL证书信息
    try:
            result_ssl = get_ssl(Domains_obj.domain)
            if result_ssl:
                obj = Domains.objects.get(domain=Domains_obj.domain)
                ssl_Vendor = result_ssl['Issuer']
                begin_obj = datetime.strptime(result_ssl['ssl_begin'], '%b %d %H:%M:%S %Y %Z')
                expire_obj = datetime.strptime(result_ssl['ssl_expire'], '%b %d %H:%M:%S %Y %Z')
                remeainder_days = (expire_obj.date() - datetime.today().date()).days
                obj.ssl_begin = begin_obj.date()
                obj.ssl_expire = expire_obj.date()
                obj.remainder_days = remeainder_days
                obj.is_active = True
                obj.ssl_issuer = ssl_Vendor
                obj.save()
                logger.info('*****单域名更新*******域名{}数据库操作完成'.format(Domains_obj.domain))
                messages.success(request, '{}更新成功'.format(Domains_obj.domain))
            else:
                logger.error('******单域名更新*******get_ssl函数执行失败 域名{}'.format(Domains_obj.domain))
                messages.error(request, '{}更新失败'.format(Domains_obj.domain))
    except Exception as err:
        logger.error(err)
        messages.error(request, '{}更新失败'.format(Domains_obj.domain))
    return HttpResponseRedirect(reverse('Domainssl'))


#开启定时工作
try:
    # 实例化调度器
    scheduler = BackgroundScheduler()
    # 调度器使用DjangoJobStore()
    scheduler.add_jobstore(DjangoJobStore(),  "default",)
    # 设置定时任务，选择方式为interval，时间间隔为60s
    # @register_job(scheduler, "interval", seconds=6000)
    # 另一种方式为每周周一到周五固定时间执行任务，对应代码为：
    #@register_job(scheduler, 'cron', day_of_week='mon-fri', hour='9', minute='30', second='10', id='task_time')

    @register_job(scheduler, 'cron', day_of_week='mon-fri', hour=11, minute=18, second=0, id='task_time')
    def my_job():
        logger.info('进入task任务')
        task()
    register_events(scheduler)
    scheduler.start()
except Exception as e:
    logger.error(e)
    # 有错误就停止定时器
    scheduler.shutdown()
