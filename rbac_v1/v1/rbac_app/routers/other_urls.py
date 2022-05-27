from django.urls import path

from v1.rbac_app.views import other_views
from v1.rbac_app.views.privilege import privilege_views


urlpatterns = [
    path('hello', other_views.RbacTestAPIView.as_view(), ),
    path("auto_gen_privileges", privilege_views.PrivilegeAutoGenerateAPIView.as_view())
]
