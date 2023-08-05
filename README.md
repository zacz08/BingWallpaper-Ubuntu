这个项目的作用是获取bing的背景图片，并将其设为ubuntu的壁纸。可以选择当天的图片或者随机的图片，看完下面的介绍之后也可以自己修改程序，做出壁纸轮播等效果。

程序之在每次开机是运行一次，不会占用很多资源。我的系统版本是ubuntu22.04，经本人测试完全没问题。

使用方法：在终端中打开项目路径，运行
```bash
python3 main.py
```
或者
```bash
./RunMe.sh
```
如果提示权限不够，请看步骤[2.2](#添加执行权限)
*******


# 0.环境准备
## 0.1 安装python3
ubuntu22.04一般自带python3，如果没有，可以通过以下命令安装：
```bash
sudo apt install python3
```

## 0.2 安装pip3
没有pip的朋友可以通过下面的指令安装：
```bash
sudo apt install python3-pip
```
## 0.3 安装requests库和hashlib库
```bash
pip3 install requests
pip3 install hashlib
```

# 1. 主程序
## 1.1 获取Bing背景图片：
通过这个api：[http://bingw.jasonzeng.dev](http://bingw.jasonzeng.dev) 获取bing的背景图片。

程序中用到了api的两个参数：resolution分辨率和index序号。resolution=UHD表示高清分辨率，也可以为1920x1080等，index=0表示今天的图片，index=1表示昨天的图片，以此类推。

通过python的requests库获取图片，保存到本地，大致过程如下：
```python
url = "http://bingw.jasonzeng.dev?resolution=UHD&index=" + str(0)
picturePath = "/path/to/project/picture/background.jpg"
response = requests.get(url)
with open(picturePath, "wb") as img:
   img.write(response.content)
```
## 1.2 设置壁纸

首先比较本地图片和从api获取的图片是否相同，如果相同则不设置壁纸，如果不同则设置壁纸。

程序通过``hashlib``库计算本地已存在的图片文件和从api获得的图片的md5哈希值，并返回比较结果。

```python
def compare(data):#data是从api获取的图片的数据
    with open(picturePath,"rb") as f:
        hash_existed = hashlib.md5(f.read()).hexdigest()
        hash_new = hashlib.md5(data).hexdigest()
      return hash_new == hash_existed
```
在终端中，可以通过以下命令将图片设为壁纸：
```bash
gsettings set org.gnome.desktop.background picture-uri file:////path/to/picture.jpg
```  
在python中，用``os.system()``函数调用终端命令设置壁纸：
```python
setCommand = "gsettings set org.gnome.desktop.background picture-uri file:///{}".format(picturePath)
os.system(setCommand)
```
## 1.3当天图片和随机图片
程序的32和33行如下：
```python
img_url = url + str(0)
img_url = randomImg()
```

32行把 api 的 index 参数设为0，即当天的图片设为壁纸。
33行调用 ``randomImg()`` 函数，该函数返回一个随机0～100（可自己在函数中改变参数）的 index 参数，即随机的图片设为壁纸。_**只需把第33行注释掉程序设置的就是当天壁纸，否则就是随机壁纸**_

# 2. 开机运行程序

如果你希望获得当天图片为壁纸，建议你将程序设置为开机启动，如果你希望获得随机图片为壁纸，那么你可以不要这一步，手动运行程序。当然，如果你希望每次开机都能随机更换壁纸，那么你也可以将程序设置为开机启动。

## 2.1 sh脚本文件
内容很简单，即运行main.py，
```bash
#!/bin/bash
python3 /absolute/path/to/project/main.py
```
## 2.2 添加执行权限

在终端中进入项目路径，用下面的命令给sh脚本文件添加执行权限：
```bash
sudo chmod +x ./RunMe.sh
```

## 2.3 开机运行脚本

通过下面的命令安装启动应用程序：
```bash
sudo apt install gnome-startup-applications
``` 

打开启动应用程序，点击添加，第二栏命令通过点击右边的“浏览”选择sh脚本文件。第一栏，第三栏自己想怎么写就怎么写。
