FROM ubuntu:20.04
VOLUME /data

RUN apt-get update 
RUN apt-get upgrade -y  
RUN apt-get install -y sudo gnupg2 curl

RUN echo "deb https://packages.cloud.google.com/apt coral-edgetpu-stable main" | sudo tee /etc/apt/sources.list.d/coral-edgetpu.list
RUN curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add - 
RUN sudo apt-get update 
RUN sudo apt-get install -y libedgetpu1-std
# RUN sudo apt-get install -y python3.9
# RUN sudo ln -sfn /usr/bin/python3.9 /usr/bin/python3
# RUN sudo ln -s /usr/bin/python3.9 /usr/bin/python
RUN sudo apt-get install -y python3-pip
RUN sudo apt-get install -y python3-pycoral

WORKDIR /server

COPY ./requirements.txt /server/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /server/requirements.txt

COPY ./app /server/app

#CMD ["/bin/bash"]

# uvicorn app.main:app --host 0.0.0.0 --port 9090
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "9090"]