import io

from PIL import Image

from fastapi import FastAPI, File, UploadFile, HTTPException, status
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.encoders import jsonable_encoder

from pycoral.adapters import common
from pycoral.adapters import detect
from pycoral.utils.dataset import read_label_file
from pycoral.utils.edgetpu import make_interpreter

app = FastAPI()

labels = read_label_file('/server/app/models/coco_labels.txt')
interpreter = make_interpreter('/server/app/models/ssd_mobilenet_v2_coco_quant_postprocess_edgetpu.tflite')
interpreter.allocate_tensors()

@app.post('/detect')
async def upload(file: UploadFile = File(...)):
    try:
        contents = await file.read()           
        image = Image.open(io.BytesIO(contents))
        _, scale = common.set_resized_input(interpreter, image.size, lambda size: image.resize(size, Image.LANCZOS))
        
        interpreter.invoke()
        objs = detect.get_objects(interpreter, 0.4, scale)
        
        reponse = {}
        reponse["detections"] = []
        if objs:
            for obj in objs:
                detection = {}
                detection["label"] = labels.get(obj.id, obj.id)
                detection["labelId"] = obj.id
                detection["boundingBox"] = {}
                detection["boundingBox"]["xmin"] = obj.bbox.xmin
                detection["boundingBox"]["ymin"] = obj.bbox.ymin
                detection["boundingBox"]["xmax"] = obj.bbox.xmax
                detection["boundingBox"]["ymax"] = obj.bbox.ymax
                reponse["detections"].append(detection)

        json_compatible_item_data = jsonable_encoder(reponse)
        return JSONResponse(content=json_compatible_item_data)
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"{repr(e)}"
        )
    
    finally:
        await file.close()


@app.get('/')
async def main():
    content = '''
    <body>
    <form action='/detect' enctype='multipart/form-data' method='post'>
    <input name='file' type='file'>
    <input type='submit'>
    </form>
    </body>
    '''
    return HTMLResponse(content=content)


# python3 -m uvicorn main:app --reload --host 0.0.0.0 --port 9090