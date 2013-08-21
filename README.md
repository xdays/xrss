#简介
自动获取博客更新内容，以邮件形式发出

#功能模块
* 解析博客RSS
* 将内容填充模版生成HTML
* 将生成HTML发送给Gmail
* 全程写日志

#配置文件介绍
##邮件配置
* addresser 发送者邮箱
* password 发送者密码

##主程序配置
* template\_dir 模板路径
* template\_file 模板文件名
* stale\_date 过期日志
* urls RSS源列表
* recipients 收件人列表

##日志配置
标准的Python日志模块配置

#模块列表
* ConfigParser
* logging
* logging.config
* feedparser
* datetime
* mailer
* jinja2

#工具
##exractrss.py
用于从网页中提取RSS源链接
