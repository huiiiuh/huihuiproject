"""
密码验证
"""
import random
import string

from hashlib import md5

from rbac.settings import SECRET_KEY


def encode_pwd(password: str):
    md5_obj = md5(SECRET_KEY.encode("utf-8"))
    md5_obj.update(password.encode("utf-8"))

    return md5_obj.hexdigest()


def verify_pwd(plain_pwd, hash_pwd):
    md5_obj = md5(SECRET_KEY.encode("utf-8"))
    md5_obj.update(plain_pwd.encode("utf-8"))

    return md5_obj.hexdigest() == hash_pwd


def random_pwd():
    """
    生成随机密码
    """
    src = string.ascii_letters + string.digits
    for _ in range(int(1)):
        list_passwd_all = random.sample(src, 5)  # 从字母和数字中随机取5位
        list_passwd_all.extend(random.sample(string.digits, 1))  # 让密码中一定包含数字
        list_passwd_all.extend(random.sample(string.ascii_lowercase, 1))  # 让密码中一定包含小写字母
        list_passwd_all.extend(random.sample(string.ascii_uppercase, 1))  # 让密码中一定包含大写字母
        random.shuffle(list_passwd_all)  # 打乱列表顺序
        str_passwd = ''.join(list_passwd_all)  # 将列表转化为字符串
        return str_passwd


if __name__ == '__main__':
    pwd = encode_pwd('123456')
    print('encode: ', pwd)
    print('verify result: ', verify_pwd('123456', pwd))
    rand_str = random_pwd()
    print(rand_str)


