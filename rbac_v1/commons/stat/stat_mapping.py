"""
自定义全局错误码
"""
from enum import Enum


MODULE_MAPPING: dict = {
    "USER": {
        "code": "10100",
        "name": "用户"
    },
    "ROLE": {
        "code": "10200",
        "name": "角色"
    },
    "PRIVILEGE": {
        "code": "10300",
        "name": "权限"
    }
}


class StatusCodeMessage(Enum):
    """
    自定义状态码
    """

    UNKNOWN: tuple = ("999", "未知异常")
    CODE_SUCCESS: tuple = ("0", "操作成功")
    CODE_NOT_LOGIN: tuple = ("001",  "账号未登录")
    CODE_INVALID_PASSWORD: tuple = ("002", "无效的密码")
    CODE_INVALID_TOKEN: tuple = ("003", "无效的Token")
    CODE_INVALID_PARAMS: tuple = ("004", "无效的参数")
    CODE_DATA_EXIST: tuple = ("005", "数据已存在")
    CODE_DATA_NOT_EXIST: tuple = ("006", "数据不存在")
    CODE_FIND_FAILED: tuple = ("007", "查询失败")
    CODE_SAVE_FAILED: tuple = ("008", "保存失败")
    CODE_UPDATE_FAILED: tuple = ("009", "更新失败")
    CODE_DELETE_FAILED: tuple = ("010", "删除失败")
    CODE_SERVER_BUSY: tuple = ("011", "服务器繁忙")
    CODE_REDIS_SERVER_ERROR: tuple = ("012", "Redis服务错误")
    CODE_FILE_NOT_FOUNT: tuple = ("013", "文件找不到")
    CODE_IMAGE_NOT_FOUNT: tuple = ("014", "图片找不到")
    CODE_IMAGE_FORMAT_ERROR: tuple = ("015", "图片格式错误")
    CODE_CANNOT_RESET_SELF_PASSWORD: tuple = ("016", "本账号密码不可重置")
    CODE_CANNOT_FREEZE_SELF: tuple = ("017", "不能冻结自己")
    CODE_ROLE_BIND_USER: tuple = ("018", "该角色已绑定用户")
    CODE_TEST_RECORD_COMPLETED: tuple = ("019", "测试记录已完成")
    CODE_SYSTEM_BACKUP_FAILED: tuple = ("020", "系统数据备份失败")
    CODE_INSUFFICIENT_PERMISSIONS: tuple = ("021", "暂无权限")
    CODE_DATABASE_NOT_WRITE_PERMISSIONS: tuple = ("022", "数据库无写入权限")
    CODE_DATABASE_TRANSACTION_FAILED: tuple = ("023", "数据库事务执行失败")

    # 用户模块
    USERNAME_NOT_EXISTS: tuple = ("500", "账号不存在")
    USERNAME_OR_PASSWORD_ERROR: tuple = ("501", "登陆账号或密码错误")
    USER_DISABLE: tuple = ("502", "账号已冻结")
    ORIGIN_PASSWORD_ERROR: tuple = ("503", "原密码错误")
    CANNOT_RESET_SELF_PASSWORD: tuple = ("504", "不可重置当前账号")
    STATUS_PARAM_IS_REQUIRED: tuple = ("505", "status 字段为必填字段")
    PHONE_FORMAT_ERROR: tuple = ("506", "手机号格式有误")
    EMAIL_FORMAT_ERROR: tuple = ("507", "邮箱格式有误")
    IMAGE_FORMAT_ERROR: tuple = ("508", "图片大小超过50kb")
    ROLE_NOT_MATCH: tuple = ("509", "角色匹配失败")
    CREATE_USER_FAILED: tuple = ("510", "创建用户失败")
    PARAM_ERROR: tuple = ("511", "参数有误")
    NOT_TOKEN: tuple = ("512", "没有token，需要登陆")
    TOKEN_PAYLOAD_ERROR: tuple = ("513", "用户信息错误")
    TOKEN_EXPIRED: tuple = ("514", "token过期, 请重新登陆")
    USER_NO_LOGIN: tuple = ("515", "用户未登录, 需要登陆")
    NO_PERMISSION: tuple = ("516", "无权操作")

    # 角色模块
    ROLE_NOT_EXISTS: tuple = ("700", "角色不存在")
    ROLE_USER_UNBIND: tuple = ("701", "角色的用户未解绑")
    ROLE_PRIVILEGE_NOT_MATCH: tuple = ("702", "权限匹配失败")
    CREATE_ROLE_FAILED: tuple = ("703", "创建角色失败")

    @property
    def code(self) -> str:
        """
        错误码
        :return:
        """
        return self.value[0]

    @property
    def message(self) -> str:
        """
        错误信息
        :return:
        """
        return self.value[-1]
