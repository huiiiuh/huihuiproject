"""
Copyright(C),2017-2022,宁静之盾

Summary: 根据请求上下文和当前异常类获取系统状态码

Description:

Example:

2022/5/23, 邹辉,
"""
from commons.stat.stat_mapping import MODULE_MAPPING


def get_module_code(context):
    """
    获取当前模块的状态码
    :param context:
    :return:
    """
    current_view_name = ''.join(context["view"].get_view_name().split()[0]).upper()
    return MODULE_MAPPING.get(current_view_name).get('code')


def get_status_code(context, exc):
    """
    自动获取模型码,获取响应状态码
    :param context: 自定义异常的上下文
    :param exc: 全局异常类
    :return: 拼接后的状态码，异常的详细信息
    """
    module_code = get_module_code(context)
    full_status = ''.join([module_code, exc.status])
    print(full_status)
    return int(full_status), exc.error_info
