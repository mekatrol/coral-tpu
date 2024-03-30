# About repo

## Intro
A small repo to remind me how to set up Coral USB TPU on Raspberry PI.

Thanks to [JungLearnBot's RPI 5 repo](https://github.com/JungLearnBot/RPi5_yolov8).

# C++

## Set up fresh Rasberry PI 5

> Install Bookworm 64 bit with desktop (desktop needed for any visualisation, but following works with headless)

```bash
sudo apt update && sudo apt upgrade -y
```
```bash  
sudo apt install code
```
> Next steps taken from site [Tensorflow Build From Source](https://www.tensorflow.org/install/source)
> 

```bash
sudo apt install python3-dev python3-pip
```

```bash
pip install -U --user pip
```

```bash
sudo apt-get update && sudo apt-get install -y llvm-17 clang-17
```
```bash
cd ~/
mkdir  bazelisk
wget https://github.com/bazelbuild/bazelisk/releases/download/v1.19.0/bazelisk-linux-arm64 -O ~/bazelisk/bazelisk
```
```bash
chmod +x ~/bazelisk/bazelisk
```
```bash
sudo ln -s ~/bazelisk/bazelisk /usr/bin/bazel
```
```bash
bazel --version

```

```bash

```

# Python

## Set up fresh Rasberry PI 5

> Install Bookworm 64 bit with desktop (desktop needed for any visualisation, but following works with headless)

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
