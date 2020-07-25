# README

## 部署

* 前提环境

  |         服务          |     版本     |
  | :-------------------: | :----------: |
  |        Python         |  3.7或更高   |
  |         MySQL         |  8.0或更高   |
  | Django REST framework | 3.11.0或更高 |
  |     django-filter     |    2.2.0     |

1. MySQL配置

   请将 MySQL 的 root 用户密码设置为 root ，并运行以下指令以完成数据库的创建：

   ```mysql
   drop database djangoexample; -- 如果您的数据库中已有名为'djangoexample'的数据库，请备份数据并运行此语句
   create database djangoexample;
   ```

3. Django REST framework 配置

   请在项目根目录下运行以下语句，完成 Django REST framework的配置：

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   python manage.py runserver
   ```


至此，项目配置完毕。

## 指引

这个 demo 通过一些代码展示了一个端口是如何运行的。请先阅读 models.py 掌握数据库模型（非常简单的数据库关系）中各个表和表中列的定义，再阅读 serializers.py 和 views.py 中的代码和注释，掌握如何对数据库进行操作。其中的注释将有很大的帮助。

推荐你进入对应端口下进行一些交互，或者使用诸如 postman 的软件向端口发送消息。这时观察一下控制台，应该会有一些打印出的调试信息帮助你理解程序的哪一部分正在运行、运行结果如何。对不清楚的地方，你也可以自己加入语句帮助你理解。

通过这个 demo 你应该能够掌握以下内容：

- 后端接收到消息后，接下来会运行那些代码？使用 ModelViewSet 或 ListCreateAPIView 或其他的模板将会有什么区别？
- 我如何重写 Serializer 的方法？什么样的语句会调用我重写的方法，什么样的语句不会？
- 我如何获取一个表中符合某些条件的对象（提示：形如`Model.objects.filter()`或其他方法）？它们返回的是什么数据类型？我该如何使用这些数据类型来最终获取到我想要的值？
- 我如何在 View 中对发往端口的消息进行数据提取？我如何进行逻辑检测并抛出异常或返回状态信息？在 View 中我可以对数据表的对象进行检索或修改吗？

等等。这些代码将告诉您，或至少指引您去如何搜索这些问题的答案。在了解了这个 demo 中代码如何运行之后，您应该可以胜任项目中后端端口的编写了。