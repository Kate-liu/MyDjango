# Django Advanced

## 概述

### Django 实战概述

![课程脉络](DjangoAdvanced.assets/课程脉络.png)



### Django 课程脉络

![1607421501290](DjangoAdvanced.assets/1607421501290.png)



## 初识 Django & 开发环境准备

### 初识 Django 

#### 课程需要的基础 

基础条件

- 有一定 Python 基础，能够使用 Python 编写代码
- 有一定的 HTML/CSS/JavaScript 基础（非必须）
- 理解 Web 应用的前后端交互 



#### 学完课程后你能掌握的内容

- 能够使用 Django Admin 搭建管理后台
- 掌握 Django 管理后台的深度定制方法，能够添加定制的功能
- Django 中间件的工作原理，能够自己设计和实现一个中间件
- 能够使用 Django 快速为企业现有系统搭建管理后台
- 精益创业的产品思维，结合 Django 1-2 天快速迭代开发出有用的企业应用 



#### Django 做了什么

- 参考 PHP MyAdmin

![1607421698876](DjangoAdvanced.assets/1607421698876.png)

- 参考 MongoDB 客户端 

![1607421734176](DjangoAdvanced.assets/1607421734176.png)



#### Django 适用于哪些场景

-  内容管理系统
  - 博客
  - CMS
  - Wiki
- 企业内部系统
  - 会议室预定
  - 招聘管理
  - ERP & CRM
  - 报表系统
- 运维管理系统
  - CMDB
  - 发布管理
  - 作业管理
  - 脚本管理
  - 变更管理
  - 故障管理 



#### Django 的优点和缺点

- 优点
  - Python 实现，代码干净、整洁
  - 提供管理后台，能够快速开发
  - 复用度高，设计、使用上遵循 DRY（Don’t repeat yourself）  原则
  - 易于扩展复用的中间件
  - 内置的安全框架
  - 丰富的第三方类库
- 缺点
  - 单体应用-不易并行开发，单点扩展
  - 不适合非常小的几行代码的项目
  - 不适合于高并发的 to C 互联网项目 



#### 哪些著名产品使用了 Django 

![1607422909622](DjangoAdvanced.assets/1607422909622.png)



#### Django 的 MTV 架构 

- Model
- Template
- View

![1607422933225](DjangoAdvanced.assets/1607422933225.png)



#### Django 的设计思想

- DRY（Don’t repeat yourself）：不重复造轮子
- MVT
- 快速开发
- 灵活易于扩展
- 松耦合
- 显式优于隐式 



### Django 开发环境准备 

#### Anaconda 介绍 

- Python 科学计算工具包：数据科学家的工具箱
- 包含了 Python 二进制发行包
- 包含 Numpy, Pandas, Matplotlib, SciPy, Bokeh, Jupyter，PyTorch, Tensorflow 等科学处理工具
- 包含了一个开源的 Python IDE：Spyder
- 包含了 Conda 包管理软件: conda install xxx 



#### PyCharm 介绍 

- PyCharm IDE，出自 JetBrains 公司，IDEA 系列产品为 JetBrains 产出的产品
- 最好用的免费 Python IDE
- PyCharm 有 Community 版本，有 Enterprise 版本
- PyCharm 社区版不支持 Django 开发， 但可以安装 Django 类库，能够实现 Django 代码的自动提示 



#### 环境准备 

- 推荐使用 Anaconda 版本，下载安装 Anaconda
- https://www.anaconda.com/products/individual
- bash ~/Downloads/Anaconda3-2020.02-MacOSX-x86_64.sh
- 安装Django到本机环境：conda install django



- 安装 PyCharm
- https://www.anaconda.com/pycharm 



#### 使用 Django 创建第一个项目 

- 创建Django项目

  - django-admin startproject recruitment(recruitment为项目名)

- 切换到项目的根目录，启动项目（监听本地所有的IP地址）

  - python manage.py runserver 0.0.0.0:8000
  - 或者
  - python manage.py runserver 127.0.0.1:8000
  - python manage.py runserver

- 浏览器本地访问：127.0.0.1:8000即可看到默认的首页

- Django数据库

  - 默认项目根目录下自动创建“db.sqlite3”文件
  - 可以在settings.py里面指定“db.sqlite3”文件的存放路径或者更改成其他的数据库引擎，如MySQL

- 访问 Django 的 admin 管理后台

  - 访问路径：127.0.0.1:8000/admin （开始无法访问，因为数据库还未初始化，提示没有这个表）
  - (1).数据库迁移，make migrations 创建数据库迁移，产生SQL脚本，使用 migrate 命令把默认的model同步到数据库，Django 会自动为 model 建立数据库表。
  - 数据库迁移：python manage.py makemigrations
  - 自动生成数据库表：python manage.py migrate
  - 此时访问 127.0.0.1:8000/admin 即可看到后台登录页面。

- 创建后台管理员账号

  - python manage.py createsuperuser
  - 根据提示输入对应的用户名，邮箱和密码

- 配置文件settings.py解读

  - 调试模式，应用注册，第三方库配置，中间件，模板引擎，国际化等  

- 后台中英切换

  - ```python
    # LANGUAGE_CODE = 'en-us'
    LANGUAGE_CODE = 'zh-hans'
    ```

![1607423749693](DjangoAdvanced.assets/1607423749693.png)





