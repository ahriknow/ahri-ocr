# Ahri OCR

## Image optical character recognition. Multi language support.

## Build the image

```Dockerfile
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
```

## Run a container

```bash
docker container run --name ocr -p 80:9000 -d ahriknow/ocr:v20200326
```

-   `--name ocr` 容器名为 ocr
-   `-p 80:9000` 将容器 9000 端口映射到宿主机 80 端口
-   `-d` 后台运行
-   `ahriknow/ocr:v20200326` 镜像

## Python requirements.txt

```py
click==7.1.1
Flask==1.1.1
itsdangerous==1.1.0
Jinja2==2.11.1
MarkupSafe==1.1.1
Pillow==7.0.0
pytesseract==0.3.3
Werkzeug==1.0.0
```

## How to use

`POST http://ip:port/ocr`

| params | explain | other       |
| ------ | ------- | ----------- |
| file   | 图片    | form-data   |
| lang   | 语言    | chi_sim/eng |

## Powered By ahri 20200326
