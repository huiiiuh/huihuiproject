"""
# -*- coding: utf-8 -*-
Copyright(C),2017-2022,宁静之盾
Name:         base_viewset
Description:
Author:       NX
Date:         2022/5/20
"""
from django.db import transaction
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet


class BaseModelViewSet(ModelViewSet):

    def list(self, request, *args, **kwargs):
        """群查"""
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
        else:
            serializer = self.get_serializer(queryset, many=True)
        data = {
            'data': {
                self.basename: serializer.data,
                'total_count': queryset.__len__()}}
        return Response(data)

    def retrieve(self, request, *args, **kwargs):
        """单查"""
        pk = kwargs.get('pk')
        asset = self.queryset.get(id=int(pk))
        data = {'data': {self.basename: self.get_serializer(asset).data}}
        return Response(data)

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        # 直接在把已登录的user_id添加到data中
        # 把已经添加过user_id的data作为序列化的参数
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        data = {'data': {self.basename: serializer.data}}

        return Response(data)

    def update(self, request, *args, **kwargs):
        """修改"""
        pk, data = int(kwargs.get('pk')), request.data.copy()
        asset = self.queryset.get(id=pk)
        serializer = self.get_serializer(instance=asset, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(
            {'data': {self.basename: serializer.data}})

    def destroy(self, request, *args, **kwargs):
        """删除"""
        pk = kwargs.get('pk')
        self.queryset.filter(id=int(pk)).delete()
        return Response({'message': '成功'})

    @action(methods=['delete'], detail=False)
    def multiple_delete(self, request, *args, **kwargs):
        ids = request.data.get('delete_id', None)
        with transaction.atomic():
            self.queryset.filter(id__in=ids).delete()
        return Response({'message': '成功'})

    @action(methods=['put'], detail=False)
    def multiple_update(self, request, *args, **kwargs):
        data = request.data
        if not isinstance(data, list):
            raise ValueError(f'格式错误: need list but got {type(data)}')
        with transaction.atomic():
            for item in data.copy():
                id = item.get('id')
                asset = self.queryset.get(id=id)
                serializer = self.get_serializer(instance=asset, data=item, partial=True)
                serializer.is_valid(raise_exception=True)
                self.perform_update(serializer)
        return Response({'message': '成功'})
