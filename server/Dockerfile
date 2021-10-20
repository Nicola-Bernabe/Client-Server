# Just a remember, dockerfile must always start by importing the base image.
# We use the keyword 'FROM' to do that.
# In our example, we want to import the python image (from DockerHub).
# So, we write 'python' for the image name and 'latest' for the version.

#https://fastapi.tiangolo.com/pt/deployment/docker/
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

#FROM python:3.9.4-slim


#FROM python:latest
WORKDIR /server/
ADD server_docker.py //
ADD index.html //
COPY . .
EXPOSE 8000
RUN pip install uvicorn
RUN pip install fastapi
RUN pip install Jinja2
RUN pip install python-multipart
RUN pip install numpy
RUN pip install aiofiles
#CMD [ "python" , "server_docker.py"  ]



 


