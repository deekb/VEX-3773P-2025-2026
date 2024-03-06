from flask import Flask, render_template, Response
import cv2
import io

app = Flask(__name__)
video_capture = cv2.VideoCapture(0)

def capture_image():
    global video_capture
    # Capture a single frame from the webcam
    success, frame = video_capture.read()
    
    if success:
        # Convert the frame to JPEG
        frame = cv2.resize(frame, (960, 544))
        ret, jpeg = cv2.imencode('.jpg', frame)
        if ret:
            return jpeg.tobytes()
    return None

# while True:
#     image = capture_image()
#     if image is not None:
#         cv2.imshow("test", image)
#         cv2.waitKey(1)

@app.route('/')
def index():
    image_data = capture_image()
    if image_data:
        return Response(image_data, mimetype='image/jpeg')
    else:
        return 'Error capturing image.'
if __name__ == '__main__':
    try:
        # Start the Flask web server
        app.run(host='0.0.0.0', port=5000, debug=True)
    finally:
        # Clean up resources
        video_capture.release()
