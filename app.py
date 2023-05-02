from flask import Flask, render_template, Response
from camera import VideoCamera
from pyngrok import ngrok
import os
from IPython.display import HTML, display

app = Flask(__name__)
@app.route('/')
def index():
    html = """
    <!DOCTYPE html>
    <html>
    <head>
      <title>My Generated HTML Page</title>
    </head>
    <body>
      <audio controls>
      {audio_html}<img src="data:image/jpeg;base64,{base64.b64encode(jpeg).decode()}">
      <source src="audio.ogg" type="audio/ogg">
      Your browser does not support the audio element.
      <audio controls>
    </body>
    </html>
    """ 
    return html


def gen(camera):
    while True:
        frame = camera.get_frame()
        if frame is not None:
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/playlist')
def playlist():
    video_dir = '/content/drive/MyDrive/01/Videos'
    video_files = [f for f in os.listdir(video_dir) if f.endswith('.mp4')]
    playlist = '\n'.join([f'<a href="/play/{os.path.splitext(f)[0]}">{f}</a>' for f in video_files])
    return f'<html><body>{playlist}</body></html>'

@app.route('/play/<string:video_id>')
def play(video_id):
    video_path = f'/content/drive/MyDrive/01/Videos/{video_id}.mp4'
    return f'''
    <html>
        <body>
            <h2>{video_id}</h2>
            <video width="800" height="600" controls>
                <source src="/video_feed/{video_id}" type="video/mp4">
            </video>
        </body>
    </html>
    '''
    
@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

# Iniciar el túnel con Ngrok
public_url = ngrok.connect(5000).public_url

# Mostrar la URL en la consola
print('El servidor Flask carpeta de videos en la siguiente URL:')
print(public_url + '/video_feed')
print('El servidor Flask playlist en la siguiente URL:')
print(public_url + '/playlist')

if __name__ == '__main__':
    app.run()
