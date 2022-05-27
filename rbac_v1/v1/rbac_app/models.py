from django.db import models

from commons.globals.enums import UserStatus, RequestMethod


class Role(models.Model):
    """
    角色信息表
    """
    id = models.AutoField(primary_key=True, unique=True, verbose_name="角色id")
    name = models.CharField(max_length=10, unique=True, verbose_name="角色名称")
    create_user = models.IntegerField(verbose_name="创建人id", null=True, blank=True)
    update_user = models.IntegerField(verbose_name="更新人id", null=True, blank=True)
    create_time = models.IntegerField(verbose_name="创建时间")
    update_time = models.IntegerField(verbose_name="更新时间")

    class Meta:
        """
        模型元数据选项
        """
        db_table = "tb_role"
        verbose_name = "tb_role"
        ordering = ['-create_time']

    @staticmethod
    def get_role_by_id(role_id):
        return Role.objects.filter(id=role_id).first()


class User(models.Model):
    """
    用户表
    """
    choices_status = (
        (UserStatus.FORBID.value, "禁用"),
        (UserStatus.ACTIVE.value, "启用"),
        (UserStatus.MODIFY_PWD.value, "需要更改密码")
    )

    id = models.AutoField(primary_key=True, unique=True, verbose_name="用户id")
    username = models.CharField(max_length=32, unique=True, verbose_name="账号")
    password = models.CharField(max_length=128, verbose_name="密码")
    nickname = models.CharField(max_length=16, db_index=True, null=True, blank=True, verbose_name="昵称")
    avatar = models.ImageField(upload_to='images/', blank=True, verbose_name="头像", default="images/default.jpg")
    phone = models.CharField(max_length=11, unique=True, verbose_name="手机号")
    email = models.CharField(max_length=64, unique=True, verbose_name="邮箱")
    status = models.SmallIntegerField(choices=choices_status, default=1, verbose_name="状态")
    is_email_notify = models.BooleanField(verbose_name="是否开启邮件通知")
    is_sms_notify = models.BooleanField(verbose_name="是否开启短信通知")
    is_login = models.BooleanField(default=False, verbose_name="是否登录")  # 用户修改密码后，需重新登陆
    # is_super = models.BooleanField(default=False, verbose_name="是否管理员")
    create_user = models.IntegerField(verbose_name="创建人id", null=True, blank=True)
    update_user = models.IntegerField(verbose_name="更新人id", null=True, blank=True)
    create_time = models.IntegerField(verbose_name="创建时间")
    update_time = models.IntegerField(verbose_name="更新时间")

    class Meta:
        """
        模型元数据选项
        """
        db_table = "tb_user"
        verbose_name = "tb_user"
        ordering = ['-create_time']

    @staticmethod
    def get_user_info_by_username(username: str):
        return User.objects.filter(username=username).values("id", "status", "password", "is_login").first()

    @staticmethod
    def get_user_by_id(user_id):
        return User.objects.filter(id=user_id).first()


class Privilege(models.Model):
    """
    权限信息表
    """
    choices_method = (
        (RequestMethod.GET.value, "GET"),
        (RequestMethod.POST.value, "POST"),
        (RequestMethod.PUT.value, "PUT"),
        (RequestMethod.PATCH.value, "PATCH"),
        (RequestMethod.DELETE.value, "DELETE")
    )
    id = models.AutoField(primary_key=True, unique=True, verbose_name="权限id")
    title = models.CharField(max_length=16, verbose_name="权限标题")
    privilege_key = models.CharField(max_length=50, unique=True, verbose_name="权限key")
    method = models.SmallIntegerField(choices=choices_method, verbose_name="请求方法", null=True, blank=True)
    route = models.CharField(max_length=255, verbose_name="路由路径", null=True, blank=True)
    pid = models.IntegerField(verbose_name="父权限id", null=True, blank=True)

    class Meta:
        """
        模型元数据选项
        """
        db_table = "tb_privilege"
        verbose_name = "tb_privilege"

    @staticmethod
    def get_privilege_list() -> list:
        privilege_lst = []
        privilege_dic = {}

        privilege_objs = Privilege.objects.values('id', 'title', 'privilege_key', 'method', 'route', 'pid')
        for privilege in privilege_objs:
            privilege_dic[privilege['id']] = privilege
            privilege_dic[privilege['id']]['children'] = []

        for privilege in privilege_objs:
            pid = privilege['pid']
            if pid is None:
                privilege_lst.append(privilege)
            else:
                parent = privilege_dic[pid]
                parent['children'].append(privilege)
        return privilege_lst


