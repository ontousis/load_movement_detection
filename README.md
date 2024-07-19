# Load Movement Detection

This Repository contains an implementation of a motion detection system designed to watch the load of a vehicle and identify possible accidents by evaluating the change that has occurred between frames. When a potential accident is detected, the last frame -annotated with information about the detection and a bounding box indicating the most significant detected movement- is uploaded on a minio bucket and a record with the incident's time, percentage of change between frames and a url pointing to the uploaded image is written in a MongoDB database. Also, during the specified delay after a successful detection, a buzzer will sound to notify the driver.

### Requirements

For the execution of the code a RaspberryPi 4b or 5 is required (older versions will most likely not cause problems). An Rpi camera or a usb camera is essential for frame capturing and a buzzer connected to GPIO pin 17 is also necessary for the notification function.

For storing the recorded incidents, a mongodb server will need to be setup, with its connection and naming parameters configured in the config.yaml file, as shown below. The application creates entries with 3 fields -Recorded frame URL, time of the incident and percentage of change detected-. Manual definition of the database entry format  is not necessary, since mongoDB will automatically store the provided data in the specified collection. If that collection does not exist, it will be automatically created. 

The frames recorded when apotential accident is detected are stored in a minio bucket having its parameters also described in the configuration file as shown in the following section.

### Parameter Configuration
The necessary parameters can be configured through the config.yaml file:
```
minio_url: "127.0.0.1:9000"                    #Minio server ip and port
minio_usr: "minioadmin"                        #Minio user
minio_pwd: "minioadmin"                        #Minio password
minio_bucket_name: "bucket001"                 #Bucket name
mongodb_server_ip: "127.0.0.1"                 #Ip for mongodb connection
mongodb_server_port: 27017                     #Port for mongodb connection 
mongodb_db_name: "potential_accident_record"   #Database name
mongodb_collection_name: "accidents"           #Name of collection in database
mongodb_username: "Admintst"                   #Database user
mongodb_password: "Admintst"                   #Password of database user
detection_threshold: 10                        #Threshold above which the system assumes there might have been an accident
delay_after_detection_ms: 1000                 #Delay between detections, to suppress multiple entries. This is also the duration of the sound of the buzzer
use_usb: 0                                     #0 for using raspberry camera, 1 for usb webcam
usb_cam_id: "/dev/video0"                      #Name of usb device-used only if use_usb==1
```
### Included Files

In the accident_detection_src folder there is the python source code and the config folder, which contains the file with the parameters mentioned above.

For the application to be run from source, some packages will need to be installed with pip, running the following:
```
pip3 install opencv-python-headless numpy minio pymongo PyYAML gpiozero
```
The code was tested using python 3.9.2, however other versions that support these packages are unlikely to cause problems. The picamera2 interface that is necessary comes preinstalled for systems released after September 2022.
