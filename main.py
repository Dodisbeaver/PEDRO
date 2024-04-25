from flask import Flask, render_template, Response, request, send_from_directory
from camera import VideoCamera
import os
import time
import signal
import sys
import pygame
import threading
import random

pi_camera = VideoCamera(flip=False) # flip pi camera if upside down.
global operator_handling
operator_handling = False
pygame.mixer.init()

sounds = {
    1: ["./AUDIO/1.1.wav", "./AUDIO/1.2.wav", "./AUDIO/1.3.wav"],
    2: ["./AUDIO/2.1.wav", "./AUDIO/2.2.wav", "./AUDIO/2.3.wav"],
    3: ["./AUDIO/3.1.wav", "./AUDIO/3.2.wav", "./AUDIO/3.3.wav"],
    4: ["./AUDIO/4.1.wav", "./AUDIO/4.2.wav", "./AUDIO/4.3.wav"],
    5: ["./AUDIO/5.1.wav", "./AUDIO/5.2.wav", "./AUDIO/5.3.wav"],
    6: ["./AUDIO/6.1.wav", "./AUDIO/6.2.wav", "./AUDIO/6.3.wav"],
    7: ["./AUDIO/7.1.wav", "./AUDIO/7.2.wav", "./AUDIO/7.3.wav"]
}

# Load the sounds
for section, filenames in sounds.items():
    for filename in filenames:
        sounds[section][filenames.index(filename)] = pygame.mixer.Sound(filename)

random_number = random.randint(0,2)
sound_channel = pygame.mixer.Channel(1)
sound_channel.play(sounds[1][random_number])

while sound_channel.get_busy():  

    pygame.time.delay(10)

sound_channel = pygame.mixer.Channel(1)
sound_channel.play(sounds[7][random_number])

while sound_channel.get_busy():  

    pygame.time.delay(10)


def signal_handler(sig, frame):
    print('Caught Ctrl+C, shutting down...')

    if pi_camera:  
        pi_camera.release()  
    sys.exit(0)  

signal.signal(signal.SIGINT, signal_handler)
# App Globals (do not edit)
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html') #you can customze index.html here

def gen(camera):
   
    operator_handling = False
    can_play = True
    found_person = False
    frames = 0

    while True:
        random_number = random.randint(0,2)
        frame, person_detected = camera.get_frame()
        frames += 1
        print(frames)
        if frames == 100:
            can_play = True
        if frame is not None:  
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        else:
            time.sleep(0.1)  

        if person_detected and can_play and not operator_handling:
            can_play = False
            if found_person:
                threading.Thread(target=say_something, args=(5, random_number)).start()
            else:
                threading.Thread(target=say_something, args=(4, random_number)).start()
                found_person = True
            frames = 0
        if frames > 140:
            threading.Thread(target=say_something, args=(random.randint(2,3), random_number)).start()
            found_person = False
            operator_handling = False
            frames = 0


def say_something(phrase=1, version=1):
    
    sound_channel = pygame.mixer.Channel(0)  
    sound_channel.play(sounds[phrase][version])



@app.route('/video_feed')
def video_feed():
    return Response(gen(pi_camera),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/sound')
def play_sound():
    random_number = random.randint(0,2)
    sound_channel = pygame.mixer.Channel(1)
    sound_channel.play(sounds[6][random_number])
    global operator_handling
    operator_handling = True


    return "None"


if __name__ == '__main__':

    app.run(host='0.0.0.0', debug=False)
