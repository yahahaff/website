from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.generic import View, ListView, CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import *
from .models import Assets
from django.urls import reverse_lazy
from django.db.models import Q
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin


# Create your views here.
class AssetsList(LoginRequiredMixin, ListView):
    """
         系统用户列表
    """
    model = Assets
    template_name = 'assets/AssetsList.html'  # Default: <app_label>/<model_name>_list.html
    context_object_name = 'assets'  # Default: object_list
    paginate_by = 12
    queryset = Assets.objects.all()  # Default: Model.objects.all()
    ordering = ['-id']

    def get_queryset(self, *args, **kwargs):
        """
            添加查询功能
        """
        context = super().get_queryset()
        keyword = self.request.GET.get('Searche', '')
        if keyword:
            #context = Assets.objects.filter(Q(ip__icontains=keyword) | Q(location__icontains=keyword))
            context = Assets.objects.filter(ip=keyword)
        return context


class AssetCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    """
    CREATE Hosts
    """
    model = Assets
    template_name = 'assets/AssetCreate.html'
    form_class = AssetCreateForm
    success_url = reverse_lazy('AssetsList')
    success_message = '主机创建成功'

    # def form_valid(self, form):
    #     try:
    #         super(AssetCreate).form_valid()
    #         form.save()
    #     except Exception as err:
    #         print(err)
    # def form_invalid(self, form):
    #     try:
    #         super(AssetCreate).form_invalid()
    #     except Exception as err:
    #         print(err)
    #     return reverse_lazy('AssetsList')

class AssetUpdate(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """
    User detail Update
    """
    model = Assets
    template_name = 'assets/AssetUpdate.html'
    #fields = ('first_name', 'last_name', 'email')
    context_object_name = 'AssetUpdate'
    form_class = AssetUpdateForm
    success_message = '主机信息更新成功'
    success_url = reverse_lazy('AssetsList')


@login_required
def AssetDel(request):
    """
    单主机删除,批量主机删除
    :param request:
    :return: /AssetsList url ADN MESSAGES
    """
    if request.method == "GET":
        asset_ids = request.GET.get('id', '')
        asset_id_list = asset_ids.split(',')
    elif request.method == "POST":
        asset_ids = request.POST.get('id', '')
        asset_id_list = asset_ids.split(',')
        messages.success(request, '批量删除成功')
        return HttpResponseRedirect(reverse('AssetsList'))
    else:
        messages.error(request, '请求出错')
        return HttpResponseRedirect(reverse('AssetsList'))

    for asset_id in asset_id_list:
        AssetsObj = Assets.objects.get(id=asset_id)
        AssetsObj.delete()
        messages.success(request, '删除成功')
    return HttpResponseRedirect(reverse('AssetsList'))


