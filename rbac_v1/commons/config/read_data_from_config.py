import os
import configparser

import threading


class Config:
    """
    根据系统环境变量自动匹配配置文件
    """
    _instance_lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not hasattr(Config, "_instance"):
            with Config._instance_lock:
                if not hasattr(Config, "_instance"):
                    Config._instance = super(
                        Config, cls).__new__(cls, *args, **kwargs)
        return Config._instance

    def __init__(self) -> None:
        self.env = os.environ.get("RBAC_ENV", "local").lower()
        _current_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        self._config = configparser.ConfigParser()
        _cur_conf_path = os.path.join(_current_path, 'conf')
        _config_path = os.path.join(_cur_conf_path, f'{self.env}.ini')
        self._config.read(_config_path, encoding='utf-8')

    def _get(self, env: str, key: str):
        return self._config.get(env, key)

    def _get_data(self, key: str):
        return self._config.get(key)

    @classmethod
    def get_config(cls, key: str):
        """
        获取指定 Key 的配置
        """
        cfg = Config()
        env = os.environ.get("RBAC_ENV", "local").lower()
        return cfg._get(env, key)
