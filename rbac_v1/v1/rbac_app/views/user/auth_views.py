from rest_framework.views import APIView

from commons.exc.custom_exc import SystemGlobalException
from commons.globals.enums import UserStatus
from commons.http.response import APIResponse
from commons.stat.stat_mapping import StatusCodeMessage
from commons.utils.jwt_helper import jwt_generate_token
from commons.utils.pwd_helper import random_pwd, encode_pwd
from v1.rbac_app.models import User
from v1.rbac_app.serializers.auth_serializers import (
    UserLoginSerializers, UserChangePWDSerializers, UserChangeActivePutSerializers,
)


class UserLoginAPIView(APIView):
    """
    用户登录
    """
    @staticmethod
    def post(request):
        serializer = UserLoginSerializers(data=request.data, context={"request": request})
        serializer.is_valid()
        username, user_id, status = serializer.validated_data.get('username'), serializer.validated_data.get('id'), serializer.validated_data.get('status')

        user = User.get_user_by_id(user_id=user_id)
        user.is_login = True
        user.save()
        return APIResponse(data={
            'token': jwt_generate_token(user_id, username),
            'id': user_id,
            'status': status
        }).get_result()


class UserLogoutAPIView(APIView):
    """
    用户注销
    """
    @staticmethod
    def post(request):
        user = request.user
        user.is_login = False
        user.save()
        return APIResponse(status=StatusCodeMessage.CODE_SUCCESS.code).get_result()


class UserChangePWDAPIView(APIView):
    """
    当前用户修改密码
    """
    @staticmethod
    def put(request):
        """
        用户账号密码修改
        """
        # 获取当前用户模型
        user = request.user
        serializer = UserChangePWDSerializers(instance=user, data=request.data, context={"user": user})
        serializer.is_valid()
        serializer.save()
        return APIResponse(data={}).get_result()


class UserResetPWDAPIView(APIView):
    """
    用户账号密码重置APIView
    """
    @staticmethod
    def put(request, user_id):
        """
        用户账号密码重置
        """
        # 1. 验证用户是否存在
        user = User.get_user_by_id(user_id=user_id)
        if not user:
            raise SystemGlobalException(StatusCodeMessage.USERNAME_NOT_EXISTS)
        # # 2. 验证重置的是否是当前已登录用户
        # if request.user == user:
        #     raise SystemGlobalException(StatusCodeMessage.CANNOT_RESET_SELF_PASSWORD)
        # 3. 生成随机密码
        new_password = random_pwd()
        # 4. 并设置新密码
        user.password = encode_pwd(new_password)
        # 4. 修改账号状态为（需要更改密码）
        user.status = UserStatus.MODIFY_PWD.value
        user.save()
        return APIResponse(data={"new_password": new_password}).get_result()


class UserChangeActiveAPIView(APIView):
    """
    用户账号状态修改APIView
    """
    @staticmethod
    def put(request, user_id):
        """
        用户账号状态修改
        """
        user = User.get_user_by_id(user_id=user_id)
        if not user:
            raise SystemGlobalException(StatusCodeMessage.USERNAME_NOT_EXISTS)

        # 获取传递过来的参数
        serializer = UserChangeActivePutSerializers(instance=user, data=request.data)
        serializer.is_valid()
        serializer.save()
        return APIResponse(data={}).get_result()
