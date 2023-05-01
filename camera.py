import cv2
# Lista de videos
import os

video_dir = '/content/drive/MyDrive/Videos'
video_files = [f for f in os.listdir(video_dir) if f.endswith('.mp4')]
video_list = [os.path.join(video_dir, f) for f in video_files]
print(video_list)
class VideoCamera(object):
    def __init__(self):
        self.video_list = video_list
        self.current_video = 0        
        self.video = cv2.VideoCapture(self.video_list[self.current_video])
        
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
            self.video = cv2.VideoCapture(self.video_list[self.current_video])
            success, image = self.video.read()
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()
