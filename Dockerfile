FROM python:3.8
MAINTAINER "ahri"<ahriknow@ahriknow.cn>
RUN apt update -y && apt install tesseract-ocr=4.0.0-2 -y
ADD app.py /project/app.py
ADD requirements.txt /project/requirements.txt
COPY traineddata/* /usr/share/tesseract-ocr/4.00/tessdata/
COPY pip.conf /etc/pip.conf
WORKDIR /project
RUN pip3 install --no-cache-dir -r requirements.txt
EXPOSE 9000
ENTRYPOINT ["gunicorn", "-w", "2", "-b", "0.0.0.0:9000", "app:app"]
