FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    gnupg \
    && wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update && apt-get install -y \
    google-chrome-stable \
    && wget -O /tmp/chromedriver.zip https://chromedriver.storage.googleapis.com/98.0.4758.48/chromedriver_linux64.zip \
    && unzip /tmp/chromedriver.zip -d /usr/bin/ \
    && rm /tmp/chromedriver.zip \
    && chmod +x /usr/bin/chromedriver

RUN mkdir /src
WORKDIR /src
ADD . /src
RUN pip install -r requirements.txt

EXPOSE 8000
CMD ["python","API/main_docker.py"]

# Error en dockerfile

# => CACHED [ 1/11] FROM docker.io/library/python:3.11-slim@sha256:6d2502238109c929569ae99355e28890c438cb11bc88ef02cd189c173b3db07c                                                        0.0s 
# => [internal] load build context                                                                                                                                                         2.0s 
# => => transferring context: 109.31kB                                                                                                                                                     0.4s 
# => [ 2/11] RUN apt-get update && apt-get install -y wget gnupg unzip                                                                                                                   132.5s 
# => [ 3/11] RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -                                                                                        6.4s 
# => [ 4/11] RUN echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list                                                         4.7s 
# => [ 5/11] RUN apt-get update && apt-get install -y google-chrome-stable                                                                                                              1364.8s 
# => ERROR [ 6/11] RUN wget -O /tmp/chromedriver.zip https://chromedriver.storage.googleapis.com/{124.0.6367.201}/chromedriver_linux64.zip                                                 5.6s 
# ------
# > [ 6/11] RUN wget -O /tmp/chromedriver.zip https://chromedriver.storage.googleapis.com/{124.0.6367.201}/chromedriver_linux64.zip:
# 4.213 --2024-05-13 15:25:30--  https://chromedriver.storage.googleapis.com/%7B124.0.6367.201%7D/chromedriver_linux64.zip
# 4.225 Resolving chromedriver.storage.googleapis.com (chromedriver.storage.googleapis.com)... 172.217.168.187, 216.58.209.91, 142.250.184.187, ...
# 4.282 Connecting to chromedriver.storage.googleapis.com (chromedriver.storage.googleapis.com)|172.217.168.187|:443... connected.
# 4.402 HTTP request sent, awaiting response... 404 Not Found
# 4.542 2024-05-13 15:25:31 ERROR 404: Not Found.
# 4.542
# ------
# dockerfile:7
# 5 |     RUN echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list
# 6 |     RUN apt-get update && apt-get install -y google-chrome-stable
# 7 | >>> RUN wget -O /tmp/chromedriver.zip https://chromedriver.storage.googleapis.com/{124.0.6367.201}/chromedriver_linux64.zip
# 8 |     RUN unzip /tmp/chromedriver.zip -d /usr/local/bin/
# 9 |
# --------------------
# ERROR: failed to solve: process "/bin/sh -c wget -O /tmp/chromedriver.zip https://chromedriver.storage.googleapis.com/{124.0.6367.201}/chromedriver_linux64.zip" did not complete successfully: exit code: 8