## 使用 Django 创建一个应用 – 职位管理系统 

### 产品需求 

1. 管理员能够发布职位
2. 匿名用户能够浏览职位
3. 匿名用户能够投递职位 



### 职位管理系统-建模 

职位名称，类别，工作地点，职位职责，职位要求，发布人，发布日期，修改日期 

![1607423681738](DjangoAdvanced.assets/1607423681738.png)



### 创建app & 同步数据库 

- 创建项目：django-admin startproject recruitment
- 创建职位app：python manage.py startapp job
- 数据库迁移：python manage.py makemigrations
- 自动生成数据库表：python manage.py migrate

![1607423975454](DjangoAdvanced.assets/1607423975454.png)



### 职位列表展示 

- 发布职位
- 浏览职位

- 列表页是独立页面，使用自定义的页面
- 添加如下页面
  - 职位列表页
  - 职位详情页
- 匿名用户可以访问 

![1607424001516](DjangoAdvanced.assets/1607424001516.png)



#### Django 的自定义模板 

- Django 模板包含了输出的 HTML 页面的静态部分的内容
- 模板里面的动态内容在运行时被替换
- 在 views 里面指定每个 URL 使用哪个模板来渲染页面 

- 模版继承与块（Template Inheritance & Block）
  - 模板继承允许定义一个骨架模板，骨架包含站点上的公共元素（如头部导航，尾部链接）
  - 骨架模板里面可以定义 Block 块，每一个 Block 块都可以在继承的页面上重新定义/覆盖
  - 一个页面可以继承自另一个页面
- 定义一个匿名访问页面的基础页面，基础页面中定义页头
- 添加页面 job/templates/base.html 



#### Base 模板 

- 如下 job/templates/base.html 定义了站点的标题
- 使用 block 指令定义了页面内容块，块的名称为 content，这个块可以在继承的页面中重新定义 

![1607424279009](DjangoAdvanced.assets/1607424279009.png)



#### 添加职位列表页模板 – 继承自 base.html 

- 这里使用 extends 指令来表示，这个模板继承自 base.html 模板
  - Block content 里面重新定义了 content 这个块
  - 变量：运行时会被替换， 变量用 {{variable_name}} 表示，变量是 views 层取到内容后填充到模板中的参数
  - Tag：控制模板的逻辑，包括 if, for, block 都是 tab 

![1607424449801](DjangoAdvanced.assets/1607424449801.png)



#### 模板内容自动转义 

- 不做内容转义的问题， 对于以下的模板内容

  - 你好 {{ name }}

- 当用户的名字输入如下内容时：

  - <script>alert('hello')</script>

- 结果

  - 模板展现的时候，用户打开的页面会出来一个弹窗（即页面展现时可以动态的代码）
  - 严重的安全漏洞（XSS 跨站脚本攻击）

- 模板内容自动转义：用户输入一段脚本作为名字时，页面展现时标签都被转义 



#### 职位列表的视图 

- 视图里面获取数据，把数据传入到模板中
- 示例中，使用 Django 的 model 来获取数据，数据按照职位类型排序
- 模板渲染指定了使用前面定义的 joblist.html，把 一个含有 job_list 这个 key 的 map 传入到模板 

![1607424707586](DjangoAdvanced.assets/1607424707586.png)



#### 添加 URL 路径映射 

- 让添加的页面，能够通过 URL 访问到
- /joblist/ 的路径访问到 views 里面定义的 joblist 视图
- 这个视图是一个 Method View，方法表示一个视图 
- 在app 里面的创建一个 urls.py 文件，写入下面内容

![1607424896549](DjangoAdvanced.assets/1607424896549.png)



#### 应用（app）的所有 URL 定义加入到项目（recruitment）中

- 如下图， 把 job 应用下面的 URL 都加到路由中；
- 收到请求时，先走 jobs 应用下面的 URL 路由找页面，然后再按照 admin/ 路径匹配请求 URL 

![1607425097519](DjangoAdvanced.assets/1607425097519.png)





#### 职位列表页

- 模板添加定义，View 页面添加完，URL 中也定义路由之后，再访问页面：
- http://127.0.0.1:8000/joblist/ 

![1607425298475](DjangoAdvanced.assets/1607425298475.png)





### 职位详情页展示

#### 添加职位详情页模板 – 继承自 base.html 

- 前面列表页，每个职位上有一个链接，指向职位详情页
- 同样添加如下 3 块内容：
  - 详情页模板 – 定义内容呈现（Template）
  - 详情页视图 – 获取数据逻辑 （View）
  - 定义 URL 路由 



#### 添加视图 & URL 路径映射 

- 如下在 views.py, urls.py 中分别定义了 View 视图

- 以及 URL 的路由规则 /job/job_id 来访问详情 

  - ```python
    url(r"^job/(?P<job_id>\d+)/$", views.detail, name="detail"),
    
    # ?P<job_id> 可将 访问 URL 中，job 后面的值，作为job_id，传递给 view 层
    ```

![1607425617461](DjangoAdvanced.assets/1607425617461.png)

![1607425665005](DjangoAdvanced.assets/1607425665005.png)



#### 职位详情页 

![1607425844807](DjangoAdvanced.assets/1607425844807.png)





## 产品实战：如何在 1 天之内交付面试评估系统 



































































































































