# OnlineWorks

This is a simple python module for performing many online tasks
Quick Start Guide:

```
import OnlineTasks # Not OnlineWorks

# This code will play a video on youtube

tube = OnlineTasks.Youtube()
tube.load('Carryminati')
tube.play()

# To get your public ip address
ip = OnlineTasks.get_ip_address()
print(ip)

# To open your mobile camera
# Follow the steps given below to open your mobile camera

# Step 1: Download and install the ip webcam app from the play store from your mobile
# Step 2: Open the ip webcam app, and then click on start server
# Step 3: Now, you will get an IPV4, so, write that on the argument 'ipwebcam_ip'
# Step 4: Call this function and then run
# Step 5: Then run and you will se your mobile camera on your computer!

OnlineTasks.open_mobile_camera('your-ip-webcam-ip-address')
```

Whats new in the latest release, 0.0.2?
```
# You can search on google
OnlineTasks.search('Carryminati')

# You can get the title of a website
title = OnlineTasks.fetch_title('https://youtube.com')
print(title)
```