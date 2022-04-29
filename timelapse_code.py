import smtplib
from picamera import PiCamera
import os
from time import sleep
from email.message import EmailMessage
 
sleep(60) # Sleep so the user can replace the lid and place the camera before the timelapse starts
 
# Login information for sending email
gmail_user = "your email"
gmail_password = "your password"
 
# Create the container email message.
msg = EmailMessage()
msg['Subject'] = 'Your Timelapse'
msg['From'] = 'sending email'
msg['To'] = 'receiving email'
 
tlminutes = 1 #set this to the number of minutes to record
secondsinterval = 1 #number of seconds between each photo
fps = 30 #frames per second of the timelapse video
numphotos = int((tlminutes*60)/secondsinterval) #number of photos to take
print("number of photos to take = ", numphotos)
print(Started taking photos for your timelapse" ) 
# Declare camera and resolution
camera = PiCamera()
camera.resolution = (1024, 768)
# Clears out pictures of any past timelapse
os.system('rm /home/pi/Pictures/*.jpg') 
# Start taking pictures
for i in range(numphotos):
    
camera.capture('/home/pi/Pictures/image{0:06d}.jpg'.format(i))
    sleep(secondsinterval)

print("Done taking photos.")
print("Please standby as your timelapse video is created.")
# Delete any older timelapses
if os.path.exists("/home/pi/Videos/timelapse.mp4"):
    os.remove("/home/pi/Videos/timelapse.mp4")
    print("former timelapse deleted")
# Name of timelapse
fileName = "timelapse"
# Code for stitching pictures into video
os.system('ffmpeg -r {} -f image2 -s 1024x768 -nostats -loglevel 0 -pattern_type glob -i "/home/pi/Pictures/*.jpg" -vcodec libx264 -crf 25  -pix_fmt yuv420p /home/pi/Videos/{}.mp4'.format(fps, fileName))
print('Timelapse video is complete. Video saved as {}.mp4'.format(fileName))
 
# Allowing the program to read the file to be sent
file = '/home/pi/Videos/timelapse.mp4'
with open(file, 'rb') as fp:
    timelapse = fp.read()
   
# MIMEtype for the format and file type
mimetype = 'video/mp4'
maintype, subtype = mimetype.split('/', 1)
# Writing the message
msg.add_attachment(timelapse, maintype=maintype, subtype=subtype, filename=fileName)
 
# Sending the message
with smtplib.SMTP_SSL('smtp.gmail.com',465) as s:
    s.ehlo()
    s.login(gmail_user, gmail_password)
    s.send_message(msg)
    s.close()
 
print("Email sent!")
