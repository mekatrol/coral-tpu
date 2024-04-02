from typing import Union

from PIL import Image
from fastapi import FastAPI
from pycoral.adapters import common
from pycoral.adapters import detect
from pycoral.utils.dataset import read_label_file
from pycoral.utils.edgetpu import make_interpreter

app = FastAPI()

labels = read_label_file('/server/app/models/coco_labels.txt')
interpreter = make_interpreter('/server/app/models/ssd_mobilenet_v2_coco_quant_postprocess_edgetpu.tflite')
interpreter.allocate_tensors()

image = Image.open('/server/app/data/grace_hopper.bmp')
_, scale = common.set_resized_input(interpreter, image.size, lambda size: image.resize(size, Image.LANCZOS))

interpreter.invoke()
objs = detect.get_objects(interpreter, 0.4, scale)

detected = ''
if not objs:
    detected = 'No objects detected'
else:
    detected = f'{objs}'

@app.get("/")
def read_root():
    return {"detect": detected}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}