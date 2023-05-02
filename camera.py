import cv2
from moviepy.video.io.VideoFileClip import VideoFileClip
import os
from pydub import AudioSegment
from IPython.display import HTML, display
import base64


VIDEO_DIR = '/content/drive/MyDrive/01/Videos'
VIDEO_FILES = [f for f in os.listdir(VIDEO_DIR) if f.endswith('.mp4')]
VIDEO_LIST = [os.path.join(VIDEO_DIR, f) for f in VIDEO_FILES]
AUDIO_DIR = '/content/playlistVideos'
if not os.path.exists(AUDIO_DIR):
    os.mkdir(AUDIO_DIR)
    

class VideoCamera(object):
    def __init__(self):
        self.video_list = VIDEO_LIST
        self.current_video = 0
        self.video_path = self.video_list[self.current_video]
        self.audio_path = os.path.join(AUDIO_DIR, f"audio_{self.current_video}.mp3")
        if not os.path.exists(self.audio_path):
            # Extraer y guardar el archivo de audio si aún no se ha hecho
            clip = VideoFileClip(self.video_path)
            audio = clip.audio
            audio.write_audiofile(self.audio_path, fps=44100)
        self.video = cv2.VideoCapture(self.video_path)
        self.audio = AudioSegment.from_file(self.audio_path)
        self.play_audio = True  # Agregar variable para controlar la reproducción de audio

    def __del__(self):
        self.video.release()

    def get_frame(self):
        success, image = self.video.read()
        if not success:
            # Si el video actual ha terminado, avanzar al siguiente video en la lista
            self.current_video += 1
            if self.current_video == len(self.video_list):
                # Si se ha reproducido todos los videos en la lista, regresar al primer video
                self.current_video = 0
            self.video_path = self.video_list[self.current_video]
            self.audio_path = os.path.join(AUDIO_DIR, f"audio_{self.current_video}.mp3")
            if not os.path.exists(self.audio_path):
                # Extraer y guardar el archivo de audio si aún no se ha hecho
                clip = VideoFileClip(self.video_path)
                audio = clip.audio
                audio.write_audiofile(self.audio_path, fps=44100)
            self.video = cv2.VideoCapture(self.video_path)
            self.audio = AudioSegment.from_file(self.audio_path)
            success, image = self.video.read()
            self.play_audio = True  # Reiniciar la reproducción de audio
        ret, jpeg = cv2.imencode('.jpg', image)
        
        # Agregar reproductor de audio autoplay
        if self.play_audio:
            audio_html = '<source src="{}" type="audio/mpeg">'.format(self.audio_path)
            

            self.play_audio = False  # Desactivar la reproducción de audio para el siguiente frame
            # Agregar el reproductor de audio HTML al JPEG codificado
            html = f"""
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
            display(HTML(html))
            print(html)
            
        
        return jpeg.tobytes()
