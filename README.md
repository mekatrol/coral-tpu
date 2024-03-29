# About repo

## Intro
A small repo to remind me how to set up Coral USB TPU on Raspberry PI.

Thanks to [JungLearnBot's RPI 5 repo](https://github.com/JungLearnBot/RPi5_yolov8).

## Set up fresh Rasberry PI 5

> Install Bookworm 64 bit with desktop (desktop needed for visualisation)

```bash
sudo apt update && sudo apt upgrade -y
  
sudo apt install code

```
see: [Get started with the USB Accelerator](https://coral.ai/docs/accelerator/get-started/)
```bash
bash
echo "deb https://packages.cloud.google.com/apt coral-edgetpu-stable main" | sudo tee /etc/apt/sources.list.d/coral-edgetpu.list

curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -

sudo apt-get update

sudo apt install libedgetpu1-std
```

- > If you already had the Coral TPU USB plugged in then remove and reinsert to connect drivers. Otherwise you will get errors like 'pycoral module not installed'.
```bash
wget https://github.com/oberluz/pycoral/releases/download/2.13.0/pycoral-2.13.0-cp311-cp311-linux_aarch64.whl

mkdir coral-dev

cd coral-dev

python3 -m venv .venv

source .venv/bin/activate

pip install Pillow

pip install ../pycoral-2.13.0-cp311-cp311-linux_aarch64.whl --no-deps

pip install tflite-runtime==2.14.0

git clone --recurse-submodules https://github.com/google-coral/pycoral

cd pycoral

python examples/classify_image.py --model test_data/mobilenet_v2_1.0_224_inat_bird_quant_edgetpu.tflite --labels test_data/inat_bird_labels.txt --input test_data/bird.bmp

```
