from rest_framework.response import Response


class APIResponse:
    """
    自定义Response
    """

    def __init__(self, status: str = "0", message: str = None, err_detail: str = None, data: dict = None
                 ):
        self.status = int(status)
        self.data = data
        self.result = {
            'status': self.status,
            'statusInfo': {
                'message': message,
                'detail': err_detail
            } if self.status else {},
            'data': {} if self.status else self.data
        }

    def get_result(self):
        """
        组装返回结果
        :return:
        """
        return Response(self.result)
