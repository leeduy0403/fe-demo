from flask import Flask, redirect, url_for, request, jsonify, Response
# from flask_mqtt import Mqtt
from flask_cors import CORS
from ultralytics import YOLO
import cv2
 
# Initializing flask app
app = Flask(__name__)
CORS(app)

# app.config['MQTT_BROKEN_URL'] = 'mqtt.ohstem.vn'
# app.config['MQTT_BROKER_PORT'] = 1883
# app.config['MQTT_USERNAME'] = 'ltbxq623'
# app.config['MQTT_PASSWORD'] = ''
# app.config['MQTT_KEEPALIVE'] = 5
# app.config['MQTT_TLS_ENABLED'] = False 

# topic = '/flask/mqtt'

# mqtt_client = Mqtt(app)

# @mqtt_client.on_connect()
# def handle_connect(client, userdata, flags, rc):
#    if rc == 0:
#        print('Connected successfully')
#        mqtt_client.subscribe(topic) # subscribe topic
#    else:
#        print('Bad connection. Code:', rc)
    
# @mqtt_client.on_message()
# def handle_mqtt_message(client, userdata, message):
#    data = dict(
#        topic=message.topic,
#        payload=message.payload.decode()
#   )
#    print('Received message on topic: {topic} with payload: {payload}'.format(**data))
 
 
# # Route for seeing a data
# @app.route('/publish', methods=['POST'])
# def publish_message():
#    request_data = request.get_json()
#    publish_result = mqtt_client.publish(request_data['topic'], request_data['msg'])
#    return jsonify({'code': publish_result[0]})

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
    app.run(debug=True)