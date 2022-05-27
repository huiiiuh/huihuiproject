# """
# 通过对象将redis的基本操作进行封装
# """
# from threading import Lock as ThreadLock
# from multiprocessing import Lock as ProcessLock
#
# import redis
# import redis_lock
# import rediscluster
#
# from rbac.settings import REDIS_HOST, REDIS_PORT, REDIS_PWD, REDIS_DB, REDIS_PREFIX
#
#
# REDIS_THREAD_LOCK = ThreadLock()
# REDIS_PROCESS_LOCK = ProcessLock()
#
#
# class OPRedis:
#     _instance_thread_lock = ThreadLock()
#     _instance_process_lock = ProcessLock()
#
#     def __init__(self):
#         self.conn = redis.Redis(connection_pool=self._pool)
#         self.prefix = f'{REDIS_PREFIX}:'
#
#     def __new__(cls, *args, **kwargs):
#         with cls._instance_process_lock:
#             with cls._instance_thread_lock:
#                 if not hasattr(cls, '_instance'):
#                     OPRedis._instance = object.__new__(cls)
#                 if not hasattr(cls, '_pool'):
#                     OPRedis._pool = redis.ConnectionPool(host=REDIS_HOST, port=REDIS_PORT,
#                                                          password=REDIS_PWD, db=REDIS_DB)
#         return OPRedis._instance
#
#     def set_redis(self, key, value, exp_ts=None):
#         """
#         string type {'key':'value'}, set operation
#         :param key: str
#         :param value: str
#         :param exp_ts: int, expire time of key in redis
#         :return: True
#         """
#         real_key = f'{self.prefix}{key}'
#         if exp_ts:
#             res = self.conn.setex(name=real_key, value=value, time=exp_ts)
#         else:
#             res = self.conn.set(real_key, value)
#         return res
#
#     def get_redis(self, key, add_prefix=True):
#         """
#         string type {'key':'value'}, get operation
#         :param key: str
#         :param add_prefix: bool, True is to add, False isn't
#         :return: bytes type (key exists),
#                  or NoneType (key doesn't exists)
#         """
#         real_key = f'{self.prefix}{key}' if add_prefix is True else key
#         res = self.conn.get(real_key)
#         return res
#
#     def set_hash_redis(self, name, key, value):
#         """
#         hash type {'name':{'key':'value'}}, set operation
#         :param name: str or int
#         :param key: str or int
#         :param value: str or int
#         :return: 1(insert key), 0(update key)
#         """
#         real_name = f'{self.prefix}{name}'
#         res = self.conn.hset(real_name, key, value)
#         return res
#
#     def get_hash_redis(self, name, key=None):
#         """
#         hash type {'name':{'key':'value'}}, get operation
#         :param name: str
#         :param key: str
#         :return: {b'':b''} bytes dict type (key=None and name exists),
#                  or {} empty dict (key=None and name doesn't exists),
#                  or b'' bytes type (key!=None and key exists)
#                  or NoneType (key!=None and (name doesn't exists or key doesn't exists))
#         """
#         real_name = f'{self.prefix}{name}'
#         if key:
#             res = self.conn.hget(real_name, key)
#         else:
#             res = self.conn.hgetall(real_name)
#         return res
#
#     def del_hash_redis(self, name, key=None):
#         """
#         hash type {'name':{'key':'value'}}, del operation
#         :param name: str
#         :param key: str
#         :return: 1 (success of delete), 0(failure of delete, meaning key doesn't exists)
#         """
#         real_name = f'{self.prefix}{name}'
#         if key:
#             res = self.conn.hdel(real_name, key)
#         else:
#             res = self.conn.delete(real_name)
#         return res
#
#     def del_redis(self, key, add_prefix=True):
#         """
#         delete key
#         :param bool add_prefix: True内部为key加上前缀
#         :param key: str
#         :return: 1(success of delete), 0(failure of delete, meaning key doesn't exists)
#         """
#         if add_prefix is True:
#             real_key = f'{self.prefix}{key}'
#         else:
#             real_key = key
#         res = self.conn.delete(real_key)
#         return res
#
#     def all_keys_redis(self):
#         """
#         get all keys from the db in redis
#         :return: [b''] bytes list (not empty db),
#                  or [] list (empty db)
#         """
#         res = self.conn.keys()
#         return res
#
#     def clear_keys_redis(self):
#         """
#
#         :return:
#         """
#         bytes_keys = self.all_keys_redis()
#         for item_bytes_key in bytes_keys:
#             if item_bytes_key.startswith(self.prefix.encode()):
#                 self.del_redis(item_bytes_key.decode()[len(self.prefix):])
#         return
#
#     def clear_all_lock_redis(self):
#         """
#         删除redis的web后端Redis锁
#         :return:
#         """
#         bytes_keys = self.all_keys_redis()
#         for item_bytes_key in bytes_keys:
#             if item_bytes_key.startswith(WMSSRedisLock.tp_ds_lock_name_prefix.encode()):
#                 self.del_redis(item_bytes_key.decode(), add_prefix=False)
#             if item_bytes_key.startswith(WMSSRedisLock.tp_ds_lock_signal_prefix.encode()):
#                 self.del_redis(item_bytes_key.decode(), add_prefix=False)
#         return
#
#
# class RedisConnectionSingleton:
#     """
#     redis连接的单例模式
#     """
#     _instance_thread_lock = REDIS_THREAD_LOCK
#     _instance_process_lock = REDIS_PROCESS_LOCK
#
#     def __init__(self, password, db, lock_db, host='localhost', port=6379, cluster_mode=False, startup_nodes=None,
#                  max_connections=None):
#         """
#         :param str host:
#         :param int port:
#         :param str password:
#         :param int db: redis 缓存数据所在 db
#         :param int lock_db: redis 锁所在的 db
#         :param bool cluster_mode: 集群模式
#         :param NoneType or list startup_nodes: 在cluster_mode为True时才使用
#         :param int or NoneType max_connections: redis的最大连接数, None表示没有限制
#         """
#         # redis普通连接
#         if not hasattr(self, '_pool'):
#             if cluster_mode is False:
#                 self._pool = redis.ConnectionPool(host=host, port=port, password=password, db=db)
#             else:
#                 self._pool = rediscluster.ClusterBlockingConnectionPool(startup_nodes=startup_nodes, password=password,
#                                                                         db=db, max_connections=max_connections)
#         if not hasattr(self, '_conn'):
#             if cluster_mode is False:
#                 self._conn = redis.Redis(connection_pool=self._pool)
#             else:
#                 self._conn = rediscluster.RedisCluster(connection_pool=self._pool)
#         # redis锁连接
#         if not hasattr(self, '_pool_lock'):
#             if cluster_mode is False:
#                 self._pool_lock = redis.ConnectionPool(host=host, port=port, password=password, db=lock_db)
#             else:
#                 self._pool_lock = rediscluster.ClusterBlockingConnectionPool(startup_nodes=startup_nodes,
#                                                                              password=password,
#                                                                              db=lock_db, max_connections=max_connections)
#         if not hasattr(self, '_conn_lock'):
#             if cluster_mode is False:
#                 self._conn_lock = redis.Redis(connection_pool=self._pool_lock)
#             else:
#                 self._conn_lock = rediscluster.RedisCluster(connection_pool=self._pool_lock)
#
#     def __new__(cls, *args, **kwargs):
#         with cls._instance_process_lock:
#             with cls._instance_thread_lock:
#                 if not hasattr(cls, '_instance'):
#                     cls._instance = object.__new__(cls)
#         return cls._instance
#
#     @property
#     def conn(self):
#         return self._conn
#
#     @property
#     def conn_lock(self):
#         return self._conn_lock
#
#
# class WMSSRedisLock(redis_lock.Lock):
#     """
#     redis锁的继承类(单redis和集群都可用)
#     """
#     tp_ds_lock_name_prefix = f'{REDIS_PREFIX}:'
#     tp_ds_lock_signal_prefix = f'{REDIS_PREFIX}-signal:'
#
#     def __init__(self, redis_client, name, expire=None, lck_id=None, auto_renewal=False, strict=True, signal_expire=1000):
#         super().__init__(redis_client, name, expire=expire, id=lck_id, auto_renewal=auto_renewal, strict=strict,
#                          signal_expire=signal_expire)
#         self._name = self.tp_ds_lock_name_prefix + name
#         self._signal = self.tp_ds_lock_signal_prefix + name
#
#
# class WMSSRedisBlockLock:
#     """ redis阻塞锁, redis超时阻塞锁的获取和释放 """
#
#     def __init__(self, lock_name, time_out=None, remark='', catch_exc=True, host=REDIS_HOST, port=REDIS_PORT,
#                  password=REDIS_PWD, db=REDIS_DB, lock_db=REDIS_DB, cluster_mode=False,
#                  startup_nodes=None):
#         """
#         获取锁名
#         :param str lock_name: redis锁名
#         :param int or NoneType time_out: 阻塞的超时时间
#         :param str remark:
#         :param bool catch_exc: True 捕捉不抛出异常, False 不捕捉抛出异常
#         :param str host:
#         :param int port:
#         :param str or NoneType password:
#         :param int db:
#         :param int lock_db:
#         :param bool cluster_mode:
#         :param list or NoneType startup_nodes:
#         :return:
#         """
#         self.time_out = time_out
#         self.lock_name_prefix = WMSSRedisLock.tp_ds_lock_name_prefix
#         self.lock_name = lock_name
#         self.real_lock_name = f"{self.lock_name_prefix}{lock_name}"
#         redis_singleton = RedisConnectionSingleton(password=password, db=db, lock_db=lock_db, host=host,
#                                                    port=port, cluster_mode=cluster_mode,
#                                                    startup_nodes=startup_nodes)
#         redis_conn_lock = redis_singleton.conn_lock
#         self.redis_block_lock = WMSSRedisLock(redis_conn_lock, lock_name)
#         self.remark = remark
#         self.catch_exc = catch_exc
#
#     def __enter__(self):
#         """
#         获取锁
#         :return:
#         """
#         try:
#             if isinstance(self.time_out, int):
#                 self.redis_block_lock.acquire(timeout=self.time_out)  # 超时阻塞
#             else:
#                 self.redis_block_lock.acquire()  # 阻塞
#         except Exception as e:
#             errmsg = f'Info: {e}\nRemark: {self.lock_name} lock failure, extra remark is {self.remark}'
#             print(errmsg)
#         return
#
#     def __exit__(self, exc_type, exc_val, exc_tb):
#         """
#         释放锁
#         :param exc_type: 通过exc_type参数接收到的值, 来判断程序执行是否出现异常(如果是None, 说明没有异常)
#         :param exc_val:
#         :param exc_tb:
#         :return:
#         """
#         # 释放锁
#         try:
#             self.redis_block_lock.release()
#         except Exception as e:
#             errmsg = f'Info: {e}\nRemark: {self.lock_name} unlock failure, extra remark is {self.remark}'
#             print(errmsg)
#         if exc_type is None:
#             # '正常执行'
#             return True
#         else:
#             # 出现异常, 可以选择怎么处理异常
#             # 返回值决定了捕获的异常是否继续向外抛出
#             # 如果是False那么就会继续向外抛出, 程序会看到系统提示的异常信息
#             # 如果是True不会向外抛出, 程序看不到系统提示信息, 只能看到else中的输出
#             err_pos = exc_tb.tb_frame.f_code.co_filename
#             err_content = f"Info: {';'.join(map(str, exc_val.args))} \nRemark: {self.remark}"
#             err_line_no = exc_tb.tb_lineno
#             print(err_line_no, err_pos, err_content)
#             _catch_exc = self.catch_exc
#             return _catch_exc
