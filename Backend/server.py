from flask import Flask, redirect, url_for, request, jsonify, Response
from flask_mqtt import Mqtt
from flask_cors import CORS
from ultralytics import YOLO
import cv2
from flask_socketio import SocketIO
import eventlet

 
# Initializing flask app
eventlet.monkey_patch()

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

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
    'V3', # light
    'V13', # message
]
MQTT_SUB = []
for t in TOPICS:
   topic = MQTT_USERNAME + '/feeds/' + t
   MQTT_SUB.append(topic)

MQTT_BULB = MQTT_USERNAME + '/feeds/V10' # turn on/off the light bulb
MQTT_FAN = MQTT_USERNAME + '/feeds/V12' # change speed of the fan

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
   def __init__(self, temperature=0, humidity=0, light=0, message='Connected'):
       self.temperature = temperature
       self.humidity = humidity
       self.light = light
       self.message = message

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
      env.message = data['payload']

   # Emit the updated data to all connected WebSocket clients
   socketio.emit('update_data', {
       'temperature': env.temperature,
       'humidity': env.humidity,
       'light': env.light,
       'message': env.message
   })
 
# Route for seeing a data
@app.route('/env')
def get_env():
   print("Message", env.message)
   return {'temperature': env.temperature,
           'humidity': env.humidity,
           'light': env.light,
           'message': env.message}
    # return {
    #     'temperature': 26.0,
    #     'humidity': 49.5,
    #     'light': 24,
    #     'message': 'The light is off'
    # }

@app.route('/fan', methods=['POST'])
def set_fan():
   speed = request.args.get('speed')
   print(speed)
   mqtt_client.publish(MQTT_FAN, speed)
   return {'fan_speed' : speed}

@app.route('/bulb', methods=['POST'])
def set_bulb():
   signal = request.args.get('signal')
   print(signal)
   mqtt_client.publish(MQTT_BULB, signal)
   return {'bulb_signal' : signal}

################################
########### YOLOv8 #############
################################

model = YOLO('best.pt')
video_capture = cv2.VideoCapture(0)

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
    # app.run(debug=True, host='0.0.0.0', port=5000)
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)