class RolePrivilege(models.Model):

    """
    角色权限关系表
    """
    id = models.AutoField(primary_key=True, unique=True, verbose_name="角色权限id")
    # privilege_id = models.IntegerField(verbose_name="权限ID")
    # role_id = models.IntegerField(verbose_name="角色ID")
    privilege_id = models.ForeignKey(Privilege, db_column="privilege_id", related_name="role_privilege", on_delete=models.DO_NOTHING, db_constraint=False, verbose_name="权限ID")
    role_id = models.ForeignKey(Role, db_column="role_id", related_name="role_privilege", on_delete=models.DO_NOTHING, db_constraint=False, verbose_name="角色ID")
    create_user = models.IntegerField(verbose_name="创建人id", null=True, blank=True)
    update_user = models.IntegerField(verbose_name="更新人id", null=True, blank=True)
    create_time = models.IntegerField(verbose_name="创建时间")
    update_time = models.IntegerField(verbose_name="更新时间")

    class Meta:
        """
        模型元数据选项
        """
        db_table = "tb_role_privilege"
        verbose_name = "tb_role_privilege"


class UserRole(models.Model):
    """
    用户角色关系表
    """
    id = models.AutoField(primary_key=True, unique=True, verbose_name="用户角色id")
    # user_id = models.IntegerField(verbose_name="用户ID")
    # role_id = models.IntegerField(verbose_name="角色ID")
    user_id = models.ForeignKey(User, db_column="user_id", related_name="user_role", on_delete=models.DO_NOTHING, db_constraint=False, verbose_name="用户ID")
    role_id = models.ForeignKey(Role, db_column="role_id", related_name="user_role", on_delete=models.DO_NOTHING, db_constraint=False, verbose_name="角色ID")
    create_user = models.IntegerField(verbose_name="创建人id", null=True, blank=True)
    update_user = models.IntegerField(verbose_name="更新人id", null=True, blank=True)
    create_time = models.IntegerField(verbose_name="创建时间")
    update_time = models.IntegerField(verbose_name="更新时间")

    class Meta:
        """
        模型元数据选项
        """
        db_table = "tb_user_role"
        verbose_name = "tb_user_role"
#
#
# class SystemLogs(models.Model):
#     """
#     系统日志表
#     """
#     action_name = models.CharField(max_length=20, verbose_name="行为名称")
#     action_description = models.TextField(null=True, blank=True, verbose_name="行为描述")
#     access_url = models.CharField(max_length=200, verbose_name="访问Url")
#     access_time = models.IntegerField(verbose_name="访问时间")
#     request_ip = models.GenericIPAddressField(verbose_name="访问时的ip")
#     user_agent = models.CharField(max_length=200, verbose_name="请求者的UserAgent")
#     user_id = models.IntegerField(null=True, blank=True, verbose_name="请求者的用户ID(非登录用户为空)")
#     success = models.BooleanField(verbose_name="操作是否成功")
#     err_message = models.CharField(null=True, blank=True, max_length=200, verbose_name="如果失败,记录失败原因")
#
#     class Meta:
#         """
#         模型元数据选项
#         """
#         db_table = "SystemLogs"
#         verbose_name = "系统日志表"
#         verbose_name_plural = verbose_name
#         ordering = ("-access_time",)
