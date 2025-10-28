# python安装
## windows
```
1.下载
    https://www.python.org/downloads/
    https://www.python.org/ftp/python/3.13.7/python-3.13.7-amd64.exe

2.安装后的python
    C:\Users\admin\AppData\Local\Programs\Python\Python313\
    sysdm.cpl
    python --version
    python -m venv env
    env\Scripts\activate
    
```
## mac
python3 -m venv env
source ./env/bin/activate

# 一.rfcli命令
```ls
通过swagger的api地址，解析出rfcli的命令行，使用RESTful API调用的命令行界面
```

## 命令简写
```
rfcli命令简写 rc
```

## 配置命令
```
 1.rc config --url:xxx 配置swagger链接的地址
 2.rc config --token:token  配置token
 3.rc config --username:xxx,--password:xxxx 配置账号密码
```




# 二.scli命令
```
使用socket.js连接调用的命令行界面
```

## 命令简写
```
scli命令简写 sc
```

## 配置命令
```
1.sc config --url:xxx 配置链接的地址
```




