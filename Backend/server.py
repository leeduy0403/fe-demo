from flask import Flask, redirect, url_for, request, jsonify, Response
from flask_mqtt import Mqtt
from flask_cors import CORS
from ultralytics import YOLO
import cv2
 
# Initializing flask app
app = Flask(__name__)
CORS(app)

################################
########## WEB APP #############
################################

app.config['MQTT_BROKER_URL'] = 'mqtt.ohstem.vn'
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_USERNAME'] = 'ltbxq623'
app.config['MQTT_PASSWORD'] = ''
app.config['MQTT_KEEPALIVE'] = 5
app.config['MQTT_TLS_ENABLED'] = False 

MQTT_USERNAME = 'ltbxq623'
TOPICS = [
    'V1', # temperature
    'V2', # humidity
    'V3' # light
    , 'V12'
    , 'V10'
]
MQTT_SUB = []
for t in TOPICS:
   topic = MQTT_USERNAME + '/feeds/' + t
   MQTT_SUB.append(topic)

MQTT_BULB = MQTT_USERNAME + '/feeds/V10'
MQTT_FAN = MQTT_USERNAME + '/feeds/V12'

mqtt_client = Mqtt(app)

@mqtt_client.on_connect()
def handle_connect(client, userdata, flags, rc):
   if rc == 0:
       print('Connected successfully')
       for topic in MQTT_SUB:
          mqtt_client.subscribe(topic) # subscribe topic
   else:
       print('Bad connection. Code:', rc)
    
class Env():
   def __init__(self, temperature=0, humidity=0, light=0):
       self.temperature = temperature
       self.humidity = humidity
       self.light = light

env = Env()
@mqtt_client.on_message()
def handle_mqtt_message(client, userdata, message):
   data = dict(
       topic=message.topic,
       payload=message.payload.decode()
  )
   print('Received message on topic: {topic} with payload: {payload}'.format(**data))
   if data['topic'] == MQTT_SUB[0]:
      env.temperature = data['payload']
   if data['topic'] == MQTT_SUB[1]:
      env.humidity = data['payload']
   if data['topic'] == MQTT_SUB[2]:
      env.light = data['payload']
   if data['topic'] == MQTT_SUB[3]:
      print(type(data['payload']), data['payload'])
   if data['topic'] == MQTT_SUB[4]:
      print(type(data['payload']), data['payload'])
 
# Route for seeing a data
@app.route('/env')
def get_env():
   return {'temperature': env.temperature,
           'humidity': env.humidity,
           'light': env.light}

@app.route('/fan')
def set_fan():
   speed = request.args.get('speed')
   mqtt_client.publish(MQTT_FAN, speed)
   return {'fan_speed' : speed}

@app.route('/bulb')
def set_bulb():
   signal = request.args.get('signal')
   mqtt_client.publish(MQTT_BULB, signal)
   return {'bulb_signal' : signal}

################################
########### YOLOv8 #############
################################

model = YOLO('best.pt')
video_capture = cv2.VideoCapture(0)

def warning(flag=False):
    return flag

def generate_frames():
    # Capture video from the webcam
    video_capture = cv2.VideoCapture(0)
    
    while True:
        # Read a frame from the video capture
        success, frame = video_capture.read()
        if not success:
            break

        # Perform object detection
        results = model.predict(source=frame)
        detections = results[0]

        # Draw bounding boxes and labels on the frame
        for detection in detections.boxes:
            x1, y1, x2, y2 = map(int, detection.xyxy[0])
            conf = detection.conf[0]
            cls = int(detection.cls[0])
            label = f"{model.names[cls]}: {conf:.2f}"
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
            if conf > 0.5:
                warning(True)

        # Encode the frame as JPEG
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        # Yield the frame in the proper format
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    video_capture.release()

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# Running app
if __name__ == '__main__':
    app.run(debug=True)