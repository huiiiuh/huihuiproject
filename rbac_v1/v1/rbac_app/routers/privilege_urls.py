from django.urls import path

from v1.rbac_app.views.privilege import privilege_views


urlpatterns = [
    path("list", privilege_views.PrivilegeListAPIView.as_view()),
]
