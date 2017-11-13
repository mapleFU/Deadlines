# Deadlines-死线之蓝DDL显示器
Flask + Bootstrap框架编写的显示DDL的应用
## 功能
### 用户认证
1. [用户注册](app/auth/views.py) (Done)
2. 用户管理 
3. 用户详情 (Done)
4. 设置自我信息 (Done)
5. 上传头像与默认头像 
6. 管理员等权限设置
7. 关注其他用户 
8. 重置密码 (Done)
9. 邮箱 + 令牌认证？
### DDL
1. 发布Deadline, 删除Deadline
2. 编辑自己发布的Deadline
3. 首页显示关注/所有的Deadline
4. 为Deadline设置private public模式
5. 邮件提醒
6. Deadline 分类设置
### Message
1. 站内信显示和阅读

## Quickstart
需要在instance配置环境变量SQLCODE, FLASK_ADMIN, SECRET_KEY, FLASK_CONFIG

在目录下运行
`python manage.py runserver --host 0.0.0.0`
即可以启动

