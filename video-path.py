from pyngrok import ngrok

video_path = '/content/drive/MyDrive/01/Videos/1.mp4'
from flask import Flask, Response
import cv2

app = Flask(__name__)

@app.route('/video_feed')
def video_feed():
    # Replace the video path with your own video file path
    
    video = cv2.VideoCapture(video_path)

    def generate():
        while True:
            success, image = video.read()
            if not success:
                break
            ret, jpeg = cv2.imencode('.jpg', image)
            frame = jpeg.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    return '<html><body><img src="/video_feed"></body></html>'

# Iniciar el túnel con Ngrok
public_url = ngrok.connect(5000).public_url

# Mostrar la URL en la consola
print('El servidor Flask está disponible en la siguiente URL:')
print(public_url)

if __name__ == '__main__':
    app.run()
