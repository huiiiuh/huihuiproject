from rest_framework import serializers

from commons.exc.custom_exc import SystemGlobalException
from commons.globals.enums import UserStatus
from commons.stat.stat_mapping import StatusCodeMessage
from commons.utils.pwd_helper import verify_pwd, encode_pwd
from v1.rbac_app.models import User


class UserLoginSerializers(serializers.Serializer):
    """
    用户登录序列化器
    """
    username = serializers.CharField(max_length=20, error_messages={"max_length": "字段类型错误, 用户名已超过20个字符"})
    password = serializers.CharField()

    class Meta:
        """
        序列化器元数据选项
        """
        model = User
        fields = ["username", "password"]

    def validate(self, attrs):
        """
        请求参数验证：
        1. 验证用户是否存在
        2. 验证用户当前状态
        3. 验证用户的密码是否正确
        :param attrs: 请求体转换后的OrderedDict
        :return: attrs 验证后的
        """
        username = attrs["username"].lower()
        password = attrs["password"]

        user = User.get_user_info_by_username(username=username)
        if not user:
            raise SystemGlobalException(status_code_message_obj=StatusCodeMessage.USERNAME_NOT_EXISTS)
        if user["status"] == UserStatus.FORBID.value:
            raise SystemGlobalException(status_code_message_obj=StatusCodeMessage.USER_DISABLE)
        if not verify_pwd(password, user["password"]):
            raise SystemGlobalException(status_code_message_obj=StatusCodeMessage.USERNAME_OR_PASSWORD_ERROR)
        attrs["id"] = user["id"]
        attrs["status"] = user["status"]
        return attrs

    def create(self, validated_data):
        """
        添加方法
        """
        return validated_data

    def update(self, instance, _):
        """
        更新方法
        """
        return instance


class UserChangePWDSerializers(serializers.Serializer):
    """
    修改用户密码序列化器
    """
    old_password = serializers.CharField(min_length=1, max_length=50, error_messages={"min_length": "类型错误,密码长度不能低于1位",
                                                                                      "max_length": "类型错误, 密码长度不能超过50个字符"})
    new_password = serializers.CharField(min_length=1, max_length=50, error_messages={"min_length": "类型错误,密码长度不能低于1位",
                                                                                      "max_length": "类型错误, 密码长度不能超过50个字符"})

    def validate(self, attrs):
        """
        多字段验证方法
        :param attrs: 请求体转换后的OrderedDict
        :return: attrs
        """
        user = self.context.get("user")
        old_pwd = attrs["old_password"]
        # 验证旧密码是否正确
        if not verify_pwd(old_pwd, user.password):
            raise SystemGlobalException(status_code_message_obj=StatusCodeMessage.ORIGIN_PASSWORD_ERROR)
        return attrs

    def create(self, validated_data):
        """
        添加方法
        """
        return validated_data

    def update(self, instance, validated_data):
        """
        更新方法
        :param instance: 本次更新模型对象
        :param validated_data: 字段验证通过后的数据
        :return: instance
        """
        user = self.context.get("user")
        instance.password = encode_pwd(validated_data["new_password"])
        instance.update_user = user.id
        # 修改密码成功 踢出登录
        instance.is_login = False
        instance.save()
        return instance


class UserChangeActivePutSerializers(serializers.ModelSerializer):
    """
    修改用户状态序列化器
    """

    class Meta:
        """
        序列化器元数据选项
        """
        model = User
        fields = ["status"]

    def validate(self, attrs):
        """
        多字段验证方法
        :param attrs: 请求体转换后的OrderedDict
        :return: attrs
        """
        if not attrs:
            raise SystemGlobalException(status_code_message_obj=StatusCodeMessage.STATUS_PARAM_IS_REQUIRED)

        return attrs
