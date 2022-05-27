from django.db import transaction
from rest_framework import serializers

from commons.exc.custom_exc import SystemGlobalException
from commons.stat.stat_mapping import StatusCodeMessage
from commons.utils.utils import get_current_timestamp
from v1.rbac_app.models import Role, Privilege, RolePrivilege


class RoleCreateUpdateSerializer(serializers.ModelSerializer):
    """
    用户角色创建 修改序列化器
    """
    class Meta:
        """
        序列化器元数据选项
        """
        model = Role
        fields = ["name"]
        read_only_fields = ("id",)

    def validate(self, attrs):
        """
        多字段验证方法
        :param attrs: 请求体转换后的OrderedDict
        :return: attrs
        """
        privilege_id_list = attrs.get("privilege_id_list")
        if privilege_id_list:
            # 判断该权限是否存在
            db_privilege_cnt = Privilege.objects.filter(id__in=privilege_id_list).count()
            if db_privilege_cnt != len(privilege_id_list):
                raise SystemGlobalException(StatusCodeMessage.ROLE_PRIVILEGE_NOT_MATCH)
        return attrs

    def create(self, validated_data):
        """
        添加数据
        :param validated_data: 字段验证通过后的数据
        :return: validated_data
        """
        now_timestamp = get_current_timestamp()
        user_id = self.context["request"].user.id
        validated_data["create_user"] = user_id
        validated_data["update_user"] = user_id
        validated_data['create_time'] = now_timestamp
        validated_data['update_time'] = now_timestamp

        with transaction.atomic():
            sid = transaction.savepoint()
            try:
                role = Role.objects.create(**validated_data)
                # 绑定角色权限
                privilege_id_list = self.initial_data.get('privilege_id_list')
                self.role_bind_privilege(privilege_id_list, role, user_id, now_timestamp)
            except Exception as error:
                transaction.savepoint_rollback(sid)
                raise SystemGlobalException(status_code_message_obj=StatusCodeMessage.CREATE_ROLE_FAILED,
                                            msg_detail=error.args)
            transaction.savepoint_commit(sid)

        return role

    def update(self, instance, validated_data):
        """
        更新数据
        :param instance: 本次修改的模型对象
        :param validated_data: 字段验证通过后的数据
        :return: instance
        """
        now_timestamp = get_current_timestamp()
        user_id = self.context["request"].user.id
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        # 删除已绑定的权限,重新进行绑定
        RolePrivilege.objects.filter(role_id=instance).delete()
        privilege_id_list = validated_data.get("privilege_id_list")
        self.role_bind_privilege(privilege_id_list, instance, user_id, now_timestamp)

        return instance

    @staticmethod
    def role_bind_privilege(privilege_id_list, instance, user_id, now_timestamp):
        """
        角色权限绑定
        :param privilege_id_list: 权限key列表
        :param instance: 本次操作实例对象
        :param user_id 用户ID
        :param now_timestamp 当前时间戳
        """
        if not privilege_id_list:
            return
        privilege_qs = Privilege.objects.filter(id__in=privilege_id_list)
        role_privilege_objs = [RolePrivilege(privilege_id=privilege,
                                             role_id=instance,
                                             create_user=user_id,
                                             update_user=user_id,
                                             create_time=now_timestamp,
                                             update_time=now_timestamp) for privilege in privilege_qs]
        RolePrivilege.objects.bulk_create(role_privilege_objs)


class RoleListSerializer(serializers.ModelSerializer):
    """
    用户角色列表 查询序列化器
    """

    privilege_id_list = serializers.SerializerMethodField()

    @staticmethod
    def get_privilege_id_list(instance):
        """
        角色权限key
        :param instance: 当前实例对象
        :return:
        """
        privilege_id_list = [role_privilege.privilege_id.id for role_privilege in instance.role_privilege.all()]
        if not privilege_id_list:
            privilege_id_list = []
        return privilege_id_list

    class Meta:
        """
        序列化器元数据选项
        """
        model = Role
        fields = ["id", "name", "privilege_id_list"]
