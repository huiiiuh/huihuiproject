from django.urls import path

from v1.rbac_app.views.user import user_views, auth_views

urlpatterns = [
    path("login", auth_views.UserLoginAPIView.as_view()),
    path("logout", auth_views.UserLogoutAPIView.as_view()),
    path('change_pwd', auth_views.UserChangePWDAPIView.as_view(), name="user_put_change_password"),
    path('<user_id>/reset_pwd', auth_views.UserResetPWDAPIView.as_view(), name="user_put_reset_password_by_id"),
    path('<user_id>/change_active', auth_views.UserChangeActiveAPIView.as_view(), name="user_put_status_by_id"),

    path('', user_views.UserCreateAPIView.as_view(), name="user_create"),
    path('list', user_views.UserListView.as_view(), name="user_list"),
    path('<user_id>', user_views.UserFindUpdateDelAPIView.as_view(), name="user_put_by_id,user_delete_by_id,user_get_by_id")
]
