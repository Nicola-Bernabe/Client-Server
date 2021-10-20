# Same thing than the 'server' Dockerfile.
FROM python:latest
ADD client_docker.py /client/
COPY . .
WORKDIR /client/
#RUN pip install numpy
RUN pip install websockets
EXPOSE 8000

