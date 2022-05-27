from rest_framework.generics import ListAPIView
from rest_framework.views import APIView

from commons.exc.custom_exc import SystemGlobalException
from commons.http.response import APIResponse
from commons.stat.stat_mapping import StatusCodeMessage
from v1.rbac_app.models import Role
from v1.rbac_app.serializers.role_serializers import RoleCreateUpdateSerializer, RoleListSerializer
from v1.rbac_app.views.role.role_filters import RoleFilter
from v1.rbac_app.views.role.role_paginations import RolePageNumberPagination


class RoleCreateAPIView(APIView):
    """
    角色创建APIView
    """
    @staticmethod
    def post(request):
        """
        角色新建
        """
        serializer = RoleCreateUpdateSerializer(data=request.data, context={"request": request})
        serializer.is_valid()
        instance = serializer.save()
        data = serializer.validated_data
        data["id"] = instance.id
        return APIResponse(data=data).get_result()


class RoleFindPutDelAPIView(APIView):
    """
    角色查询,修改,删除APIView
    """
    @staticmethod
    def get(_, role_id):
        """
        角色查询
        """
        role = Role.get_role_by_id(role_id=role_id)
        if not role:
            raise SystemGlobalException(status_code_message_obj=StatusCodeMessage.ROLE_NOT_EXISTS)
        serializer = RoleListSerializer(role)
        return APIResponse(data=serializer.data).get_result()

    @staticmethod
    def put(request, role_id):
        """
        角色修改
        """
        role = Role.get_role_by_id(role_id=role_id)
        if not role:
            raise SystemGlobalException(status_code_message_obj=StatusCodeMessage.ROLE_NOT_EXISTS)
        serializer = RoleCreateUpdateSerializer(instance=role, data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return APIResponse(data={}).get_result()

    @staticmethod
    def delete(_, role_id):
        """
        角色删除
        """
        role = Role.get_role_by_id(role_id=role_id)
        if not role:
            raise SystemGlobalException(status_code_message_obj=StatusCodeMessage.ROLE_NOT_EXISTS)
        user_role = role.user_role.count()
        if user_role != 0:
            # 只能删除未绑定的用户的角色
            raise SystemGlobalException(status_code_message_obj=StatusCodeMessage.ROLE_USER_UNBIND)
        role.delete()
        return APIResponse(data={}).get_result()


class RoleListAPIView(ListAPIView):
    """
    角色列表APIView
    """
    queryset = Role.objects.all()
    # 序列化器
    serializer_class = RoleListSerializer
    # 分页器
    pagination_class = RolePageNumberPagination
    # 过滤器
    filter_class = RoleFilter
