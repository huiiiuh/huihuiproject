## RBAC 框架文档

> 一般系统都需要进行权限控制，所以构造了一个基于 Django REST Framework 框架通用基于角色的权限认证系统 

### 系统模块

- 用户认证
  - [x] 用户登录
  - [x] 用户注销
  - [x] 修改密码
  - [x] 密码重置
  - [x] 更新用户状态
- 用户管理
  - [x] 创建用户
  - [x] 用户列表
  - [x] 用户详情
  - [x] 修改用户
  - [x] 删除用户
- 角色管理
  - [x] 创建角色
  - [x] 角色列表
  - [x] 角色详情
  - [x] 修改角色
  - [x] 删除角色
- 权限管理（支持父子权限）
  - [x] 权限列表
  - [x] 初始化权限基础信息
    
## 目录结构
- commons：系统工具类和方法
  
  - config: 加载配置工具类
  - exc: 全局异常捕获和自定义异常类
  - globals: 系统常量和枚举
  - http: 封装全局响应处理类
  - log: 加载日志
  - stat: 全局状态信息
  - utils: 通用工具类（jwt认证、密码处理、字段校验等）
    
    - drf_helper: Django REST Framework 帮助类(认证、权限、分页)
- conf: 全局配置文件存放目录
  
- logs: 系统的日志存放目录
  
- middlewares: 中间件

- rbac: django配置根路径, 根路由
  
- v1/rbac_app
  
   - routers: 路由分发（user、roles、privilege、others）
   - serializers: 业务逻辑
   - views: 控制层
  
- .gitignore: git忽略文件

- manager.py: 系统入口，主服务启动文件
  
- rbac.sqlite3: 数据库文件
  
- db.sqlite3: 数据库文件
  
- requirements.txt: 系统依赖第三方库

## 数据库结构设计
用户表

| 字段名          | 说明             | 类型     | 长度 | 可空 | 默认值  |
| :-------------- | :--------------- | :------- | :--- | :--- | :------ |
| id              | 用户id           | integer  | ——   | 否   | ——      |
| username        | 用户名           | varchar  | 32   | 否   | ——      |
| password        | 密码             | varchar  | 128  | 否   | ——      |
| nickname        | 昵称             | varchar  | 16   | 是   | ——      |
| avatar          | 头像             | varchar  | 100  | 否   | ——      |
| phone           | 手机号码         | varchar  | 11   | 否   | ——      |
| email           | 邮箱             | varchar  | 64   | 否   | ——      |
| status          | 状态             | smallint | ——   | 否   | 1: 激活 |
| is_email_notify | 是否启用邮箱通知 | bool     | ——   | 否   | false   |
| is_sms_notify   | 是否启动短信通知 | bool     | ——   | 否   | false   |
| is_login        | 是否登录         | bool     | ——   | 否   | false   |
| create_user     | 创建人           | integer  | ——   | 是   | ——      |
| update_user     | 更新人           | integer  | ——   | 是   | ——      |
| create_time     | 创建时间         | integer  | ——   | 否   | ——      |
| update_time     | 更新时间         | integer  | ——   | 否   | ——      |



角色表

| 字段名      | 说明     | 类型    | 长度 | 可空 | 默认值 | 取值范围 |
| :---------- | :------- | :------ | :--- | :--- | :----- | :------- |
| id          | 角色id   | integer | ——   | 否   | ——     | ——       |
| name        | 角色名称 | varchar | 10   | 否   | ——     | ——       |
| create_user | 创建人   | integer | ——   | 是   | ——     | ——       |
| update_user | 更新人   | integer | ——   | 是   | ——     | ——       |
| create_time | 创建时间 | integer | ——   | 否   | ——     | ——       |
| update_time | 更新时间 | integer | ——   | 否   | ——     | ——       |



权限表

| 字段名        | 说明     | 类型     | 长度 | 可空 | 默认值 |
| :------------ | :------- | :------- | :--- | :--- | :----- |
| id            | 权限id   | integer  | ——   | 否   | ——     |
| tItle         | 权限标题 | varchar  | 16   | 否   | ——     |
| privilege_key | 权限key  | varchar  | 50   | 否   | ——     |
| method        | 请求方法 | smallint | ——   | 否   | ——     |
| route         | 请求url  | varchar  | 255  | 否   | ——     |
| pid           | 父权限ID | integer  | ——   | 是   | ——     |



用户角色表

| 字段名      | 说明     | 类型    | 长度 | 可空 | 默认值 | 取值范围 |
| :---------- | :------- | :------ | :--- | :--- | :----- | :------- |
| id          | id       | integer | ——   | 否   | ——     | ——       |
| user_id     | 用户ID   | integer | ——   | 否   | ——     | ——       |
| role_id     | 角色ID   | integer | ——   | 否   | ——     | ——       |
| create_user | 创建人   | integer | ——   | 是   | ——     | ——       |
| update_user | 更新人   | integer | ——   | 是   | ——     | ——       |
| create_time | 创建时间 | integer | ——   | 否   | ——     | ——       |
| update_time | 更新时间 | integer | ——   | 否   | ——     | ——       |



角色权限表

| 字段名       | 说明     | 类型    | 长度 | 可空 | 默认值 | 取值范围 |
| :----------- | :------- | :------ | :--- | :--- | :----- | :------- |
| id           | id       | integer | ——   | 否   | ——     | ——       |
| privilege_id | 权限ID   | integer | ——   | 否   | ——     | ——       |
| role_id      | 角色ID   | integer | ——   | 否   | ——     | ——       |
| create_user  | 创建人   | integer | ——   | 是   | ——     | ——       |
| update_user  | 更新人   | integer | ——   | 是   | ——     | ——       |
| create_time  | 创建时间 | integer | ——   | 否   | ——     | ——       |
| update_time  | 更新时间 | integer | ——   | 否   | ——     | ——       |
## 使用说明

## 注意事项
