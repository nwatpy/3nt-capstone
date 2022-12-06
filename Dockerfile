FROM python:latest
LABEL "MAINTAINER"="NDWLM/PYBLOG"
WORKDIR /home/ubuntu
RUN pip install --upgrade pip
COPY pyblog/. ./
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 80
CMD [ "python3"]
