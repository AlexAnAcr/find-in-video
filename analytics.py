import numpy as np
import os
import io
import datetime

root_path = r'C:\Users\user\Downloads\VideoData'

finded_faces = dict()

def remove_prefix(text, prefix):
    if text.startswith(prefix):
        return text[len(prefix):]
    return text

def lines_proc(lines):
    for line in lines:
        line = line.strip()
        if line != '':
            line = remove_prefix(line, "D:\\Видео\\")
            lparts = line.split(' - ')
            lparts[0] = lparts[0].strip()
            if lparts[0] in finded_faces:
                finded_faces[lparts[0]].append(float(lparts[1].strip()))
                
            else:
                finded_faces[lparts[0]] = [float(lparts[1].strip())]

                
for root, dirs, files in os.walk(root_path):
    for file in files:
        if file.endswith('.txt'):
            f = io.open(os.path.join(root, file), mode="r", encoding="utf-8")
            lines = f.readlines()
            f.close()
            lines_proc(lines)

f = io.open('results.txt', mode="w+", encoding="utf-8")
for key, values in sorted(finded_faces.items()):
    f.write(key + ' :')
    for value in values:
        conversion = datetime.timedelta(seconds=int(value))
        f.write( ', ' + str(conversion))
    f.write('\n')
f.close()
