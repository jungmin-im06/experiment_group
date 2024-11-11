import tkinter as tk
import cv2
import face_recognition
import time
from scipy.spatial import distance
import pygame
from pyvidplayer2 import Video
import platform
from tkinter import messagebox
import imutils
from pymongo import MongoClient

import WebCamVideo
import DisplayLink
import DisplayIntro

# Try importing AppKit for macOS functionality (if available)
try:
  if platform.system() == "Darwin":  # Check for macOS using platform module
    from AppKit import NSApplication, NSAlert, NSWindow, NSSound
    from Foundation import NSAutoreleasePool
except ModuleNotFoundError:
  pass

def initial_values():
    global gone_timestamp, closed_timestamp, face_gone, face_closed, gone_alarm_duration, closed_alarm_duration, \
        gone_alarm_count, closed_alarm_count, pause_duration, duration_limit
    
    gone_timestamp = -1
    closed_timestamp = -1

    gone_alarm_duration = 0
    closed_alarm_duration = 0
    gone_alarm_count = 0
    closed_alarm_count = 0
    pause_duration = 0
    face_gone = False
    face_closed = False

    # setting the limit of learning time
    duration_limit = 1 *60


def reset_counter():
    global gone_timestamp, closed_timestamp, face_gone, face_closed
    gone_timestamp = -1
    closed_timestamp = -1

    face_gone = False
    face_closed = False

# showing alert
def show_alert(type, blink):
    global gone_alarm_duration, closed_alarm_duration, gone_alarm_count, closed_alarm_count

    os_name = platform.system()

    vid.toggle_pause()
    alarm_timestamp = time.time()

    # if computer is running on MacOS
    if os_name == 'Darwin':
        pool = NSAutoreleasePool.alloc().init()
        alert = NSAlert.alloc().init()
        alert.setMessageText_("경고!")

        if type == 'face':
            alert.setInformativeText_("화면에서 얼굴이 보이지 않아요. 화면을 보며 학습에 집중해 볼까요?")

        elif type == 'eye':
            alert.setInformativeText_("눈을 감고 계신 시간이 길어지고 있어요. 화면을 보며 학습에 집중해 볼까요?")
        
        NSSound.soundNamed_("Glass").play()

        response = alert.runModal()
        del pool

    # if computer is running on Windows
    elif os_name == 'Windows':
        import winsound
        root = tk.Tk() 
        root.attributes("-topmost", True)  # Ensure the alert window is on top
        root.withdraw()  # Hide the tkinter window

        if type == 'face':
            winsound.Beep(1500, 300) 
            tk.messagebox.showwarning("알림!", "화면에서 얼굴이 보이지 않아요. 화면을 보며 학습에 집중해 볼까요?")
        elif type == 'eye':
            winsound.Beep(1500, 300) 
            tk.messagebox.showwarning("알림!", "눈을 감고 계신 시간이 길어지고 있어요. 화면을 보며 학습에 집중해 볼까요?")

        root.destroy()
    
    vid.toggle_pause()
    
    if type == 'face':
        gone_alarm_duration += time.time() - alarm_timestamp
        gone_alarm_count += 1
    
    elif type == 'eye':
        closed_alarm_duration += time.time() - alarm_timestamp
        closed_alarm_count += 1

# drawing points in face
def draw_landmarks(frame, landmarks):
    for landmark_type in landmarks:
        for point in landmarks[landmark_type]:
            cv2.circle(frame, point, 2, (0, 0, 255), -1)


def detect_blink(landmarks):
    # Assuming left eye landmarks are at index 0 and right eye landmarks are at index 1
    left_eye = landmarks['left_eye']
    right_eye = landmarks['right_eye']

    # Calculate the aspect ratio of the eyes
    left_eye_aspect_ratio = eye_aspect_ratio(left_eye)
    right_eye_aspect_ratio = eye_aspect_ratio(right_eye)

    # Average the aspect ratios of both eyes
    avg_eye_aspect_ratio = (left_eye_aspect_ratio + right_eye_aspect_ratio) / 2.0

    return avg_eye_aspect_ratio


def eye_aspect_ratio(eye):
    # Compute the euclidean distances between the two sets of vertical eye landmarks
    a = distance.euclidean(eye[1], eye[5])
    b = distance.euclidean(eye[2], eye[4])

    # Compute the euclidean distance between the horizontal eye landmarks
    c = distance.euclidean(eye[0], eye[3])

    # Compute the eye aspect ratio
    ear = (a + b) / (2.0 * c)
    return ear


def video_control(key):

    global pause_duration, paused_timestamp, resume_timestamp

    if key == "q":
            vid.stop()
              
    elif key == "space":
        vid.toggle_pause()      #pause/plays video

        # records timestamp of when it was paused
        if vid.paused:
            paused_timestamp = time.time()
        
        # records timestamp of when it was resumed
        # adds the total time video was paused to pause_duration
        else:
            resume_timestamp = time.time()
            pause_duration += resume_timestamp - paused_timestamp

        reset_counter()
    elif key == "left":
        vid.seek(-15)           #rewind 15 seconds in video

    # keys that are not required for the program
    """
    elif key == "r":            #rewind video to beginning
        vid.restart() 
    elif key == "right":
        vid.seek(15)            #skip 15 seconds in video
    elif key == "m":
        vid.toggle_mute()       #mutes/unmutes video
    """

