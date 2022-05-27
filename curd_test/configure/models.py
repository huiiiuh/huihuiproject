import json

import IPy
from django.db import models, transaction
from django.db.models import Q

from utils.common import to_dict


class NetworkArea(models.Model):
    """网络区域"""
    IMPORT_LEVEL = ((1, "一般重要"), (2, "重要"), (3, "非常重要"))
    id = models.AutoField(primary_key=True, unique=True, verbose_name="网络区域id")
    area_name = models.CharField(max_length=64, unique=True, verbose_name="区域名称")
    ip_list = models.JSONField(verbose_name='ip列表')
    important_level = models.IntegerField(choices=IMPORT_LEVEL, verbose_name="重要性")
    area_color = models.CharField(max_length=64, null=True, blank=True, verbose_name="区域颜色")
    description = models.TextField(null=True, blank=True, verbose_name="描述")
    create_user = models.IntegerField(null=True, blank=True, verbose_name="创建者")
    update_user = models.IntegerField(null=True, blank=True, verbose_name="修改者")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = "network_area"
        verbose_name = "network_area"
        ordering = ['-create_time', '-important_level']

    @staticmethod
    def get_query_network_area_by_id(network_area_id: int):
        """
        根据id获取区域记录
        """
        network_area = NetworkArea.objects.get(id=network_area_id)
        return network_area

    @staticmethod
    def get_query_network_area_by_area_name(area_name: str):
        network_area = NetworkArea.objects.get(area_name=area_name)
        return network_area

    @staticmethod
    def get_query_network_area_by_important_leve(queryset, important_leve: int):
        queryset = queryset.filter(important_level=important_leve)
        return queryset

    @staticmethod
    def get_query_network_area_by_keyword(queryset, keyword: str):
        """
        根据keyword模糊查询区域名称、IP、描述
        """
        import re

        def isIP(str):
            p = re.compile('^((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)(/*?)(\d*?)')
            if p.match(str):
                return True
            else:
                return False

        flag = isIP(keyword)
        if flag:
            if '/' in keyword:
                keyword = re.split(',|/', keyword)
                for key in keyword:
                    queryset = queryset.filter(ip_list__icontains=key)
            else:
                queryset = queryset.filter(ip_list__icontains=keyword)
        else:
            queryset = queryset.filter(Q(area_name__icontains=keyword) | Q(description__icontains=keyword))

        return queryset

    @staticmethod
    def order_by_sort_list(queryset, sort_by: str):
        sort_by_list = sort_by.split(',')
        for sort_rule in sort_by_list:
            queryset = queryset.order_by(sort_rule)
        return queryset

    @staticmethod
    def update_network_area_by_id(network_area_id: int, data: dict):
        """
        修改网络区域
        """
        if 'ip_list' in data.keys():
            data['ip_list'] = json.dumps(data['ip_list'])
        network_area = NetworkArea.get_query_network_area_by_id(network_area_id)
        network_area.__dict__.update(**data)
        network_area.save()
        return network_area

    @staticmethod
    def delete_network_area_by_id(network_area_id: int):
        """
        删除网络区域
        """

        with transaction.atomic():
            network_area = NetworkArea.get_query_network_area_by_id(network_area_id)
            network_area.delete()


class IpListDetails(models.Model):
    """
    ip_list描述
    """
    id = models.AutoField(primary_key=True, unique=True, verbose_name="id")
    ip = models.GenericIPAddressField(max_length=64, verbose_name="ip")
    network_area = models.ForeignKey(NetworkArea, on_delete=models.CASCADE, verbose_name="network_area_id")
    min_mask = models.BigIntegerField(verbose_name="最小子网掩码")
    max_mask = models.BigIntegerField(verbose_name="最大子网掩码")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'ip_list_details'
        verbose_name = 'ip_list_details'
        ordering = ['-max_mask']

    @staticmethod
    def bulk_create_ip_list_details(data):
        """批量插入"""
        IpListDetails.objects.bulk_create(data)

    @staticmethod
    def delete_ip_list_details_by_network_area_id(network_area_id):
        IpListDetails.objects.filter(network_area_id=network_area_id).delete()


class PasswordDict(models.Model):
    """
    密码字典
    """
    MAX_VERBOSE = 1

    choices_type = ((0, "DEFAULT"), (1, "CUSTOM"))
    id = models.AutoField(primary_key=True, unique=True, verbose_name="策略id")
    name = models.CharField(max_length=16, verbose_name="策略名称")
    type = models.SmallIntegerField(choices=choices_type, verbose_name="类型", default=1)
    account_list = models.JSONField(verbose_name="账号集合", null=True, blank=True)
    password_list = models.JSONField(verbose_name="密码集合", null=True, blank=True)
    note = models.TextField(verbose_name="备注", null=True, blank=True)
    create_user = models.IntegerField(verbose_name="创建人id", null=True, blank=True)
    update_user = models.IntegerField(verbose_name="更新人id", null=True, blank=True)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        """
        模型元数据选项
        """
        db_table = "password_dict"
        verbose_name = "password_dict"

    @classmethod
    def describe_pwd_dicts(cls, pwd_dicts, verbose=0):
        pwd_dict_list = []
        for pwd_dict in pwd_dicts:
            if isinstance(pwd_dict, cls):
                pwd_dict = to_dict(pwd_dict)
            pwd_dict_list.append(pwd_dict)

            # 获取密码字典详情
            if verbose == 0:
                pwd_dict.pop("account_list", None)
                pwd_dict.pop("password_list", None)

        return pwd_dict_list


