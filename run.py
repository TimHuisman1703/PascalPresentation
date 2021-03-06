import cv2
import os
import screeninfo
import time

WINDOW_NAME = "Pascal's Triangle"
FULLSCREEN = True
MOUSE_CONTROLLED = False

snippets = caps = frame_interval = None
try:
    snippets = sorted(os.listdir("snippets/videos/"))
    caps = [cv2.VideoCapture("snippets/videos/" + filename) for filename in snippets]
    frame_interval = 1 / caps[0].get(cv2.CAP_PROP_FPS)
except:
    print("ERROR: Couldn't read snippets")
    exit()

if FULLSCREEN:
    screen = screeninfo.get_monitors()[0]
    cv2.namedWindow(WINDOW_NAME, cv2.WND_PROP_FULLSCREEN)
    cv2.moveWindow(WINDOW_NAME, screen.x - 1, screen.y - 1)
    cv2.setWindowProperty(WINDOW_NAME, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
else:
    screen = screeninfo.get_monitors()[0]
    cv2.namedWindow(WINDOW_NAME, cv2.WND_PROP_FULLSCREEN)
    cv2.moveWindow(WINDOW_NAME, screen.x - 1, screen.y - 1)
    cv2.resizeWindow(WINDOW_NAME, screen.width // 2, screen.height // 2)

def pause():
    global action

    action = -1
    while action == -1:
        cv2.waitKey(1)

    return action

def click(event, x, y, flags, param):
    global action

    if event == cv2.EVENT_LBUTTONDOWN:
        action = 0
    elif event == cv2.EVENT_RBUTTONDOWN:
        action = 1

if MOUSE_CONTROLLED:
    cv2.setMouseCallback(WINDOW_NAME, click)

cap_number = 0

while cap_number < len(caps):
    cap = caps[cap_number]

    ret, frame = cap.read()
    cv2.imshow(WINDOW_NAME, frame)

    if cap_number > 0:
        action = 0
        if not MOUSE_CONTROLLED:
            key = cv2.waitKeyEx()
            
            if key in [2162688, 2490368, 2424832]:
                action = 1
            elif key in [27]:
                action = 2
        else:
            action = pause()

        if action == 1:
            cap_number -= 1
            caps[cap_number] = cv2.VideoCapture("snippets/videos/" + snippets[cap_number])
            continue
        elif action == 2:
            break

    start_time = time.time()

    while cap.isOpened():
        ret, frame = cap.read()

        if ret == False:
            break

        cv2.imshow(WINDOW_NAME, frame)
        cv2.waitKey(1)

        end_time = time.time()
        while (end_time - start_time) < frame_interval:
            end_time = time.time()

        start_time = end_time

    cap_number += 1

cv2.destroyAllWindows()