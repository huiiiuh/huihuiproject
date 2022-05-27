# -*- coding: utf-8 -*-

class DatabaseRouter:
    """
    A router to control all database operations on models in the auth application.
    """
    # 这是准备加入 db_user 数据库的app名字列表,
    # 如果决定吧那些app下创建的表就放到db_user中,就把app名字写到里面
    db_user_apps = (
        "rbac_app",
    )

    def db_for_read(self, model, **hints):
        """
        Attempts to read auth models go to default.
        """

        if model._meta.app_label in self.db_user_apps:
            return 'rbac_db'
        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write auth models go to default.
        """
        if model._meta.app_label in self.db_user_apps:
            return 'rbac_db'
        return None

    def allow_migrate(self, db, app_label, model=None, **hints):
        """
        Make sure the auth app only appears in the 'default' database.
        """
        if app_label in self.db_user_apps:
            return db == 'rbac_db'
        return None
