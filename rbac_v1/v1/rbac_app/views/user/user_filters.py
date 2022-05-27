"""
用户管理模块过滤器文件
"""
from django_filters import rest_framework

from v1.rbac_app.models import User


class UsersFilter(rest_framework.FilterSet):
    """
    自定义过滤器
    gte 大于等于
    lte 小于等于
    不指定默认是等于
    iexact：表示精确匹配, 并且忽略大小写
    icontains：表示模糊查询（包含），并且忽略大小写
    """
    role_id = rest_framework.CharFilter(field_name="user_role__role_id")

    class Meta:
        """
        过滤器元数据选项
        """
        model = User  # 模型名
        # 可以使用的过滤字段
        fields = ["username"]
