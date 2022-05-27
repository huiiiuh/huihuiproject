from rest_framework.generics import ListAPIView
from rest_framework.views import APIView

from commons.exc.custom_exc import SystemGlobalException
from commons.http.response import APIResponse
from commons.stat.stat_mapping import StatusCodeMessage
from v1.rbac_app.models import User
from v1.rbac_app.serializers.user_serializers import (
    UserCreateSerializers, UserListSerializers, UserPutSerializers
)
from v1.rbac_app.views.user.user_filters import UsersFilter
from v1.rbac_app.views.user.user_paginations import UsersPageNumberPagination


class UserCreateAPIView(APIView):
    """
    用户创建APIView
    """
    @staticmethod
    def post(request):
        """
        用户创建
        """
        # 实例化序列化器对象
        create_user_serializer = UserCreateSerializers(data=request.data, context={"request": request})
        # 调用验证方法
        create_user_serializer.is_valid()
        instance = create_user_serializer.save()
        data_serializer = UserListSerializers(instance)
        return APIResponse(data=data_serializer.data).get_result()


class UserListView(ListAPIView):
    """
    用户列表APIView
    """
    queryset = User.objects.all()
    serializer_class = UserListSerializers
    # 分页器
    pagination_class = UsersPageNumberPagination
    # 过滤器
    filter_class = UsersFilter


class UserFindUpdateDelAPIView(APIView):
    """
    用户查询,更新APIView
    """
    @staticmethod
    def get(_, user_id):
        """
        用户查询
        """
        user = User.get_user_by_id(user_id=user_id)
        if not user:
            raise SystemGlobalException(StatusCodeMessage.USERNAME_NOT_EXISTS)
        serializer = UserListSerializers(user)
        return APIResponse(data=serializer.data).get_result()

    @staticmethod
    def put(request, user_id):
        """
        用户修改
        """
        user = User.get_user_by_id(user_id=user_id)
        if not user:
            raise SystemGlobalException(StatusCodeMessage.USERNAME_NOT_EXISTS)
        serializer = UserPutSerializers(instance=user, data=request.data)
        # 调用验证方法
        serializer.is_valid()
        serializer.save()
        return APIResponse(data={}).get_result()

    @staticmethod
    def delete(request, user_id):
        """
        用户删除
        """
        user = User.get_user_by_id(user_id=user_id)
        if not user:
            raise SystemGlobalException(StatusCodeMessage.USERNAME_NOT_EXISTS)
        user.delete()
        return APIResponse(data={}).get_result()
