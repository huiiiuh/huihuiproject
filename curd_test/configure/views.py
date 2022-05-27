# Create your views here.
import json
import os

from django.db import transaction

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.assets.models import Assets
from apps.configure.models import NetworkArea, PasswordDict, PortGroup, RiskDetectItems, PenetTestItems, Strategy
from apps.configure.serializers import NetworkAreaSerializers, ImportantAssetsSerializers
from apps.configure.serializers import StrategyCreateUpdateSerializer
from hubo_system_backend.settings import BASE_DIR
from utils.base_viewset import BaseModelViewSet
from utils.common import Type, to_dict
from utils.download_help import download_file


class NetworkAreaModelViewSet(BaseModelViewSet):
    queryset = NetworkArea.objects.all()
    serializer_class = NetworkAreaSerializers

    def get_queryset(self):
        queryset = self.queryset
        query_params = self.request.query_params
        keyword, sort_by = query_params.get(
            'keyword', None), query_params.get(
            'sort_by', None)
        if keyword:
            queryset = NetworkArea.get_query_network_area_by_keyword(
                queryset, keyword)
        if sort_by:
            queryset = NetworkArea.order_by_sort_list(queryset, sort_by)

        important_level = query_params.get('important_level', None)
        if important_level:
            queryset = NetworkArea.get_query_network_area_by_important_leve(
                queryset, int(important_level))
        return queryset

    # def file_iterator(self, file_path, chunk_size=512):
    #     """
    #     文件生成器,防止文件过大，导致内存溢出
    #     :param file_path: 文件绝对路径
    #     :param chunk_size: 块大小
    #     :return: 生成器
    #     """
    #     with open(file_path, mode='rb') as f:
    #         while True:
    #             c = f.read(chunk_size)
    #             if c:
    #                 yield c
    #             else:
    #                 break
    #
    # @action(methods=['get'], detail=False)
    # def down(self, request, *args, **kwargs):
    #     tmp_path = os.path.join(BASE_DIR, 'media','template',
    #                             '域名导入模板1111.7z')
    #     response = download_file(tmp_path, '域名导入模板.7z')
    #     return response


"""
重要资产展示逻辑:
任务完成后会有资产清单, 资产初始的important_level重要性全为0(未知),
配置资产页面展示重要性全为0的记录
重要资产页面展示重要性为[1.2.3]的记录
删除重要资产则将重要性改为0
"""


class ImportantAssetsModelViewSet(BaseModelViewSet):
    queryset = Assets.objects.all()
    serializer_class = ImportantAssetsSerializers

    # http_method_names = ['get', 'put', 'delete']  # 测试阶段post添加数据

    def get_queryset(self):
        queryset, query_params = self.queryset, self.request.query_params
        is_show, important_level = query_params.get(
            'is_show', None), query_params.get(
            'important_level', None)
        keyword, sort_by = query_params.get(
            'keyword', None), query_params.get(
            'sort_by', None)
        network_area_id, ip = query_params.get('network_area_id', None), query_params.get('ip', None)
        if is_show:
            queryset = Assets.get_query_assets_by_is_show(queryset, [0])
        else:
            queryset = Assets.get_query_assets_by_is_show(queryset, [1, 2, 3])
        if keyword:
            queryset = Assets.get_query_assets_by_keyword(queryset, keyword)
        if sort_by:
            queryset = Assets.order_by_sort_list(queryset, sort_by)
        if important_level:
            queryset = Assets.get_query_assets_by_important_level(
                queryset, int(important_level))
        if network_area_id:
            queryset = Assets.get_query_assets_by_network_area_id(queryset, int(network_area_id))
        if ip:
            queryset = Assets.get_query_assets_by_ip(queryset, ip)
        return queryset

    def destroy(self, request, *args, **kwargs):
        """删除"""
        pk = kwargs.get('pk')
        Assets.delete_assets_by_id(int(pk))
        return Response({'message': '成功'})

    @action(methods=['delete'], detail=False)
    def multiple_delete(self, request, *args, **kwargs):
        delete_id = request.data.get('delete_id', None)
        if not delete_id:
            raise ValueError('multiple_delete error assets:not fund delete_id')
        with transaction.atomic():
            for id in delete_id:
                Assets.delete_assets_by_id(id)
        return Response({'message': '成功'})


