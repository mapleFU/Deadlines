# Deadlines-死线之蓝学生生活赞助器
Flask 框架编写的显示课程、DDL的应用
## 功能
### 用户认证
1. [用户注册](app/auth/views.py) (Done)
2. 用户管理 
3. 用户详情 (Done)
4. 设置自我信息 (Done)
5. 上传头像与默认头像 (Done) 
8. 重置密码 (Done)
7. 删除之前的头像(Done)
### DDL
1. 发布Deadline
2. 完成自己的 Deadline
3. 编辑自己发布的Deadline
4. 可以选择发布自己的deadline，让他人监督(也可以选择转发？)
5. 邮件提醒或其他方式提醒
6. Deadline **分类**设置
### 课程表\(老师, 课程名\)

1. 绑定自己的账号与同济大学账号，访问课程表（并在小程序／服务端缓存）
2. 手动导入课程？
3. 对自己选过的课程进行评论（需不需要考虑中期退课？）
4. *（跟老师关联）
5. 查看课程评论
6. 转发自己对课程的评论

## 优化

1. 缓存

## Quickstart
需要在instance配置环境变量SQLCODE, FLASK_ADMIN, SECRET_KEY, FLASK_CONFIG

在目录下运行
`sudo rabbitmq-server`开启 Rabbitmq 进程

`celery worker -A celery_worker.celery --loglevel=info` 来开启Celery进程

`python manage.py runserver --host 0.0.0.0`
即可以启动

