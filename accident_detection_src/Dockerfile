FROM python:3.10

ADD acc_det_cv_request_new.py .

RUN apt-get update && apt -y upgrade

RUN apt-get install -y python3-pip
RUN apt-get clean

RUN apt install -y libcap-dev

RUN pip install gpiozero opencv-python-headless numpy minio pymongo PyYAML

RUN apt-get update -y && apt-get upgrade -y

RUN apt-get install -y libcap-dev libatlas-base-dev ffmpeg libopenjp2-7


RUN apt install -y libcamera-v4l2

RUN pip install --upgrade pip
RUN pip install wheel


RUN apt-get update && apt-get install -y \
    libboost-dev \
    libgnutls28-dev \
    libjpeg-dev \
    libtiff-dev \
    libyaml-dev \
    meson \
    ninja-build \
    python3-pip \
    git \
    cmake \
    build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN pip install jinja2 ply jinja2

#RUN apt-get update

RUN apt-get update && apt-get install -y libdrm-dev libfmt-dev libxrandr-dev

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y

RUN pip install requests
RUN pip install lgpio

CMD ["python3", "./acc_det_cv_request_new.py"]
