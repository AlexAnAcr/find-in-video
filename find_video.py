import os
import cv2
from pymediainfo import MediaInfo
import face_recognition
import numpy as np
import subprocess as sp
import io

f = io.open('list.ini', mode="r", encoding="utf-8")
root_paths = f.readlines()
f.close()

with open('set.ini') as f:
    set = f.readlines()

denom = int(set[1].strip())
rest = int(set[2].strip())

photo_encoding = face_recognition.face_encodings(face_recognition.load_image_file(set[0].strip()))[0]

def video_proc(file, pixel_ratio, fps, frame_width, frame_height):
    count = 0
    succ_cond = 0
    
    fps = float(fps)
    frame_height = int(frame_height)
    frame_width = int(frame_width)
    if pixel_ratio != 1:
        frame_width = int(frame_width * float(pixel_ratio))
     
    command = ['ffmpeg.exe',
           '-i', file,
           '-f', 'image2pipe',
           '-loglevel', 'quiet',
           '-pix_fmt', 'rgb24',
            '-vf', 'yadif,scale='+str(frame_width)+':'+str(frame_height),
           '-vcodec', 'rawvideo', '-']
    pipe = sp.Popen(command, stdout = sp.PIPE)

    res=frame_width*frame_height*3
    while(True):
         
        frame = np.frombuffer(pipe.stdout.read(res), dtype='uint8')
        if len(frame) == 0:
            break
        frame = frame.reshape((frame_height,frame_width,3))[:, :, ::-1]
        
        count += 1
        if (count >= succ_cond):
            face_locations = face_recognition.face_locations(frame)
            frame_encodings = face_recognition.face_encodings(frame, face_locations)
            
            results = face_recognition.compare_faces(frame_encodings, photo_encoding, tolerance=0.7)
            if np.any(results):
                succ_cond = count + 5 * fps
                f = io.open('finded.txt', mode="a+", encoding="utf-8")
                f.write(file + ' - ' + str(count / fps) + "\n")
                f.close()
                print('Success!')

for root_path in root_paths:
    root_path = root_path.strip()
    for root, dirs, files in os.walk(root_path):
        num = 0
        for name in files:
            if (num % denom == rest):
                file = os.path.join(root, name)
            
                media_info = MediaInfo.parse(file)
                for track in media_info.tracks:
                    if track.track_type == "Video":
                        print(file)
                        video_proc(file, track.pixel_aspect_ratio, track.frame_rate, track.width, track.height)
            num += 1


