放在linux crontab定时执行获取外网IP，如果和之前的ip不一致，发送一封邮件到指定的邮箱中。
发送者和收件人的邮箱使用json格式储存放在相同目录下，保存为conf.json，有多个收件人用逗号隔开。
```
# JSON Format
# outlook example
{
    'sender':'xxx@xxx.xx',
    'passwd':'**********',
    'receivers':'xxx1@xxx.xx,xxx2@xxx.xx,xxx3@xxx.xx',
    'SMTPServer':'smtp-mail.outlook.com'
}
```