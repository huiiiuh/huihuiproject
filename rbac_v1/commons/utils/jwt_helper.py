"""
生成token文件
"""
import datetime
import jwt

from rest_framework.exceptions import AuthenticationFailed

from rbac.settings import SECRET_KEY
from commons.config.read_data_from_config import Config


def jwt_generate_token(user_id, user_name):
    """
    生成token
    :param user_id: 用户ID
    :param user_name: 用户名
    :return:
    """
    days = datetime.datetime.utcnow() + datetime.timedelta(days=int(Config.get_config('token_expiration')))
    timestamp = int(days.timestamp())
    payload = {
        'exp': timestamp,  # 过期时间
        'iat': datetime.datetime.utcnow(),  # 签发时间
        'iss': 'rbac_root',  # 签发人
        'data': {'user_id': user_id, 'user_name': user_name}
    }
    token = jwt.encode(payload, SECRET_KEY, 'HS256')

    return token.decode() if isinstance(token, bytes) else token


def jwt_parse_token(token):
    """解析token
    :param token
    """
    try:
        payload = jwt.decode(jwt=token, key=SECRET_KEY, algorithms='HS256')
        return payload
    except Exception as e:
        raise AuthenticationFailed(f"token error: {e}")


if __name__ == '__main__':
    token = jwt_generate_token(2, 'nx')
    print('generate token: ', token)
    data = jwt_parse_token(token)
    print('decode token: ', data)




