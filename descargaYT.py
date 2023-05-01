from flask import Flask, render_template, request, send_file
from pyngrok import ngrok
import json
import os
import urllib.request
import pytube
from pytube.__main__ import YouTube

app = Flask(__name__)

@app.route('/')
def index():
    return 'Hola, Mundo!'

@app.route('/playlist')
def playlist():
    # leer archivo JSON con información de la lista de reproducción
    with open('playlist.json', 'r') as f:
        playlist = json.load(f)

    # ejemplo de diccionario
    dict_videos = playlist

    # crear lista HTML
    list_html = '<ul>'
    for video in dict_videos['items']:
        list_html += f'<li><a href="{video["url"]}"><img src="{video["thumbnailUrl"]}" alt="{video["title"]}">{video["title"]}</a> <a href="/download/{video["id"]}">Descargar</a></li>'
    list_html += '</ul>'

    # mostrar lista HTML
    return list_html

@app.route('/download/<video_id>')
def download(video_id):
    # buscar el video correspondiente al ID en la lista de reproducción
    with open('playlist.json', 'r') as f:
        playlist = json.load(f)
    video = next((v for v in playlist['items'] if v['id'] == video_id), None)
    if video is None:
        return 'Video no encontrado'

    # crear una carpeta para guardar los videos si no existe
    if not os.path.exists('videos'):
        os.makedirs('videos')

    # descargar el video
    url = video['url']
    yt = pytube.YouTube(url)
    # comprobar si el video está disponible para descargar
    if not yt.streams:
        return f'El video {video_id} no está disponible para descargar.'
        
    stream = yt.streams.get_highest_resolution()
    finished = stream.download()
    print('Download is complete') 

# Iniciar el túnel con Ngrok
public_url = ngrok.connect(5000).public_url

# Mostrar la URL en la consola
print('El servidor Flask está disponible en la siguiente URL:')
print(public_url)

if __name__ == '__main__':
    app.run()



