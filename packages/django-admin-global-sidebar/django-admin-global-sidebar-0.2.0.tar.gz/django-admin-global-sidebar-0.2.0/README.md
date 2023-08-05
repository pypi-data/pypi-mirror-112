# django-admin-global-sidebar

## 文档

- [中文文档](https://gitee.com/rRR0VrFP/django-admin-global-sidebar/)
- [English Document](https://gitee.com/rRR0VrFP/django-admin-global-sidebar/blob/master/README.en.md)

## 项目描述

为Django自带的管理站点提供可自由配置的左侧导航栏。

## 项目特性

- 支持两级菜单导航。
- 支持导航栏折叠。
- 支持菜单项权限管控。
- 可根据当前页面自动设置相应一级二级菜单激活状态。
- 菜单项支持css样式图标的显示。

## 效果图

### 两级左侧导航菜单

![两级左侧导航菜单预览图](https://gitee.com/rRR0VrFP/django-admin-global-sidebar/raw/master/doc/images/preview01.png)

### 折叠后的左侧导航菜单

![折叠后的左侧导航菜单预览图](https://gitee.com/rRR0VrFP/django-admin-global-sidebar/raw/master/doc/images/preview02.png)


## 安装

```shell
pip install django-admin-global-sidebar
```

## 使用

- 使用`django-admin-global-sidebar`会自动禁用Django 3.x提供的左侧导航。
- 在`pro/settings.py`的`INSTALLED_APPS`中引入三个依赖包。
- 在`pro/settings.py`中通过常量`DJANGO_ADMIN_GLOBAL_SIDEBAR_MENUS`来定义自定义左侧导航菜单。如果不设置常量`DJANGO_ADMIN_GLOBAL_SIDEBAR_MENUS`，则不显示左侧导航菜单。

**pro/settings.py**

```python
INSTALLED_APPS = [
    ...
    'django_static_fontawesome',
    'django_static_jquery3',
    'django_admin_global_sidebar',
    ...
]

DJANGO_ADMIN_GLOBAL_SIDEBAR_MENUS = [
    {
        "title": "首页",
        "icon": "fa fa-home",
        "url": "/admin/",
    },{
        "title": "图书管理",
        "icon": "fa fa-book",
        "children": [
            {
                "title": "分类管理",
                "icon": "fas fa-list",
                "model": "django_admin_global_sidebar_example.category",
                "permissions": ["django_admin_global_sidebar_example.view_category"],
            },{
                "title": "图书管理",
                "icon": "fas fa-book",
                "model": "django_admin_global_sidebar_example.book",
                "permissions": ["django_admin_global_sidebar_example.view_book"],
            }
        ]
    },{
        "title": "认证和授权",
        "icon": "fa fa-cogs",
        "children": [
            {
                "title": "用户管理",
                "icon": "fas fa-user",
                "model": "auth.user",
                "permissions": ["auth.view_user",],
            },
            {
                "title": "用户组管理",
                "icon": "fas fa-users",
                "model": "auth.group",
                "permissions": ["auth.view_group",],
            }
        ]
    },
]

```

## 菜单项配置

- 支持两级菜单配置。
- 菜单项配置项有：
    - `title` 字符串。表示菜单项主文字。
    - `icon` 字符串。表示菜单项图标，允许使用css样式图标。默认已加载fontawesome开源版图标。可以通过引入自己定义的图标定义文件，从而使用自已的图标样式。
    - `children` 列表。定义二级菜单列表。
    - `url`, `model` or `view` 字符串。用来计算菜单项关联的链接，按次序只有一个配置能生效。
        - `url` 表示固定链接。
        - `model` 表示模型列表页。
        - `view` 表示django中定义视图名称，最后使用`revered(view)`来计算出实际的链接.
    - `permissions` 列表。表示权限列表。
        - 列表元素可以为字符串，或字符串元组。字符串表示权限，字符串元组表示权限组合。
        - 用户只要具备permissions列表中的某项权限或某项权限组合，即可显示该菜单项。
        - 权限组合要求用户具备组合中的所有权限，才能显示该菜单项。
    - `active_patterns` 列表。菜单项激活控制正则列表。
        - 列表元素为正则表达式字符串。
        - 用于根据页面的URL路径来控制一级菜单项的打开关闭状态或二级菜单的高亮状态。
        - 正则表示式与`request.path`进行匹配。匹配则为激活状态，不匹配则处理于非激活状态。
        - 一级菜单激活状态为打开。非激活状态为关闭。
        - 二级菜单激活状态为高亮显示。非激活状态为正常显示。

## 高级用法

### 菜单列表加载函数

除了将`pro/settings.py`中的`DJANGO_ADMIN_GLOBAL_SIDEBAR_MENUS`变量设置为固定菜单列表外，还可以将`DJANGO_ADMIN_GLOBAL_SIDEBAR_MENUS`变量设置为菜单列表加载函数的引用路径。比如设置`DJANGO_ADMIN_GLOBAL_SIDEBAR_MENUS="app.menus.get_menus_by_user"`。这里要求`"app.menus.get_menus_by_user"`为函数的引用路径，可以通过`magic_import.import_from_string`引入。菜单加载函数接受唯一参数`request`并返回菜单列表，返回的菜单列表格式与`DJANGO_ADMIN_GLOBAL_SIDEBAR_MENUS`所要求的菜单列表相同。例如在`app/menus.py`中定义如下函数：

```
def get_menus_by_user(request):
    user_type = get_user_type(request.user)
    if user_type == MANAGER:
         return [{
             "title": "系统管理",
             ...
             "children": [{
                 "title": "用户管理",
                 ...
             },{
                 "title": "权限管理",
                 ...
             }]
         }]
    elif user_type == READER:
        return [{
            "title": "读者中心",
            ...
            "children": [{
                "title": "积分管理",
                ...
            }]
        }]
    else:
        return []

```

上述代码表示根据用户的类型，显示不同的菜单列表。如果是管理员，则显示“系统管理”菜单；如果是读者，则显示“读者中心”菜单。

### 从数据库中加载菜单列表

菜单列表加载函数是在Django模板解析时被调用的，这时Django的数据库引擎已经初始化完成了，所以菜单列表加载函数中可以访问数据库，从页实现“从数据库中加载菜单列表”。

### 菜单列表多语言翻译支持

因为`pro/settings.py`在解析的时候，Django的翻译机制还没有准备好，无法提供翻译服务，所以需要菜单列表多语言翻译支持的话，也需要将`DJANGO_ADMIN_GLOBAL_SIDEBAR_MENUS`配置为加载函数。在函数中，可以任意地使用Django的翻译服务。

## 版本记录

| 版本 | 发布时间 | 变更日志                                                     | 注意 |
| ------ | ---------- | ---------------------------------------------------------------- | ---- |
| v0.1.0 | 2020/04/23 | 1. 首次发布 | |
| v0.1.1 | 2020/06/20 | 2. 弹窗编辑页中不显示左侧导航。 | |
| v0.1.2 | 2020/09/01 | 3. 修正依赖包版本。 | |
| v0.1.3 | 2020/09/23 | 4. 加入对[django-app-requires](https://pypi.org/project/django-app-requires/)的支持。 | |
| v0.1.4 | 2021/04/12 | 5. 强制取消Django 3.x自带的左侧导航栏。<br />6. 修正超长页面下的左侧导航栏显示效果。 | |
| v0.2.0 | 2021/07/01 | 7. 代码使用gitee.com托管。<br />8. 添加中文文档。<br />9. 修正打开或关闭一级菜单时，页面滚动的问题。<br />10. 支持将`DJANGO_ADMIN_GLOBAL_SIDEBAR_MENUS`配置为菜单列表加载函数的引用路径。 | |
