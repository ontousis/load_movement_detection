# Load Movement Detection

This Repository contains an implementation of a motion detection system designed to watch the load of a vehicle and identify possible accidents by evaluating the change that has occurred between frames. When a potential accident is detected, the last frame -annotated with information about the detection and a bounding box indicating the most significant detected movement- is uploaded on a minio bucket and a record with the incident's time, percentage of change between frames and a url pointing to the uploaded image is written in a MongoDB database. Also, during the specified delay after a successful detection, a buzzer will sound to notify the driver.

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
delay_after_detection_ms: 500                  #Delay between detections, to suppress multiple entries. This is also the duration of the sound of the buzzer
```
### Included Files

In the accident_detection_src folder there is the python source code, the Dockerfile needed to create the docker image and the config folder, which contains the file with the parameters mentioned above. In the following link: https://drive.google.com/file/d/1aBhVsQxf5fJ-5GVKTBiL-rBq6njfdsM_/view?usp=sharing there is a .tar file that can be used to obtain a preconstructed image of the application. Once the accident_detection.tar is downloaded, the image can be loaded as follows:
```
sudo docker load < accident_detection.tar
```
The application can be run as seen below:
```
sudo docker run --device /dev/video0 --network="host" -v $(pwd)/config:/config accident_detection
```
$(pwd)/config assumes that the config folder with the configuration file is in the directory where the above commands are executed. Of course the path can be adapted. --device /dev/video0 is used so that we can have access to the host's camera (assuming it is properly configured).

### Running from Source

For the application to be run directly from source, some packages will need to be installed with pip, running the following:
```
pip3 install opencv-python-headless numpy minio pymongo PyYAML gpiozero
```
The code was tested using python 3.10, however other versions that support these packages are unlikely to cause problems.
