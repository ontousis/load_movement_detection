FROM python:3.10

ADD acc_det_cv.py .

RUN pip3 install opencv-python-headless numpy minio pymongo PyYAML
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y

CMD ["python", "./acc_det_cv.py"]
