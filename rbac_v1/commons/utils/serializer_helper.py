"""
Copyright(C),2017-2022,宁静之盾

Summary: 根据序列化器获取错误详情

Description:

Example:

2022/5/23, 邹辉,
"""


def get_msg_detail_by_serializer_obj(serializers):
    """
    获取参数校验详情
    :param serializers: 序列化类
    :return:
    """
    return [f"{k}:{v}" for k, v in serializers.errors.items()][0]
