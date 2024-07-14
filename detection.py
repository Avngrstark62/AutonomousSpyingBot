import cv2
import numpy as np
import requests
from io import BytesIO
from serial import Serial



def detect_object_properties(url):
  
    response = requests.get(url)
    if response.status_code == 200:
        image = np.asarray(bytearray(response.content), dtype="uint8")
        frame = cv2.imdecode(image, cv2.IMREAD_COLOR)
        
        
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        
        lower_color = np.array([50, 100, 100])
        upper_color = np.array([70, 255, 255]) #green ball
        mask = cv2.inRange(hsv, lower_color, upper_color)
        
    
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if contours:
            largest_contour = max(contours, key=cv2.contourArea)
            
       
            x, y, w, h = cv2.boundingRect(largest_contour)
            
          
            cx = x + w // 2
            size = w 
            
            return size, cx  
    

    return -1, -1  


url = "http://192.168.48.55:8080/shot.jpg"  # Replace with the URL provided by IP Webcam
ArduinoSerial=Serial('com12',9600,timeout=0.1) #change com according to arduino ide port
center_steer = 90 #change according to center value of steering
while True:
    size, cx = detect_object_properties(url)
    if size != -1 and cx != -1: 
        servoX = np.interp(cx, [0, 1920], [0,180 ]) #flip 180 and 0 if servo is reversed
        if(size>=1300): size=1300
        rear_power = np.interp(size, [0, 1300], [255,-255])
        print("Rear_power:", rear_power, " and Steering:", servoX)
        rear_power = int(rear_power)
        servoX = int(servoX)
        string='R{0:d}X{1:d}'.format(rear_power,servoX)
        ArduinoSerial.write(string.encode('utf-8'))    
    else:
        print("No object detected.")
        rear_power = int(0)
        servoX = int(center_steer)
        string='R{0:d}X{1:d}'.format(rear_power,servoX)
        ArduinoSerial.write(string.encode('utf-8'))  
    

    cv2.waitKey(200)