

from django.db import transaction
from rest_framework import serializers

from commons.exc.custom_exc import SystemGlobalException
from commons.stat.stat_mapping import StatusCodeMessage
from commons.utils.pwd_helper import encode_pwd
from commons.utils.utils import gen_uuid_str, get_current_timestamp
from commons.utils.validate_helper import validate_phone, validate_email
from v1.rbac_app.models import User, Role, UserRole


class UserCreateSerializers(serializers.ModelSerializer):
    """
    新建用户序列化器
    """
    class Meta:
        """
        序列化器元数据选项
        """
        model = User
        fields = [
            "id", "username", "password", "nickname", "avatar",
            "phone", "email", "status", "is_email_notify", "is_sms_notify"
        ]
        extra_kwargs = {
            "password": {
                "write_only": True,
                "min_length": 1,
                "max_length": 50,
                "error_messages": {
                    "min_length": "类型错误, 请确保这个字段至少包含 1 个字符",
                    "max_length": "类型错误, 密码长度不能超过50个字符",
                }
            },
            "status": {
                "read_only": True
            },
        }

    def validate(self, attrs):
        """
        多字段验证方法
        :param attrs: 请求体转换后的OrderedDict
        :return: attrs
        """
        # 校验角色是否存在
        role_id_list = self.initial_data.get('role_id_list')
        if role_id_list:
            role_count = Role.objects.filter(id__in=role_id_list).count()
            if len(role_id_list) != role_count:
                raise SystemGlobalException(status_code_message_obj=StatusCodeMessage.ROLE_NOT_MATCH)
            attrs["role_id_list"] = role_id_list

        # 校验手机号
        if attrs.get("phone") and not validate_phone(attrs.get("phone")):
            raise SystemGlobalException(status_code_message_obj=StatusCodeMessage.PHONE_FORMAT_ERROR)
        # 校验邮箱
        if attrs.get("email") and not validate_email(attrs.get("email")):
            raise SystemGlobalException(status_code_message_obj=StatusCodeMessage.EMAIL_FORMAT_ERROR)

        # 头像大小小于50kb
        if attrs.get("avatar"):
            if attrs["avatar"].size > 50 * 1024:
                raise SystemGlobalException(status_code_message_obj=StatusCodeMessage.IMAGE_FORMAT_ERROR)
            attrs["avatar"].name = gen_uuid_str() + "." + attrs["avatar"].name.rsplit('.')[-1]
        return attrs

    def create(self, validated_data):
        """
        创建用户
        :param validated_data: 字段验证通过后的数据
        :return: instance
        """
        create_user = self.context["request"].user.id
        now_timestamp = get_current_timestamp()
        role_ids = validated_data.pop("role_id_list", None)
        validated_data["password"] = encode_pwd(validated_data.pop("password"))
        validated_data["create_user"] = create_user
        validated_data["update_user"] = create_user
        validated_data['create_time'] = now_timestamp
        validated_data['update_time'] = now_timestamp

        with transaction.atomic():
            sid = transaction.savepoint()
            try:
                # 创建用户
                user = User.objects.create(**validated_data)

                # 用户角色绑定
                if role_ids:
                    roles = Role.objects.filter(id__in=role_ids).all()
                    user_roles = [UserRole(role_id=role, user_id=user, create_user=create_user, update_user=create_user,
                                           update_time=now_timestamp, create_time=now_timestamp)
                                  for role in roles]
                    UserRole.objects.bulk_create(user_roles)
            except Exception as error:
                transaction.savepoint_rollback(sid)
                raise SystemGlobalException(status_code_message_obj=StatusCodeMessage.CREATE_USER_FAILED,
                                            msg_detail=error.args)
            transaction.savepoint_commit(sid)
        return user


class UserListSerializers(serializers.ModelSerializer):
    """用户列表展示序列化器"""
    role_id_list = serializers.SerializerMethodField()

    @staticmethod
    def get_role_id_list(instance):
        """
        角色id列表
        :param instance: 当前模型实例对象
        :return:
        """
        user_role_list = UserRole.objects.filter(user_id=instance)
        if user_role_list:
            role_id_list = [user_role.role_id.id for user_role in user_role_list]
        else:
            role_id_list = []
        return role_id_list

    class Meta:
        """
        序列化器元数据选项
        """
        model = User
        fields = ["id", "username", "nickname", "avatar", "phone", "email", "role_id_list", "status"]


class UserPutSerializers(serializers.ModelSerializer):
    """
    修改用户信息序列化器
    """
    class Meta:
        """
        序列化器元数据选项
        """
        model = User
        fields = [
            "id", "username", "nickname", "avatar", "phone", "email",
            "is_email_notify", "is_sms_notify"
        ]

    def validate(self, attrs):
        return attrs


    # def validate(self, attrs):
    #     """
    #     多字段验证方法
    #     :param attrs: 请求体转换后的OrderedDict
    #     :return: attrs
    #     """
    #
    #     role_id_list = self.initial_data.get('role_id_list')
    #     if role_id_list:
    #         role_ids = [int(i) for i in role_id_list.split(",")]
    #         role_count = Role.objects.filter(id__in=role_ids).count()
    #         if len(role_ids) != role_count:
    #             raise SystemGlobalException(status_code_message_obj=StatusCodeMessage.ROLE_NOT_MATCH)
    #     attrs["role_id_list"] = role_ids
    #     # 校验角色是否存在
    #     try:
    #         role_queryset = Role.objects.filter(pk__in=attrs["role_id_list"])
    #     except ValueError:
    #         raise serializers.ValidationError(
    #             detail={"role_id_list": message.USER_ROLE_NOT_EXISTS}) from serializers.ValidationError
    #     attrs["role_id_list"] = role_queryset
    #     return attrs