class PWDDictsAPIView(APIView):
    @staticmethod
    def get(request):
        """字典列表"""
        params = request.query_params
        page = int(params.get("page", 1))
        page_size = int(params.get("page_size", 10))
        keyword = params.get("keyword")
        total_only = params.get("total_only")
        sort_by = request.data.get("sort_by")

        obj = PasswordDict.objects

        # 根据关键字筛选
        if keyword:
            obj = obj.filter(name__icontains=keyword)

        total_count = obj.count()
        data = {"total_count": total_count}
        if total_only:
            return Response({"data": data})

        data["pwd_dicts"] = []
        if sort_by:
            sort_by = sort_by.split(",")
            for sort in sort_by:
                obj = obj.order_by(sort)

        # 分页
        pwd_dicts = obj.all()[(page - 1) * page_size: page * page_size]
        if pwd_dicts:
            pwd_dicts = PasswordDict.describe_pwd_dicts(pwd_dicts)
            data["pwd_dicts"] = pwd_dicts

        return Response({"data": data})


class TestItemsAPIView(APIView):
    @staticmethod
    def get(request):
        """获取测试项"""
        # 1. 资产探测数据(端口组)
        query_fields = ["id", "name", "type", "port_info", "description"]
        default_port_groups = list(PortGroup.objects.filter(type=Type.DEFAULT.value).values(*query_fields))
        custom_port_groups = list(PortGroup.objects.filter(type=Type.CUSTOM.value)[:10].values(*query_fields))
        asset_detect_items = []
        for port_group in (default_port_groups + custom_port_groups):
            ports = []
            [ports.extend(i) for i in port_group.pop("port_info", {}).values()]
            port_group["ports"] = list(set(ports))
            asset_detect_items.append(port_group)

        # 2. 风险检测数据
        risk_detect_items = [to_dict(r) for r in RiskDetectItems.objects.all()]

        # 3. 渗透测试数据
        penet_test_items = [to_dict(p) for p in PenetTestItems.objects.all()]

        data = {
            "asset_detect_items": asset_detect_items,
            "risk_detect_items": risk_detect_items,
            "penet_test_items": penet_test_items
        }
        return Response({"data": data})


class StrategiesAPIView(APIView):
    @staticmethod
    def get(request):
        """策略列表接口"""
        params = request.query_params
        page = int(params.get("page", 1))
        page_size = int(params.get("page_size", 10))
        keyword = params.get("keyword")
        total_only = params.get("total_only")
        sort_by = request.data.get("sort_by")

        obj = Strategy.objects

        # 根据关键字筛选
        if keyword:
            obj = obj.filter(name__icontains=keyword)

        total_count = obj.count()
        data = {"total_count": total_count}
        if total_only:
            return Response({"data": data})

        data["strategies"] = []
        if sort_by:
            sort_by = sort_by.split(",")
            for sort in sort_by:
                obj = obj.order_by(sort)

        # 分页
        strategies = obj.all()[(page - 1) * page_size: page * page_size]
        if strategies:
            strategies = Strategy.describe_strategies(strategies)
            data["strategies"] = strategies

        return Response({"data": data})

    @staticmethod
    def post(request):
        """策略创建接口"""
        serializer = StrategyCreateUpdateSerializer(data=request.data, context={"user": request.user})
        serializer.is_valid(raise_exception=True)
        strategy = serializer.save()
        strategy = Strategy.describe_strategies([strategy], verbose=Strategy.MAX_VERBOSE)[0]

        return Response({"data": {"strategy": strategy}})


class SingleStrategyAPIView(APIView):
    @staticmethod
    def get(request, pk):
        """获取策略详情"""
        strategy = Strategy.objects.get(pk=pk)
        strategy = Strategy.describe_strategies([strategy], verbose=Strategy.MAX_VERBOSE)[0]
        return Response({"data": {"strategy": strategy}})

    @staticmethod
    def put(request, pk):
        """修改策略"""
        strategy = Strategy.objects.get(pk=pk)
        serializer = StrategyCreateUpdateSerializer(
            strategy, data=request.data, partial=True, context={"user": request.user})
        serializer.is_valid(raise_exception=True)
        strategy = serializer.save()
        strategy = Strategy.describe_strategies([strategy], verbose=Strategy.MAX_VERBOSE)[0]

        return Response({"data": {"strategy": strategy}})

    @staticmethod
    def delete(request, pk):
        """删除策略"""
        strategy = Strategy.objects.get(pk=pk)
        strategy.delete()

        return Response({})
