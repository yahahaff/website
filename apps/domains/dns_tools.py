import os
import dns.resolver
import socket
import ssl
from datetime import datetime
from .models import Domains
from assets.models import Assets
from apscheduler.schedulers.background import BackgroundScheduler

import logging
logger = logging.getLogger('django')

def get_dns_resolver(domain):
    """
    解析域名DNS 记录  有多条A  CNAME 记录的将只返回记录最后一条记录
    :param domain:
    :return: {'domain': 'networks.mc188.com', 'A': '119.9.104.207'}
    """
    logger.info('进入函数')
    res = dns.resolver.Resolver()
    query_result = res.query(domain)
    ruest = {}
    nn = 0             #为防止CNAME中的A记录进入ruest
    try:
        for i in query_result.response.answer:
            ruest['domain'] = domain
            for j in i:
                if j.rdtype == 1 and nn == 0:
                    ruest['A'] = j.address
                    nn = nn+1
                if j.rdtype == 5:
                    ruest['CNAME'] = str(j.target).strip('.')
                    nn = nn + 1
        return ruest
    except dns.resolver.Timeout:
        # print('{0} query DNS time out'.format(domain))
        return ruest
    except Exception as err:
        print('获取域名DNS失败', err)
        return ruest


def get_ssl(domain):
    """
    :param domain:
    :return: {'Issuer': "Let's Encrypt", 'notBefore': 'Apr  9 05:47:26 2019 GMT', 'notAfter': 'Jul  8 05:47:26 2019 GMT'}

    """
    try:
        logger.info('开始获取域名： {}证书信息'.format(domain))
        ctx = ssl.create_default_context()
        s = ctx.wrap_socket(socket.socket(), server_hostname=domain)
        s.settimeout(3)
        s.connect((domain, 443))
        cert = s.getpeercert()
        result = {'Issuer': cert['issuer'][1][0][1], 'ssl_begin': cert['notBefore'],
                  'ssl_expire': cert['notAfter']}
        logger.info(result)
    except Exception as err:
        logger.error('获取域名:{}证书信息出错'.format(domain), err)
        obj = Domains.objects.get(domain=domain)
        obj.is_active = False
        obj.save()
        return None

    return result







def task():
    obj = Domains.objects.all().values_list('domain')
    logger.info('开始域名task')
    for domain in obj:
        try:
            result_nds = get_dns_resolver(domain[0])
            logger.info(result_nds)
            if 'A' in result_nds.keys():
                ass_ip = Assets.objects.get(ip=result_nds['A'])
                if ass_ip.pk:
                    obj_info = Domains.objects.get(domain=result_nds['domain'])
                    obj_info.resolve = ass_ip
                    obj_info.save()
                    logger.info('域名{} A 数据库操作完成'.format(domain[0]))
            else:
                obj_info = Domains.objects.get(domain=result_nds['domain'])
                obj_info.resolve = None
                obj_info.save()
                logger.info('域名{} CNAME 数据库操作完成'.format(domain[0]))

        except Exception as err:
            logger.error('获取域名%s DNS解析失败'.format(domain[0]), err)

    try:
        obj_ssl = Domains.objects.filter(is_encryption=True).values_list('domain')
        for domain in obj_ssl:
            result_ssl = get_ssl(domain[0])
            if result_ssl:
                obj = Domains.objects.get(domain=domain[0])
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
                logger.info('域名{}数据库操作完成'.format(domain[0]))
            else:
                logger.error('get_ssl函数执行失败 域名{}'.format(domain[0]))
    except Exception as err:
        logger.error('获取域名{}ssl 失败'.format(domain[0]), err)