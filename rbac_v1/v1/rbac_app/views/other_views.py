from rest_framework.views import APIView

from commons.exc.custom_exc import SystemGlobalException
from commons.stat.stat_mapping import StatusCodeMessage


class RbacTestAPIView(APIView):
    """
    用户列表APIView
    """
    @staticmethod
    def get(request):
        """
        """
        # print(request)
        # 1/0
        raise SystemGlobalException(status_code_message_obj=StatusCodeMessage.CODE_DATA_EXIST, msg_detail='This is not exist record')
        # return APIResponse(status=StatusCodeMessage.CODE_SUCCESS.code, message=StatusCodeMessage.CODE_SUCCESS.message, data={'result': {}}).get_result()