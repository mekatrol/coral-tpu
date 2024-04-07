import cv2
import requests
import json
import time 

def main(preview: bool):
  # Open video stream
  # TODO: Inject video stream through intefact to abstract from specific hardware
  cap = cv2.VideoCapture(0)

  # TODO: Pass in URL   
  url = "http://videoprocessor.lan:9090/detect"
  
  # Default font for writing to screen
  font = cv2.FONT_HERSHEY_SIMPLEX 
  
  # Last frame recorded time
  last_frame_time = time.time()
  
  # Main loop 
  while (cap.isOpened()):
    # Read a single frame
    ret, frame = cap.read()
    
    # If escape pressed or no more frames then exit loop
    key = cv2.waitKey(1)
    if key == 27 or not ret:
      break
        
    # Convert frame to in memory jpg file (as bytes)
    image_bytes = cv2.imencode('.jpg', frame)[1].tobytes()
    
    # Post the file to the image processing server
    r = requests.post(url, files={'file': image_bytes})
    
    # Response is json data
    response = json.loads(r.text)
    
    if response:
      detections = response['detections']
      for detection in detections:
        if(detection['label'] == 'person'):
          bbox = detection['boundingBox']
          xmin = bbox['xmin']
          ymin = bbox['ymin']
          xmax = bbox['xmax']
          ymax = bbox['ymax']
          cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (0, 255, 0), 3)
                    
    if preview:
      # Get current frame time
      current_frame_time = time.time() 

      # Calculate fps which is inverse delta time: 1 / (t2 - t1)
      fps = 1 / (current_frame_time - last_frame_time) 
    
      # We only display integer part
      fps = int(fps) 
      
      # As a string for display
      cv2.putText(frame, str(fps) + 'fps', (5, 50), font, 1, (0, 0, 255), 1, cv2.LINE_AA, False)           

      # Save to last frame time for next loop iteration    
      last_frame_time = current_frame_time 

      cv2.imshow("Frame", frame)      

  cap.release()
  cv2.destroyAllWindows()

if __name__ == "__main__":
    main(True)      