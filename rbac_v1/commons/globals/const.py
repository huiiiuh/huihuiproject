from commons.globals.enums import RequestMethod
from commons.stat.stat_mapping import MODULE_MAPPING

PRIVILEGE_INFO_MAPPING = {
    "list": {
        "title": "列表",
        "method": RequestMethod.GET.value
    },
    "get": {
        "title": "详情",
        "method": RequestMethod.GET.value
    },
    "create": {
        "title": "创建",
        "method": RequestMethod.POST.value
    },
    "put": {
        "title": "编辑",
        "method": RequestMethod.PUT.value
    },
    "patch": {
        "title": "修改",
        "method": RequestMethod.PATCH.value
    },
    "delete": {
        "title": "删除",
        "method": RequestMethod.DELETE.value
    }
}


def get_list(module_name):
    first_title = MODULE_MAPPING.get(module_name).get('name')
    new_privilege_info_mapping = dict()
    for k, item in PRIVILEGE_INFO_MAPPING.items():
        new_privilege_info_mapping[k] = {
            'title': first_title + item['title'],
            'method': item['method']
        }
    return new_privilege_info_mapping


def get_permission_by_key(p_key, url_path):
    module_dic = {}
    for module_name in MODULE_MAPPING.keys():
        new_privilege_info_mapping = get_list(module_name)
        module_dic[module_name.lower()] = new_privilege_info_mapping

    permission = {}
    for module_name, module_info in module_dic.items():
        for method_name, method_item in module_info.items():
            if module_name in p_key and method_name in p_key:
                permission['privilege_key'] = p_key
                permission['title'] = module_dic[module_name][method_name]['title']
                permission['method'] = module_dic[module_name][method_name]['method']
                permission['route'] = url_path
    return permission


def get_permission_list_by_key_list(url_name_list: str, url_path: str) -> list:
    permissions = []
    for url_key in url_name_list.split(','):
        permission = get_permission_by_key(url_key, url_path)
        permissions.append(permission)
    return permissions


# import json
# print(json.dumps(get_permission_list_by_key_list(url_name_list="role_get_by_id,role_put_by_id,role_delete_by_id", url_path="/rbac/v1/roles/1"), ensure_ascii=False))