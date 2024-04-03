FROM ubuntu:20.04
VOLUME /data
ENV DEBIAN_FRONTEND noninteractive

# Update and install packages
RUN apt-get update && \
  apt-get upgrade -y   && \
  apt-get install -y sudo gnupg2 curl openssh-server nano iproute2 apt-transport-https git wget

# Install VS Code
RUN wget -qO- https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > packages.microsoft.gpg && \
  sudo install -D -o root -g root -m 644 packages.microsoft.gpg /etc/apt/keyrings/packages.microsoft.gpg && \
  sudo sh -c 'echo "deb [arch=amd64,arm64,armhf signed-by=/etc/apt/keyrings/packages.microsoft.gpg] https://packages.microsoft.com/repos/code stable main" > /etc/apt/sources.list.d/vscode.list' && \
  rm -f packages.microsoft.gpg && \
  sudo apt update && \
  sudo apt install -y code

# Set up configuration for SSH
RUN mkdir /var/run/sshd && \
  sed -i 's/#Port 22/Port 2202/' /etc/ssh/sshd_config && \
  echo 'AllowUsers dev' >> /etc/ssh/sshd_config && \
  sed 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' -i /etc/pam.d/sshd && \
  echo "export VISIBLE=now" >> /etc/profile

# Expose the SSH port (nano /etc/ssh/sshd_config) 
EXPOSE 2202

# Install Coral TPU USB config and python packages
RUN echo "deb https://packages.cloud.google.com/apt coral-edgetpu-stable main" | sudo tee /etc/apt/sources.list.d/coral-edgetpu.list && \
  curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -  && \
  sudo apt-get update  && \
  sudo apt-get install -y libedgetpu1-std && \
  sudo apt-get install -y python3-pip && \
  sudo apt-get install -y python3-pycoral

# Add dev user and set their password to dev (so they can SSH)
RUN useradd -rm -d /home/dev -s /bin/bash -g root -G sudo -u 1001 -p "$(openssl passwd -1 dev)" dev

WORKDIR /server

COPY ./requirements.txt /server/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /server/requirements.txt

COPY ./app /server/app

# Setup shell run script (run sshd and fast api server)
RUN echo "#! /bin/bash" > /run.sh && \
  echo "/usr/sbin/sshd -D &" >> /run.sh && \
  echo "cd /server" >> /run.sh && \
  echo "uvicorn app.main:app --host 0.0.0.0 --port 9090" >> /run.sh && \
  echo "while true; do sleep 1; done"  >> /run.sh && \
  chmod +x /run.sh

#CMD ["/bin/bash"]
CMD ["/run.sh"]