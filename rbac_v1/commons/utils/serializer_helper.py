


def get_msg_detail_by_serializer_obj(serializers):
    """
    获取参数校验详情
    :param serializers: 序列化类
    :return:
    """
    return [f"{k}:{v}" for k, v in serializers.errors.items()][0]