class PortGroup(models.Model):
    """
    端口组
    """
    choices_type = ((0, "DEFAULT"), (1, "CUSTOM"))
    id = models.AutoField(primary_key=True, unique=True, verbose_name="端口组id")
    name = models.CharField(max_length=16, verbose_name="端口组名称")
    description = models.CharField(max_length=64, default="", verbose_name="端口组描述")
    type = models.SmallIntegerField(choices=choices_type, verbose_name="类型", default=1)
    port_info = models.JSONField(verbose_name="端口信息")
    key = models.IntegerField(null=True, blank=True, verbose_name="端口组key")
    create_user = models.IntegerField(verbose_name="创建人id", null=True, blank=True)
    update_user = models.IntegerField(verbose_name="更新人id", null=True, blank=True)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        """
        模型元数据选项
        """
        db_table = "port_group"
        verbose_name = "port_group"


class Protocol(models.Model):
    """
    协议表
    """
    id = models.AutoField(primary_key=True, unique=True, verbose_name="协议id")
    name = models.CharField(max_length=16, verbose_name="协议名称")

    class Meta:
        """
        模型元数据选项
        """
        db_table = "protocol"
        verbose_name = "protocol"


class Strategy(models.Model):
    """
    策略表
    """
    MAX_VERBOSE = 1

    choices_type = ((0, "DEFAULT"), (1, "CUSTOM"))
    id = models.AutoField(primary_key=True, unique=True, verbose_name="策略id")
    name = models.CharField(max_length=20, verbose_name="策略名称")
    type = models.SmallIntegerField(choices=choices_type, verbose_name="类型", default=1)
    asset_detect_items = models.JSONField(verbose_name="资产探测项id集合", null=True, blank=True)
    penet_test_items = models.JSONField(verbose_name="渗透测试项id集合", null=True, blank=True)
    risk_detect_items = models.JSONField(verbose_name="风险检测项id集合", null=True, blank=True)
    weak_cipher_items = models.JSONField(verbose_name="弱口令id集合", null=True, blank=True)
    note = models.TextField(verbose_name="备注", null=True, blank=True)
    create_user = models.IntegerField(verbose_name="创建人id", null=True, blank=True)
    update_user = models.IntegerField(verbose_name="更新人id", null=True, blank=True)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        """
        模型元数据选项
        """
        db_table = "strategy"
        verbose_name = "strategy"
        ordering = ['-update_user']

    @classmethod
    def describe_strategies(cls, strategies, verbose=0):
        strategy_list = []
        for strategy in strategies:
            if isinstance(strategy, cls):
                strategy = to_dict(strategy)
            strategy_list.append(strategy)
            if verbose == 0:
                strategy.pop("asset_detect_items")
                strategy.pop("risk_detect_items")
                strategy.pop("penet_test_items")
                strategy.pop("weak_cipher_items")

            elif verbose >= 1:
                # 获取测试项详情
                # 1. 获取资产探测详情(端口组)
                if strategy.get("asset_detect_items"):
                    asset_detect_items = strategy.pop("asset_detect_items", [])
                    strategy["asset_detect_items"] = \
                        PortGroup.objects.filter(id__in=asset_detect_items).values("id", "name")
                # 2. 获取风险检测详情
                if strategy.get("risk_detect_items"):
                    risk_detect_items = strategy.pop("risk_detect_items", [])
                    strategy["risk_detect_items"] = \
                        RiskDetectItems.objects.filter(id__in=risk_detect_items).values("id", "name")
                # 3. 获取渗透测试详情
                if strategy.get("penet_test_items"):
                    penet_test_items = strategy.pop("penet_test_items", [])
                    strategy["penet_test_items"] = \
                        PenetTestItems.objects.filter(id__in=penet_test_items).values("id", "name")
                # 4. 获取弱密码详情(密码字典)
                if strategy.get("weak_cipher_items"):
                    penet_test_items = strategy.pop("weak_cipher_items", [])
                    strategy["weak_cipher_items"] = \
                        PasswordDict.objects.filter(id__in=penet_test_items).values("id", "name")

        return strategy_list


class RiskDetectItems(models.Model):
    """风险检测表"""
    id = models.AutoField(primary_key=True, unique=True, verbose_name="风险检测id")
    name = models.CharField(max_length=256, verbose_name="风险检测名称")
    key = models.CharField(max_length=32, unique=True, verbose_name="风险检测key")

    class Meta:
        db_table = "risk_detect_items"
        verbose_name = "risk_detect_items"


class PenetTestItems(models.Model):
    """渗透测试表"""
    id = models.AutoField(primary_key=True, unique=True, verbose_name="渗透测试id")
    name = models.CharField(max_length=256, verbose_name="渗透测试名称")
    key = models.CharField(max_length=32, unique=True, verbose_name="渗透测试key")

    class Meta:
        db_table = "penet_test_items"
        verbose_name = "penet_test_items"
