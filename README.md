# Load Movement Detection

This Repository contains an implementation of a motion detection system designed to watch the load of a vehicle and identify possible accidents by evaluating the change that has occurred between frames. When a potential accident is detected, the last frame -annotated with information about the detection and a bounding box indicating the most significant detected movement- is uploaded on a minio bucket and a record with the incident's time, percentage of change between frames and a url pointing to the uploaded image is written in a MongoDB database.

### Parameter Configuration
The necessary parameters can be configured through the config.yaml file:
```
minio_url: "127.0.0.1:9000" #minio server
minio_usr: "minioadmin"
minio_pwd: "minioadmin"
minio_bucket_name: "bucket001"
mongodb_server_ip: "127.0.0.1"
mongodb_server_port: 27017
mongodb_db_name: "potential_accident_record"
mongodb_collection_name: "accidents"
detection_threshold: 10
```
