
import traceback

from rest_framework.exceptions import ValidationError, PermissionDenied
from rest_framework.views import exception_handler

from commons.exc.custom_exc import SystemGlobalException
from commons.http.response import APIResponse
from commons.stat.stat_mapping import StatusCodeMessage
from commons.log.logger_help import log  # 自定义的日志记录使用方法
from commons.stat.status_help import get_status_code, get_module_code


def common_exception_handler(exc, context):
    # 接收内置exception_handler的异常处理结果
    response = exception_handler(exc, context)
    if response is None:
        # 处理drf未处理的异常
        if isinstance(exc, SystemGlobalException):
            log.error(f"user:{exc.user}, API Controller: {context['view'].__class__.__name__}, Request API: {context['request'].path}, Exception: {exc.error_info} Exc Details: {exc.error_detail}")
            module_status, message_info = get_status_code(context, exc)
            response = APIResponse(status=module_status, message=message_info, err_detail=exc.error_detail).get_result()
        else:
            log.error(f"user:{context['request'].user}, API Controller: {context['view'].__class__.__name__}, Request API: {context['request'].path}, Exception: {str(exc)}, Exc Details: {traceback.format_exc(exc)}")
            response = APIResponse(status=StatusCodeMessage.UNKNOWN.code, message=exc.args, err_detail=exc.args).get_result()
    else:
        # drf内部异常处理
        if isinstance(exc, ValidationError):
            log.error(f"user:{context['request'].user}, API Controller: {context['view'].__class__.__name__}, Request API: {context['request'].path}, Exception: {exc.args}, Exc Details: {exc.detail}")
            full_status = get_module_code(context) + StatusCodeMessage.PARAM_ERROR.code
            response = APIResponse(status=full_status, message=exc.detail).get_result()
        elif isinstance(exc, PermissionDenied):
            log.error(f"user:{context['request'].user}, API Controller: {context['view'].__class__.__name__}, Request API: {context['request'].path}, Exception: {exc.args}, Exc Details: {exc.detail}")
            full_status = get_module_code(context) + StatusCodeMessage.NO_PERMISSION.code
            response = APIResponse(status=full_status, message=exc.detail).get_result()
    return response
