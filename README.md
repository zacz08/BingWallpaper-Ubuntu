# 项目介绍

这个项目的作用是获取bing的背景图片并设为ubuntu的壁纸。可以选择当天图片或者随机图片，看完下面的实现思路之后也可以自己修改程序，做出壁纸轮播等效果。

程序只在每次开机时运行一次，不会占用很多资源。我的系统版本是ubuntu22.04，经本人测试完全没问题。由于需要下载高清图片，程序运行时间和网速有关。

另外，api的图片更新时间和bing的更新时间似乎不一样，如果出现壁纸和bing官网不一样的，这是正常情况。

*****

# 使用方法

## 0 环境准备
### 0.1 安装python3
ubuntu22.04一般自带python3，如果没有，可以通过以下命令安装：
```bash
sudo apt install python3
```

### 0.2 安装pip3
没有pip的朋友可以通过下面的指令安装：
```bash
sudo apt install python3-pip
```
### 0.3 安装requests库和hashlib库
```bash
pip install requests
pip install hashlib
```
注意是requests不是request，不要漏了最后的s
## 1 修改配置

打开``config.yml``文件，修改``path``为项目的绝对路径；修改``mode``为你想要的模式：

|mode|说明|
|:---:|:---:|
|random|随机图片作为壁纸|
|0|当天图片作为壁纸|
|1|昨天图片作为壁纸|
|...|...|


在终端中运行这条命令，给sh脚本添加执行权限
```bash
sudo chmod +x ./RUNME.sh
```
到这里，你可以在终端中运行

```bash
./RUNME.sh
```
来更换壁纸


## 2 开机运行程序
如果你不想程序每次在开机时运行，可以省略这一步，并把程序的第30行：
```python
time.sleep(5)
```
删除。程序在这里暂停5秒是为了保证开机后有足够的时间连上网，否则程序无法下载图片，会报错。


### 2.1安装 启动应用程序
在终端中执行下面的命令安装启动应用程序：
```bash
sudo apt install gnome-startup-applications
``` 

打开启动应用程序，点击添加，第二栏命令通过点击右边的“浏览”选择RUNME.sh脚本文件。第一栏，第三栏自己想怎么写就怎么写。


******
# 程序实现思路

思路很简单。如果想修改程序，实现其他功能的，可以看看这部分内容。

## 1 主程序
### 1.1 获取Bing背景图片：
通过这个api：[http://bingw.jasonzeng.dev](http://bingw.jasonzeng.dev) 获取bing的背景图片。

程序中用到了api的两个参数：resolution分辨率和index序号。resolution=UHD表示高清分辨率，也可以为1920x1080等，index=0表示今天的图片，index=1表示昨天的图片，以此类推。index也可以是random，表示随机的图片。

通过python的requests库获取图片，保存到本地，大致过程如下：
```python
url = "http://bingw.jasonzeng.dev?resolution=UHD&index=" + sys.argv[1]
picturePath = "/path/to/project/picture/background.jpg"
response = requests.get(url)
with open(picturePath, "wb") as img:
   img.write(response.content)
```
### 1.2 设置壁纸

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
## 2 RUNME.sh脚本
脚本的主要作用是读取配置文件`config.yml`,给主程序传递api的index参数值和项目的路径。
