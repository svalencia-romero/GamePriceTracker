FROM python:3.11-slim
RUN mkdir /src
WORKDIR /src
ADD . /src
RUN pip install -r requirements.txt
EXPOSE 8000
CMD ["python","API/main_docker.py"]
