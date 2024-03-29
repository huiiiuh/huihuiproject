
from collections import OrderedDict

from django.utils.module_loading import import_string
from django.conf import settings
# for django 1.0
# from django.urls import RegexURLResolver, RegexURLPattern
# for django 2.0
from django.urls.resolvers import URLResolver, URLPattern


def recursion_urls(pre_namespace, pre_url, urlpatterns, url_ordered_dict):
    """
    递归的去获取URL
    :param pre_namespace: namespace前缀，以后用户拼接name
    :param pre_url: url前缀，以后用于拼接url
    :param urlpatterns: 路由关系列表
    :param url_ordered_dict: 用于保存递归中获取的所有路由
    :return:
    """
    for item in urlpatterns:
        if isinstance(item, URLPattern):  # 非路由分发
            if not item.name:
                continue
            if pre_namespace:
                name = '%s:%s' % (pre_namespace, item.name)
            else:
                name = item.name
            url = pre_url + str(item.pattern)

            url_ordered_dict[name] = {'name': name, 'url': url.replace('^', '').replace('$', '')}
        elif isinstance(item, URLResolver):
            if pre_namespace:
                if item.namespace:
                    namespace = '%s:%s' % (pre_namespace, item.namespace)
                else:
                    namespace = pre_namespace
            else:
                if item.namespace:
                    namespace = item.namespace
                else:
                    namespace = None
            recursion_urls(namespace, pre_url + str(item.pattern), item.url_patterns, url_ordered_dict)


def get_all_url_dict():
    """
    获取项目中所有的URL
    :return:
    """
    url_ordered_dict = OrderedDict()
    md = import_string(settings.ROOT_URLCONF)
    recursion_urls(None, '/', md.urlpatterns, url_ordered_dict)  # 递归去获取所有的路由
    return url_ordered_dict


