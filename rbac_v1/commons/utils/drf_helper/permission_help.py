
import re

from django.conf import settings
from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied

from commons.globals.enums import UserStatus, RequestMethod
from v1.rbac_app.models import UserRole, RolePrivilege, Privilege


class MyPermission(BasePermission):
    METHOD_MAP = {
        "GET": RequestMethod.GET.value,
        "POST": RequestMethod.POST.value,
        "PUT": RequestMethod.PUT.value,
        "DELETE": RequestMethod.DELETE.value
    }
    MY_URL_WHITELIST = settings.URL_WHITELIST

    def has_permission(self, request, view):
        path = request.path
        method = request.method
        if path in self.MY_URL_WHITELIST:
            return True

        user = request.user
        if not user:
            return False

        # 禁止使用
        if user.status == UserStatus.FORBID.value:
            raise PermissionDenied("the account has been frozen")
        # 必须修改密码
        if user.status == UserStatus.MODIFY_PWD.value:
            raise PermissionDenied("the account need to modify the initial password")

        role_ids = UserRole.objects.filter(user_id=user.id).values_list("role_id", flat=True)
        if not role_ids:
            return False

        privilege_ids = RolePrivilege.objects.filter(role_id__in=role_ids).values_list("privilege_id", flat=True)
        if not privilege_ids:
            return False

        privileges = Privilege.objects.filter(id__in=privilege_ids).values("method", "route", 'id')
        # privileges = Privilege.objects.filter(id__in=[39]).values("method", "route", 'id')
        for privilege in privileges:
            if privilege["route"] == "":
                privilege["route"] = '^$'
            if re.match(privilege["route"], path):
                if privilege["method"] == self.METHOD_MAP.get(method):
                    return True

        return False
