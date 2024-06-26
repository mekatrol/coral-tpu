# About repo

## Intro

A small repo to remind me how to set up Coral USB TPU on Raspberry PI.

Four sets of instructions:

1. Ubuntu under docker with python 3.9
2. C++ for tensorflow 2.4.2
3. C++ / WHL for tensorflow 2.16.1
4. PyCoral (Thanks to [JungLearnBot's RPI 5 repo](https://github.com/JungLearnBot/RPi5_yolov8)).

For each option, it assumes:

## Set up fresh Rasberry PI 5

> Install Bookworm 64 bit with desktop (desktop needed for any visualisation, but following works with headless)

```bash
sudo apt update && sudo apt upgrade -y

sudo apt install -y git
```

## Docker install

>
> NOTE: DO NOT INSTALL libedgetpu.so on host Raspberry Pi, just in the Docker container! [see docker/pycoral/Dockerfile](https://github.com/mekatrol/coral-tpu/blob/main/docker/pycoral/Dockerfile)
>

### See [Install Docker Engine on Debian](https://docs.docker.com/engine/install/debian/) - Install using the apt repository

```bash
for pkg in docker.io docker-doc docker-compose podman-docker containerd runc; do sudo apt-get remove $pkg; done
```

```bash
# Add Docker's official GPG key:
sudo apt-get update
sudo apt-get install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/debian/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# Add the repository to Apt sources:
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/debian \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
```

```bash
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

```bash
sudo usermod -aG docker $USER
sudo reboot
```

```bash
# Test install
docker run hello-world

# Delete test image (say Y to both when prompted)
docker container prune
docker image prune -a
```

> Sometimes after a reboot it can take a couple of minutes for USB to start
> working and you will see this error until it does.  
> `ValueError: Failed to load delegate from libedgetpu.so.1`
> This can be resolved by adding a cron job to run a restart container script as follows.

Create file `/home/pi/test_container.py` (change to use your user name in place of 'pi')

```python
import requests
import subprocess

restart_container = False

try:
  response = requests.get('http://videoprocessor.lan:9090')
  if response.status_code != 200:
    restart_container = True
except:
  restart_container = True

if restart_container:
  subprocess.run('docker container restart image_processing_servershell=True)
```

```bash
crontab -e
```
> Add `*/1 * * * * /usr/bin/python /home/pi/test_container.py`
>
> Check logs `journalctl -u cron | grep test_container.py`

```bash
git clone https://github.com/mekatrol/coral-tpu.git
cd ~/coral-tpu/docker
docker build -t pycoral:1.0 . -f pycoral/Dockerfile
docker run --name pycoral --privileged -it pycoral:1.0 
```

```bash
# inside docker container
cd pycoral
./dep.sh
```

> Restart the container and wait a bit for USB to mount

```bash
cd pycoral
./classify.sh
./detect.sh

# On docker container, push to docker container host
# Copy generated bmp via ssh/   (change 'pi' to your user name and change 'videoprocessor.lan to your host / IP)'
scp ~/grace_hopper_processed.bmp pi@videoprocessor.lan:~/grace_hopper_processed.bmp

# From windows machine or similar, pull from docker container host
scp pi@videoprocessor.lan:~/grace_hopper_processed.bmp ./grace_hopper_processed.bmp 
```

## Build TF 2.4.2

```bash  
sudo apt install git
```

```bash
sudo apt install python3-dev python3-pip
```

```bash  
sudo apt install code
```

### Clone tensorflow (2.4.2)

```bash
git clone -b v2.4.2 --single-branch https://github.com/tensorflow/tensorflow.git tensorflow-2.4.2
```

### Set up bazel (3.7.2)

```bash
# Get binary
wget https://github.com/bazelbuild/bazel/releases/download/3.7.2/bazel-3.7.2-linux-arm64 -O ~/bazel/bazel-3.7.2

# Make execuable
chmod +x ~/bazel/bazel-3.7.2

# Confirm version
~/bazel/bazel-3.7.2 --version

# Create softlink from /usr/bin (adds to default path)
sudo ln -s ~/bazel/bazel-3.7.2 /usr/bin/bazel

# Check version again to confirm is in path
bazel --version
```

### Create virtual environment for tensorflow build

```bash
cd tensorflow-2.4.2
python3 -m venv .venv
source ./.venv/bin/activate
```

```bash
pip install -U pip numpy wheel
pip install -U keras_preprocessing --no-deps
```

### Configure build

```bash
python ./configure.py
```

- Make sure bazel detected:

> You have bazel 3.7.2 installed.

- Press enter to select default python location

> Please specify the location of python. [Default is /home/pi/tensorflow-2.4.2/.venv/bin/python]:

- Press enter to select default package location

> Please input the desired Python library path to use.  Default is [/home/pi/tensorflow-2.4.2/.venv/lib/python3.11/site-packages]

- No for ROCm support

> Do you wish to build TensorFlow with ROCm support? [y/N]:

- No for CUDA support

> Do you wish to build TensorFlow with CUDA support? [y/N]:

- No fo fresh release of clang

> Do you wish to download a fresh release of clang? (Experimental) [y/N]:

- Press enter for default bazel options

> Please specify optimization flags to use during compilation when bazel option "--config=opt" is specified [Default is -Wno-sign-compare]:

- No for Android builds

> Would you like to interactively configure ./WORKSPACE for Android builds? [y/N]:
> Next steps taken from site [Tensorflow Build From Source](https://www.tensorflow.org/install/source)
>

#### Result should be similar to

```bash
Preconfigured Bazel build configs. You can use any of the below by adding "--config=<>" to your build command. See .bazelrc for more details.
 --config=mkl          # Build with MKL support.
 --config=mkl_aarch64  # Build with oneDNN support for Aarch64.
 --config=monolithic   # Config for mostly static monolithic build.
 --config=ngraph       # Build with Intel nGraph support.
 --config=numa         # Build with NUMA support.
 --config=dynamic_kernels # (Experimental) Build kernels into separate shared objects.
 --config=v2           # Build TensorFlow 2.x instead of 1.x.
Preconfigured Bazel build configs to DISABLE default on features:
 --config=noaws        # Disable AWS S3 filesystem support.
 --config=nogcp        # Disable GCP support.
 --config=nohdfs       # Disable HDFS support.
 --config=nonccl       # Disable NVIDIA NCCL support.
```

### Build with bazel

#### Build lib file

```bash
bazel build -c opt //tensorflow/lite:libtensorflowlite.so
```

#### Output file

`~/tensorflow-2.4.2/bazel-bin/tensorflow/lite/libtensorflowlite.so`

## Build TF 2.16.1

### Clone tensorflow (2.16.1)

```bash
# Clone repo at latest release branch (2.16.1 at time of writing)
git clone -b v2.16.1 --single-branch https://github.com/tensorflow/tensorflow.git tensorflow-2.16.1
```

### Set up bazel (6.5.0)

>
> The bazel version needs is defined in the ~/tensorflow-2.16.1/.bazelversion file

```bash

# Get binary (6.5.0 at the time of writing)
wget https://github.com/bazelbuild/bazel/releases/download/6.5.0/bazel-6.5.0-linux-arm64 -O ~/bazel/bazel-6.5.0

# Make execuable
chmod +x ~/bazel/bazel-6.5.0

# Confirm version
~/bazel/bazel-6.5.0 --version

# Create softlink from /usr/bin (adds to default path)
sudo rm /usr/bin/bazel
sudo ln -s ~/bazel/bazel-6.5.0 /usr/bin/bazel

# Check version again to confirm is in path
bazel --version
```

### Create virtual environment for tensorflow build (2.16.1)

```bash
cd tensorflow-2.16.1
python3 -m venv .venv
source ./.venv/bin/activate
```

```bash
pip install -U pip numpy wheel
pip install -U keras_preprocessing --no-deps
```

### Configure the build

```bash
./configure
```

- Make sure bazel detected:

> You have bazel 6.5.0 installed.

- Press enter to select default python location

> Please specify the location of python. [Default is /home/pi/tensorflow-2.16.1/.venv/bin/python3]:

- Press enter to select default package location

> Please input the desired Python library path to use.  Default is [/home/pi/tensorflow-2.16.1/.venv/lib/python3.11/site-packages]

- No for ROCm support

> Do you wish to build TensorFlow with ROCm support? [y/N]:

- No for CUDA support

> Do you wish to build TensorFlow with CUDA support? [y/N]:

- No fo fresh release of clang

> Do you wish to download a fresh release of clang? (Experimental) [y/N]:

- Press enter for default bazel options

> Please specify optimization flags to use during compilation when bazel option "--config=opt" is specified [Default is -Wno-sign-compare]:

- No for Android builds

> Would you like to interactively configure ./WORKSPACE for Android builds? [y/N]:
> Next steps taken from site [Tensorflow Build From Source](https://www.tensorflow.org/install/source)
>

#### Result should be similar to (#2)

```bash
Preconfigured Bazel build configs. You can use any of the below by adding "--config=<>" to your build command. See .bazelrc for more details.
 --config=mkl          # Build with MKL support.
 --config=mkl_aarch64  # Build with oneDNN and Compute Library for the Arm Architecture (ACL).
 --config=monolithic   # Config for mostly static monolithic build.
 --config=numa         # Build with NUMA support.
 --config=dynamic_kernels # (Experimental) Build kernels into separate shared objects.
 --config=v1           # Build with TensorFlow 1 API instead of TF 2 API.
Preconfigured Bazel build configs to DISABLE default on features:
 --config=nogcp        # Disable GCP support.
 --config=nonccl       # Disable NVIDIA NCCL support.
Configuration finished
```

### Build TPU version with bazel

```bash
/home/pi/tensorflow-2.16.1/tensorflow/lite/tools/pip_package/build_pip_package_with_bazel.sh
```

> OR

```bash
bazel build -c opt //tensorflow/lite:libtensorflowlite.so
```

#### This should produce the library file

```bash
~/tensorflow-2.16.1/tensorflow/lite/tools/pip_package/gen/tflite_pip/python3/dist/tflite_runtime-2.16.1-cp311-cp311-linux_aarch64.whl
```

> OR

```bash
~/tensorflow-2.16.1/bazel-bin/tensorflow/lite/libtensorflowlite.so
```

## Python

```bash
sudo apt update && sudo apt upgrade -y
```

```bash  
sudo apt install code
```

see: [Get started with the USB Accelerator](https://coral.ai/docs/accelerator/get-started/)

```bash
echo "deb https://packages.cloud.google.com/apt coral-edgetpu-stable main" | sudo tee /etc/apt/sources.list.d/coral-edgetpu.list
```

```bash
curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -
```

```bash
sudo apt-get update
```

```bash
sudo apt install libedgetpu1-std
```

- > If you already had the Coral TPU USB plugged in then remove and reinsert to connect drivers. Otherwise you will get errors like 'pycoral module not installed'.

```bash
wget https://github.com/oberluz/pycoral/releases/download/2.13.0/pycoral-2.13.0-cp311-cp311-linux_aarch64.whl
```

```bash
mkdir coral-dev
cd coral-dev
```

```bash
python3 -m venv .venv
source .venv/bin/activate
```

```bash
pip install Pillow
pip install ../pycoral-2.13.0-cp311-cp311-linux_aarch64.whl --no-deps
pip install tflite-runtime==2.14.0
```

```bash
git clone --recurse-submodules https://github.com/google-coral/pycoral
```

```bash
cd pycoral
```

```bash
python examples/classify_image.py --model test_data/mobilenet_v2_1.0_224_inat_bird_quant_edgetpu.tflite --labels test_data/inat_bird_labels.txt --input test_data/bird.bmp
```
