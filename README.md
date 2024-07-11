# Introduction

This project is to obtain the background image of bing and set it as the wallpaper of ubuntu 20.04/22.04


*****

# Getting Started

## 0 Preapre the Environment
### 0.1 Install python3
```bash
sudo apt install python3
```

### 0.2 Install pip3
```bash
sudo apt install python3-pip
```
### 0.3 Install required libraries
```bash
pip install requests
pip install hashlib
```

## 1 Modify Config file

Open ``config.yml`` file and change ``path`` to your work path, change ``mode`` as needed

|mode|intro|
|:---:|:---:|
|random|Random pictures|
|0|Today's picture|
|1|Yesterday's picture|
|...|...|


Add execution permission to RUNME.sh
```bash
sudo chmod +x RUNME.sh
```
Now, you can change the wallpaper by running:

```bash
./RUNME.sh
```


## 2 Automatically run programs at boot
Dismiss this step if you don't want to make the script auto run when system boot, and comment out folling code in main.py
```python
time.sleep(5)
```
The above code is to wait for system to connect to the Interenet after booting.


### 2.1 Install Requirements
```bash
sudo apt install gnome-startup-applications
``` 

### 2.2 Set Auto Run
Open the startup application, click Add, and select the RUNME.sh script file by clicking "Browse" on the right in the second column of commands. 
Fill in the first and third columns as needed.
