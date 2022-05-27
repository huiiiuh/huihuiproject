class SystemGlobalException(Exception):
    """
    全局自定义异常
    """
    def __init__(self, status_code_message_obj=None, msg_detail=None, user=None):
        self.status_code_message_obj = status_code_message_obj
        self.status = status_code_message_obj.code
        self.error_info = status_code_message_obj.message
        self.error_detail = msg_detail
        self.user = user

    # def __str__(self):
    #     return f'error_info: {self.error_info}, error_detail: {self.error_detail}'
