"""
自定义获取分页响应数据
"""
from collections import OrderedDict

from commons.http.response import APIResponse


def custom_get_paginated_response(self, data):
    """
    :param self: 当前对象
    :param data: 要分页的总数据
    :param model: 当前models
    :param serializers: 列表序列化器
    :return:
    """
    # get_page = self.request.query_params.get("page")
    # get_page_size = self.request.query_params.get("page_size")
    # 总页数(如果 total_only 为 true, 则不返回该值)
    total_pages = (self.page.paginator.count // self.page_size) + 1 \
        if (self.page.paginator.count % self.page_size) != 0 else self.page.paginator.count // self.page_size
    # 判断 total_only 是否在 query 里,并且值为True(只返回总数据量)
    if "total_only" in self.request.query_params and self.request.query_params.get("total_only") == "true":
        return APIResponse(data={"total_records": self.page.paginator.count})
    return APIResponse(data=OrderedDict([
        ('total_records', self.page.paginator.count),
        ('total_pages', total_pages),
        ('result', data)
    ])).get_result()
