import time
import sys
import os
import requests
import hashlib
url = "http://bingw.jasonzeng.dev?resolution=UHD&index="

def getImg(url): #返回从api获取的内容，即图片的数据
    response = requests.get(url)
    return response.content

def compare(data): #比较从api获得的图片是否和本地已存在的图片相同
    with open(picturePath,"rb") as f:
        hash_existed = hashlib.md5(f.read()).hexdigest()
        hash_new = hashlib.md5(data).hexdigest()
        return hash_new == hash_existed

def setWallpaper(): #将本地的图片设为壁纸
    setCommand = "gsettings set org.gnome.desktop.background picture-uri file:///{}".format(picturePath)
    os.system(setCommand)
    notify = 'notify-send "my bingWallpaper" "Wallpaper Updated Successfully"'
    os.system(notify)

if __name__ == "__main__":
    if len(sys.argv) != 3: #参数错误
        notify = 'notify-send "my bingWallpaper" "Arguement Error!"'
        os.system(notify)
        sys.exit()
    #time.sleep(5) #确保开机后有足够时间连上网
    try:
        picturePath = sys.argv[1] + '/picture/background.jpg'#argv[1]为传入的项目路径
        img_url = url + sys.argv[2] #argv[2]为传入的index值，数字或者random
        img_data = getImg(img_url)
        if not compare(img_data):
            with open(picturePath, 'wb') as img:
                img.write(img_data)
            setWallpaper()
    except Exception as e:
        notify = 'notify-send "my bingWallpaper" "{}"'.format(str(e))
        os.system(notify)
