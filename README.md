# Load Movement Detection

This Repository contains an implementation of a motion detection system designed to watch the load of a vehicle and identify possible accidents by evaluating the change that has occurred between frames. When a potential accident is detected, the last frame -annotated with information about the detection and a bounding box indicating the most significant detected movement- is sent in a POST request, the body of which also contains additional information about the incident. Finally, during the specified delay after a successful detection, a buzzer will sound to notify the driver.

### Requirements

For the execution of the code a RaspberryPi 4b or 5 is required (older versions will most likely not cause problems). A usb camera is essential for frame capturing and a buzzer connected to GPIO pin 17 is also necessary for the notification function.

For receiving and storing the data, the backend will have to accept the mentioned POST request, that is created with the following command:
```
requests.post(backend_url,files={'image':open("potential_accident"+str(t)+".jpg","rb")},data={'time':time.strftime("%d_%m_%Y_%H_%M_%S"),'change_percentage':round(avg_percentage_changed,2)})
```

The body of the request contains 1 file named 'image' -the recorded frame-, and 2 data entries, named 'time' and 'change_percentage' that specify the time of detection and the detected change between frames. The timestamp is returned in the form day_month_year_hour_minute_second.

### Parameter Configuration
The necessary parameters can be configured through the config.yaml file:
```
backend_url: "http://192.168.1.5:5000/upload"  #The url where the POST request is sent
detection_threshold: 10                        #Threshold above which the system assumes there might have been an accident
delay_after_detection_ms: 1000                 #Delay between detections, to suppress multiple entries. This is also the duration of the sound of the buzzer
usb_cam_id: "/dev/video0"                      #Name of usb device-used only if use_usb==1
```
### Included Files

In the accident_detection_src_request folder there is the python source code and the config folder, which contains the file with the parameters mentioned above. In [this](https://drive.google.com/file/d/1P68amWxpSDq-yTv6jgweaRRCF5SWlVkf/view?usp=sharing) link there is a .tar file that can be used to load the application's docker image like this:
```
sudo docker load < accident_detection_request_final.tar
```
The resulting image can be run as shown here:
```
sudo docker run --privileged --network="host" -v $(pwd)/config:/config accident_detection_request_final
```
$(pwd)/config assumes that the config folder in which the configuration file is located is inside the directory where the above command is executed. Of course the path can be adapted.
### Running from Source

For the application to be run from source, some packages will need to be installed with pip, running the following:
```
pip3 install opencv-python-headless numpy PyYAML gpiozero requests
```
The code was tested using python 3.9.2, however other versions that support these packages are unlikely to cause problems. The picamera2 interface that is necessary comes preinstalled for systems released after September 2022.