def save_to_db(data):
    # Connect to MongoDB (Replace <username>, <password>, and <cluster-url> with your MongoDB credentials)
    client = MongoClient("mongodb+srv://aiedLAB:aiedAICU606!@aied.ysvwwtj.mongodb.net/")
    db = client['user_data']
    collection = db['experiment_data']
    
    # Insert the data into the collection
    collection.insert_one(data)

def fit_vid():
    # find the size of the computer screen
    pygame.display.set_mode((0, 0), pygame.NOFRAME)
    computer = pygame.display.Info()
    screen_width, screen_height = computer.current_w, computer.current_h

    # adjust the size of the video accordingly
    video_width, video_height = vid.original_size
    vid.change_resolution(int((screen_width/video_width) * video_height))

    # setting display for the educational video + space for progress bar
    video_width, video_height = vid.current_size
    win = pygame.display.set_mode((video_width, video_height+10))
    pygame.display.set_caption(vid.name)

    return win

def display_progress_bar(win):
    bar_width = vid.current_size[0]
    bar_height = 10
    bar_x = 0
    bar_y = vid.current_size[1]
    progress = vid.get_pos() / vid.duration
    progress_width = progress * bar_width
    
    # Draw background bar
    pygame.draw.rect(win, (50, 50, 50), (bar_x, bar_y, bar_width, bar_height))
    # Draw progress bar
    pygame.draw.rect(win, (0, 128, 255), (bar_x, bar_y, progress_width, bar_height))

def init():
    # getting face image from camera
    cap = WebCamVideo.WebcamVideoStream(src=0).start()

    global gone_timestamp, closed_timestamp, face_gone, face_closed, gone_alarm_duration, closed_alarm_duration, \
          gone_alarm_count, closed_alarm_count, pause_duration, duration_limit, assigned_num

    # reset all the counters that we have
    initial_values()

    # setting display for the educatinal video
    win = fit_vid()

    start_time = time.time()

    # while there is a video
    while vid.active:

        # detecting any keys that are pressed
        key = None
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pass
            elif event.type == pygame.KEYDOWN:
                key = pygame.key.name(event.key)

        # if a key has been pressed
        if key:
            video_control(key)

        # Capture frame-by-frame
        frame = cap.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # reducing size and changing into grayscale for efficiency
        frame = imutils.resize(frame, width=400)
        

        # Find all the faces and features in the current frame of video
        face_locations = face_recognition.face_locations(frame)

        # for detecting 1 face at a time
        if face_locations:
            one_face_location = face_locations[0]
            face_landmarks_list = face_recognition.face_landmarks(frame, [one_face_location])
            one_face_landmark = face_landmarks_list[0] if face_landmarks_list else None



        # face_landmarks = face_recognition.face_landmarks(frame)

        # if video is playing right now
        if not vid.get_paused():

            curr_time = time.time()
            if curr_time - start_time - pause_duration - gone_alarm_duration - closed_alarm_duration >= duration_limit:
                # print(vid.get_pos())
                vid.stop()

            # if face detected 
            if face_locations:
                
                # reset
                face_gone = False
                gone_timestamp = -1

                if one_face_landmark:

                    # commented it out as we don't actually have to draw anything lol
                    draw_landmarks(frame, one_face_landmark)

                    ear = detect_blink(one_face_landmark)
                    
                    # eyes closed
                    if ear < 0.25:  # Assuming 0.2 as the threshold for blink detection

                        # set time stamp if eyes closed for the first time
                        if not face_closed:
                            closed_timestamp = time.time()
                        face_closed = True

                    # eyes open
                    else:
                        face_closed = False
                        closed_timestamp = -1

            # face is not detected
            else:

                # set time stamp if face_gone for the first time
                if not face_gone:
                    gone_timestamp = time.time()
                face_gone = True

            # finding time diff between curr and last time an event has occurred
            curr_time = time.time()

            # if face was gone for more than 5 seconds
            if gone_timestamp >= 0 and curr_time - gone_timestamp >= 5: 
                show_alert('face', 0)
                reset_counter()

            if closed_timestamp >= 0 and curr_time - closed_timestamp >= 5:
                show_alert('eye', 5)
                reset_counter() 
            

        # if video is paused, reset all counter
        else:
            reset_counter()

        # Display the resulting image
        cv2.imshow('Video', frame)

        # Update the progress bar
        display_progress_bar(win)
        
        # only draw new frames, and only update the screen if something is drawn
        if vid.draw(win, (0, 0), force_draw=False):
            pygame.display.update()

    # close face detection when done
    cap.stop()
    cv2.destroyAllWindows()

    # close video when done
    vid.close()
    pygame.quit()

    data = {
        "usernum": assigned_num,
        "closed_alarm_count": closed_alarm_count,
        "closed_alarm_duration": closed_alarm_duration,
        "gone_alarm_count": gone_alarm_count,
        "gone_alarm_duration": gone_alarm_duration,
        "pause_duration": pause_duration
    }
    save_to_db(data)

if __name__ == "__main__":
    pygame.init()

    # global vid
    vid = Video("resource/2016vid.mp4")
    global gone_timestamp, closed_timestamp, face_gone, face_closed, \
    gone_alarm_count, closed_alarm_count, pause_duration, duration_limit, paused_timestamp, resume_timestamp, assigned_num

    assigned_num = input('Enter user number: ')

    if DisplayIntro.display_intro():
        init()
        DisplayLink.display_link()
