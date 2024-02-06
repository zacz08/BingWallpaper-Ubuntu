import time
import sys
import os
import requests
import hashlib
url = "http://bingw.jasonzeng.dev?resolution=UHD&index="

def getImg(url):
    response = requests.get(url)
    return response.content

# Check whether the image obtained from the api is already exists locally
def compare(data):
    with open(picturePath,"rb") as f:
        hash_existed = hashlib.md5(f.read()).hexdigest()
        hash_new = hashlib.md5(data).hexdigest()
        return hash_new == hash_existed

# set the local picture in /picture folder as the wallpaper
def setWallpaper(picPath): 
    setCommand = "gsettings set org.gnome.desktop.background picture-uri file:///{}".format(picPath)
    os.system(setCommand)
    notify = 'notify-send "my bingWallpaper" "Wallpaper Updated Successfully"'
    os.system(notify)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        notify = 'notify-send "my bingWallpaper" "Arguement Error!"'
        os.system(notify)
        sys.exit()
    time.sleep(5) # wait for 5s to connect to the internet
    try:
        # argv[1] is the project path set in config.yml
        picturePath = sys.argv[1] + '/picture/background.jpg'
        
        # splice a complete URL with argv[2] (index, number or ramdom)
        img_url = url + sys.argv[2]

        img_data = getImg(img_url)
        if not compare(img_data):
            with open(picturePath, 'wb') as img:
                img.write(img_data)
            setWallpaper(picturePath)
    except Exception as e:
        notify = 'notify-send "my bingWallpaper" "{}"'.format(str(e))
        os.system(notify)
