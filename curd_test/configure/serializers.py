import json

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from apps.assets.models import Assets
from apps.configure.models import NetworkArea, Strategy
from utils.common import validate_chiness_english_num, validate_chinese_digit_letter, Type


class NetworkAreaSerializers(serializers.ModelSerializer):
    create_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', required=False)
    update_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', required=False)

    def validate_area_name(self, val):
        flat = validate_chiness_english_num(val)
        if not flat:
            raise ValueError("网络区域名称由汉字、大小写英文、数字组成")
        return val

    class Meta:
        model = NetworkArea
        fields = "__all__"
        extra_kwargs = {
            "area_name": {
                "min_length": 1,
                "max_length": 20,
                "error_messages":
                    {
                        "max_length": "请确保area_name字段不能超过 20 个字符",
                        "min_length": "请确保area_name字段不少于 1 个字符"
                    }
            }
        }


class ImportantAssetsSerializers(serializers.ModelSerializer):
    create_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', required=False)
    update_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', required=False)
    network_area = serializers.SerializerMethodField()

    def validate(self, attrs):
        if not self.instance:
            ip, network_area = self.initial_data.get("ip"), self.initial_data.get("network_area_id", None)
            assets = Assets.objects.filter(ip=ip)
            if network_area:
                assets = assets.filter(network_area_id=network_area)
            else:
                assets = assets.filter(network_area_id__isnull=True)
            if assets.exists():
                self.initial_data["important_level"] = assets.first().important_level
                assets.delete()
        return self.initial_data

    def get_network_area(self, obj):
        if obj.network_area:
            return {'id': obj.network_area.id, 'area_name': obj.network_area.area_name}
        return []

    class Meta:
        model = Assets
        fields = ('id', 'ip', 'important_level', 'network_area', 'create_time', 'update_time')


class StrategyCreateUpdateSerializer(serializers.ModelSerializer):
    """
    新建更新策略列化器
    """

    class Meta:
        model = Strategy
        fields = "__all__"

        extra_kwargs = {
            "name": {
                "min_length": 2,
                "max_length": 20,
                "error_messages": {
                    "max_length": "请确保 策略名称 不能超过 20 个字符",
                    "min_length": "请确保 策略名称 不少于 2 个字符"
                }
            }
        }

    def validate(self, attrs):
        # 校验名字
        if attrs.get("name") and not validate_chinese_digit_letter(attrs.get("name")):
            raise ValidationError("策略名称由汉字、大小写英文、数字组成")

        if attrs.get("asset_detect_items") and not isinstance(attrs["asset_detect_items"], list):
            raise ValidationError("expect list but got %s" % type(attrs["asset_detect_items"]).__name__)

        if attrs.get("penet_test_items") and not isinstance(attrs["penet_test_items"], list):
            raise ValidationError("expect list but got %s" % type(attrs["penet_test_items"]).__name__)

        if attrs.get("risk_detect_items") and not isinstance(attrs["risk_detect_items"], list):
            raise ValidationError("expect list but got %s" % type(attrs["risk_detect_items"]).__name__)

        if attrs.get("weak_cipher_items") and not isinstance(attrs["weak_cipher_items"], list):
            raise ValidationError("expect list but got %s" % type(attrs["weak_cipher_items"]).__name__)

        return attrs

    def create(self, validated_data):
        # 不能手动创建默认类型
        if validated_data.get("type") == Type.DEFAULT.value:
            raise ValidationError("strategy cannot be created manually")

        validated_data["create_user"] = self.context['user'].id
        validated_data["update_user"] = self.context['user'].id

        return super(StrategyCreateUpdateSerializer, self).create(validated_data)

    def update(self, instance, validated_data):
        # 不能手动更新默认类型
        if instance.type == Type.DEFAULT.value:
            raise ValidationError("strategy cannot be updated manually")

        validated_data["update_user"] = self.context['user'].id
        return super(StrategyCreateUpdateSerializer, self).update(instance, validated_data)
