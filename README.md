# Load Movement Detection

This Repository contains an implementation of a motion detection system designed to watch the load of a vehicle and identify possible accidents by evaluating the change that has occurred between frames. When a potential accident is detected, the last frame -annotated with information about the detection and a bounding box indicating the most significant detected movement- is sent to a specifiec url via a post request.

### Requirements

For the execution of the code a RaspberryPi 4b or 5 is required (older versions will most likely not cause problems, however there might be compatibility issues related to the Rpi camera with Operating Systems released before "Bullseye"). An Rpi camera or a usb camera is essential for frame capturing and a buzzer connected to GPIO pin 17 is also necessary for the notification function.

### Parameter Configuration
The necessary parameters can be configured through the config.yaml file:
```
backend_url: "http://192.168.1.5:5000/upload"  #The url where the POST request is sent
detection_threshold: 10                        #Threshold above which the system assumes there might have been an accident
delay_after_detection_ms: 1000                 #Delay between detections, to suppress multiple entries. This is also the duration of the sound of the buzzer
usb_cam_id: "/dev/video0"                      #Name of usb device-used only if use_usb==1
```
### Included Files

In the accident_detection_src folder there is the python source code and the config folder, which contains the file with the parameters mentioned above. In [this](https://drive.google.com/file/d/1vaXJ9ytIbQdkx6QYxqSN8CVukRSKq1E5/view?usp=sharing) link there is a .tar file that can be used to load the application's docker image like this:
```
sudo docker load < load_move_det_10_7_25.tar
```
The resulting image can be run as shown here:
```
sudo docker run --privileged --network="host" -v $(pwd)/config:/config load_move_det_10_7_25
```
$(pwd)/config assumes that the config folder in which the configuration file is located is inside the directory where the above command is executed. Of course the path can be adapted.
