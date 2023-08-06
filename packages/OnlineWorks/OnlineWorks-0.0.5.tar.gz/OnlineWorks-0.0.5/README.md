# OnlineWorks

This is a simple python module for performing many online tasks
&nbsp;
# Installation
To install this libarary, you have to run these commands on your cmd or powershell
```
pip install OnlineWorks
```
Thats it for installation :)
# Quick Start Guide

```
import OnlineTasks # Not OnlineWorks
import OnlineTasks.Nasa as Nasa
import OnlineTasks.Whatsapp as whatsapp

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

# To get the title of a website
title = OnlineTasks.fetch_title('https://youtube.com')
print(title)

# To search anything in google

# It will open the browser and automatically search on google!
# Also, it will return info about the topic
# If there is not adat avaliable
# It will return None.

result = OnlineTasks.search('Carryminati')
print(result)

# To get corona info according to the country
Data = OnlineTasks.get_corona_info(Country='india')
deaths = Data['deaths']
cases = Data['cases']
recovered = Data['recovered']

# You can send email
# Disable the less secure apps in your gmail

OnlineTasks.SendEmail(
    email='your-email@example.com', 
    password='your-password', 
    to='whom-you-want-to-send-email@example.com', 
    subject='Example Subject', 
    body='Example Message'
)

# To open any place in google maps!
OnlineTasks.OpenPlaceInGoogleMaps(Place='india')

# To get your city, state and country where you are living!

# Step 1: Register in https://ipgeolocation.abstractapi.com
# Step 2: Get your api key
# Step 3: Give your api key in the parameter 'api_key'

OnlineTasks.get_location(api_key='your-api-key')

# You can get info of a solar body
Data = Nasa.SolarBodies('earth') # Returns the information about a solar body
mass = Data['mass'] # The mass of earth
gravity = Data['gravity'] # The gravity of earth
velocity = Data['escape_velocity'] # The escape velocity of earth
density = Data['density'] # The desnsity of earth
print(mass, gravity, velocity, density)

# To send a whatsapp message to a number
# The 'time_hour' parameter is that on which hour you want to send the message, it must be int
# The 'time_min' parameter is that on which minute you want to send the message, it must be int
# It will open up your browser and automaticallly send the message, so you need to be logged in to whatsapp web.
# If you minimize the browser, this function will not work!

whatsapp.send_whatsapp_message('phone_number_you_want_to_send_to_with_country_code', 'Your message here', time_hour=12, time_min=59)
```
Whats new in the latest release, 0.0.5?
You can send a whatsapp message to group!
```
import OnlineTasks.Whatsapp as whatsapp
whatsapp.send_whatsapp_message_to_group(
    group_id='type-the-group's-id-here',
    message='Your message here',
    time_hour=12, # The hour you want to send the message
    time_min=34 # The minute you want to send the message
)
```