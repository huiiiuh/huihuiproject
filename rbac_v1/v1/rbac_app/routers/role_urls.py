from django.urls import path

from v1.rbac_app.views.role import role_views


urlpatterns = [
    path("", role_views.RoleCreateAPIView.as_view(), name='role_create'),
    path("list", role_views.RoleListAPIView.as_view(), name='role_list'),
    path("<role_id>", role_views.RoleFindPutDelAPIView.as_view(), name='role_get_by_id,role_put_by_id,role_delete_by_id')
]
