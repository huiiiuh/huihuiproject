from rest_framework.views import APIView

from commons.globals.const import get_permission_list_by_key_list
from commons.http.response import APIResponse
from commons.utils.url_helper import get_all_url_dict
from v1.rbac_app.models import Privilege


class PrivilegeListAPIView(APIView):
    """
    权限列表 APIView
    """
    @staticmethod
    def get(request):
        """
        角色查询
        """
        result = Privilege.get_privilege_list()
        return APIResponse(data={'result': result}).get_result()


class PrivilegeAutoGenerateAPIView(APIView):
    @staticmethod
    def get(_):
        """
        根据路由自动生成权限列表
        :param _:
        :return:
        """
        result = get_all_url_dict()
        p_lst = []
        for item in result.values():
            res = get_permission_list_by_key_list(url_name_list=item['name'], url_path=item['url'])
            p_lst.extend(res)
        Privilege.objects.bulk_create([Privilege(
            title=p['title'],
            method=p['method'],
            privilege_key=p['privilege_key'],
            route=p['route']
        ) for p in p_lst])
        return APIResponse(data={'result': p_lst, 'count': len(p_lst)}).get_result()
