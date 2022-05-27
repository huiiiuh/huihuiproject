from django.urls import path
from rest_framework.routers import DefaultRouter

from apps.configure.views import *

router = DefaultRouter()
router.register('network_areas', NetworkAreaModelViewSet)  # 网络区域urls
router.register('important_assets', ImportantAssetsModelViewSet)  # 重要资产urls
urlpatterns = [
    path("strategies/test_items", TestItemsAPIView.as_view(), name="test_items"),  # 策略测试项查询urls
    path("pwd_dicts", PWDDictsAPIView.as_view(), name="pwd_dicts"),  # 密码字典创建、列表urls
    path("strategies", StrategiesAPIView.as_view(), name="strategies"),  # 策略创建、列表urls
    path("strategies/<pk>", SingleStrategyAPIView.as_view(), name="strategy"),  # 策略详情、修改、删除urls

]
urlpatterns += router.urls
