"""
分页管理
"""

from rest_framework.pagination import PageNumberPagination

from commons.utils.drf_helper.pagination_help import custom_get_paginated_response


class UsersPageNumberPagination(PageNumberPagination):
    """
    用户列表分页器
    """
    page_query_param = "page"  # 查询字符串中代表的变量名
    page_size_query_param = "page_size"  # 查询字符串中代表每一页数据的变量名
    page_size = 10  # 每一页的数量
    # max_page_size = 1000  # 允许客户端通过查询字符串调整的最大单页数量

    def get_paginated_response(self, data):
        """
        重写分页响应
        :param data: 要分页的总数据
        :return: Response
        """
        return custom_get_paginated_response(self, data)
