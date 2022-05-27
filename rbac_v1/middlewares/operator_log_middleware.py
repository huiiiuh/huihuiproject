"""
自定义记录日志中间件文件
"""

import time

from django.utils.deprecation import MiddlewareMixin


# TODO
class CustomLogMiddleware(MiddlewareMixin):
    """
    自定义日志中间件
    """

    def __init__(self, get_response):
        super().__init__(get_response)
        self.access_time = None
        self.request_ip = None
        self.user_agent = None
        self.action_name = None
        self.action_description = None

    def process_request(self, request):
        """
        请求进来时
        :param request: WSGIRequest请求对象
        """
        self.access_time = int(round(time.time() * 1000))
        self.request_ip = request.META.get("HTTP_X_FORWARDED_FOR") if request.META.get(
            'HTTP_X_FORWARDED_FOR') else request.META.get("REMOTE_ADDR")
        self.user_agent = request.META.get('HTTP_USER_AGENT')

    def process_view(self, request, view_func, view_args, view_kwargs):
        """
         视图接收参数,没执行代码前
        :param request: WSGIRequest请求对象
        :param view_func: 当前请求视图对象
        :param view_args:
        :param view_kwargs:
        :return:
        """
        if request.method == "GET":
            self.action_name = eval(view_func.cls.get.__doc__.strip())[1]
            self.action_description = eval(view_func.cls.get.__doc__.strip())[0]
        elif request.method == "POST":
            self.action_name = eval(view_func.cls.post.__doc__.strip())[1]
            self.action_description = eval(view_func.cls.post.__doc__.strip())[0]
        elif request.method == "PUT":
            self.action_name = eval(view_func.cls.put.__doc__.strip())[1]
            self.action_description = eval(view_func.cls.put.__doc__.strip())[0]
        elif request.method == "DELETE":
            self.action_name = eval(view_func.cls.delete.__doc__.strip())[1]
            self.action_description = eval(view_func.cls.delete.__doc__.strip())[0]
        elif request.method == "PATCH":
            self.action_name = eval(view_func.cls.patch.__doc__.strip())[1]
            self.action_description = eval(view_func.cls.patch.__doc__.strip())[0]

    def process_response(self, request, response):
        """
        视图响应后
        :param request: WSGIRequest请求对象
        :param response: 响应对象
        :return: response
        """
        request_log = {
            "action_name": self.action_name,
            "action_description": self.action_description,
            "access_url": request.build_absolute_uri(),
            "access_time": self.access_time,
            "request_ip": self.request_ip,
            "user_agent": self.user_agent,
            "user_id": request.user.id
        }
        if response.data.get("code") == 0:
            request_log["success"] = True
        else:
            request_log["success"] = False
            request_log["err_message"] = response.data.get("message")
        # TODO
        # SystemLogs.objects.create(**request_log)
        return response
