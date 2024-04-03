FROM ubuntu:20.04
VOLUME /data

RUN apt-get update 
RUN apt-get upgrade -y  
RUN apt-get install -y sudo gnupg2 curl git usbutils nano

RUN echo "deb https://packages.cloud.google.com/apt coral-edgetpu-stable main" | sudo tee /etc/apt/sources.list.d/coral-edgetpu.list
RUN curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add - 
RUN sudo apt-get update 
RUN sudo apt-get install -y libedgetpu1-std
RUN sudo apt-get install -y python3
RUN sudo apt-get install -y python3-pycoral

RUN git clone https://github.com/mekatrol/coral-tpu.git
RUN git clone https://github.com/google-coral/pycoral.git
RUN printf "bash examples/install_requirements.sh classify_image.py\nbash examples/install_requirements.sh detect_image.py\n" > pycoral/dep.sh
RUN chmod +x pycoral/dep.sh
RUN echo "python3 examples/classify_image.py --model test_data/mobilenet_v2_1.0_224_inat_bird_quant_edgetpu.tflite --labels test_data/inat_bird_labels.txt --input test_data/parrot.jpg" > pycoral/classify.sh
RUN chmod +x pycoral/classify.sh
RUN echo "python3 examples/detect_image.py --model test_data/ssd_mobilenet_v2_coco_quant_postprocess_edgetpu.tflite --labels test_data/coco_labels.txt --input test_data/grace_hopper.bmp  --output ${HOME}/grace_hopper_processed.bmp" > pycoral/detect.sh
RUN chmod +x pycoral/detect.sh

CMD ["/bin/bash"]