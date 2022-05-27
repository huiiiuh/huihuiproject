
import datetime

from rest_framework.authentication import BaseAuthentication

from rbac.settings import URL_WHITELIST
from commons.exc.custom_exc import SystemGlobalException
from commons.stat.stat_mapping import StatusCodeMessage
from commons.utils.jwt_helper import jwt_parse_token
from v1.rbac_app.models import User


class LoginAuthenticate(BaseAuthentication):
    # 认证类，继承BaseAuthentication，其中重写authenticate方法
    def authenticate(self, request):
        path = request.path
        print(path)
        if path in URL_WHITELIST:
            return
        token = request.META.get("HTTP_AUTHORIZATION")
        # 认证的逻辑按照实际情况来，这里假设从get请求的请求体中拿token
        if not token:
            # 校验不成功，没有token或者token不存在，使用这个模块来抛出异常
            raise SystemGlobalException(status_code_message_obj=StatusCodeMessage.NOT_TOKEN)
        payload = jwt_parse_token(token.split()[-1])
        exp, user_id, user_name = payload['exp'], payload['data']['user_id'], payload['data']['user_name']
        user = User.get_user_by_id(int(user_id))
        if not user:
            raise SystemGlobalException(status_code_message_obj=StatusCodeMessage.USERNAME_NOT_EXISTS)
        if user.username != user_name:
            raise SystemGlobalException(status_code_message_obj=StatusCodeMessage.TOKEN_PAYLOAD_ERROR)
        now = int(datetime.datetime.utcnow().timestamp())
        if now > exp:
            if user.is_login:
                user.is_login = False
                user.save()
            raise SystemGlobalException(status_code_message_obj=StatusCodeMessage.TOKEN_EXPIRED)
        if not user.is_login:
            raise SystemGlobalException(status_code_message_obj=StatusCodeMessage.USER_NO_LOGIN)
        return user, token


