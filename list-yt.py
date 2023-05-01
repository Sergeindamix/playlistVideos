
from flask import Flask, render_template, request
from pyngrok import ngrok
import json
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
        list_html += f'<li><a href="{video["url"]}"><img src="{video["thumbnailUrl"]}" alt="{video["title"]}">{video["title"]}</a></li>'
    list_html += '</ul>'

    # mostrar lista HTML
    return list_html






# Iniciar el túnel con Ngrok
public_url = ngrok.connect(5000).public_url

# Mostrar la URL en la consola
print('El servidor Flask está disponible en la siguiente URL:')
print(public_url)
if __name__ == '__main__':
    app.run()
