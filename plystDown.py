import os
app = Flask(__name__)
@app.route('/playlist')
def playlist():
    video_dir = '/content/drive/MyDrive/Videos'
    video_files = [f for f in os.listdir(video_dir) if f.endswith('.mp4')]
    playlist = '\n'.join([f'<a href="/play/{os.path.splitext(f)[0]}">{f}</a>' for f in video_files])
    return f'<html><body>{playlist}</body></html>'

@app.route('/play/<string:video_id>')
def play(video_id):
    video_path = f'/content/drive/MyDrive/Videos/{video_id}.mp4'
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
# Iniciar el túnel con Ngrok
public_url = ngrok.connect(5000).public_url

# Mostrar la URL en la consola
print('El servidor Flask está disponible en la siguiente URL:')
print(public_url)

if __name__ == '__main__':
    app.run()