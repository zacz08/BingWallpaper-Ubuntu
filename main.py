import time
import os
import requests
import hashlib
import random
picturePath = "/home/y/code/bingWallpaper/picture/background.jpg"
url = "http://bingw.jasonzeng.dev?resolution=UHD&index="
def randomImg():
    index = random.randint(0,100)
    rand_url = url + str(index)
    return rand_url

def getImg(url):
    response = requests.get(url)
    return response.content

def compare(data):
    with open(picturePath,"rb") as f:
        hash_existed = hashlib.md5(f.read()).hexdigest()
        hash_new = hashlib.md5(data).hexdigest()
        return hash_new == hash_existed

def setWallpaper():
    setCommand = "gsettings set org.gnome.desktop.background picture-uri file:///{}".format(picturePath)
    os.system(setCommand)
    notify = 'notify-send "my bingWallpaper" "Wallpaper Updated Successfully"'
    os.system(notify)

if __name__ == "__main__":
    time.sleep(5) 
    try:
        img_url = url + str(0)
        img_url = randomImg()
        img_data = getImg(img_url)
        if not compare(img_data):
            with open(picturePath, 'wb') as img:
                img.write(img_data)
            setWallpaper()
    except Exception as e:
        notify = 'notify-send "my bingWallpaper" "{}"'.format(str(e))
        os.system(notify)


