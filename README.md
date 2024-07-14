# Load Movement Detection

This Repository contains an implementation of a motion detection system designed to watch the load of a vehicle and identify possible accidents by evaluating the change that has occurred between frames. When a potential accident is detected, the last frame -annotated with information about the detection and a bounding box indicating the most significant detected movement- is uploaded on a minio bucket and a record with the incident's time, percentage of change between frames and a url pointing to the uploaded image is written in a MongoDB database.

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
delay_after_detection_ms: 200                  #Delay between detections, to suppress multiple entries, should be set lower if these entries are not a concern
```
