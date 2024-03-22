import tkinter as tk
import cv2
import numpy as np
import pyautogui
import mediapipe as mp
import time
import math
from tkinter import messagebox
import requests
from tkinter import ttk
import time



mappings = {'1': 1, '2': 2, '3': 8,  '4': 4, '5': 13, '6': 7, '7' : 13, '9': 10, '10' : 3}
is_open = True
last_zoom_in_time = 0
last_zoom_out_time = 0
last_left_click_time = 0
last_right_click_time = 0
last_ss_time = 0

# Set the minimum delay between zoom in actions (in seconds)


####################### Module for Hand detector ############################
#############################################################################

class handDetector():
    def __init__(self, mode=False, maxHands=2, model_complexity=1, detectionCon=0.7, trackCon=0.3):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, model_complexity,
                                        self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils
        self.tipIds = [4, 8, 12, 16, 20]

    def findHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        # print(results.multi_hand_landmarks)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms,
                                               self.mpHands.HAND_CONNECTIONS)

        return img

    def findPosition(self, img, handNo=0, draw=True):
        xList = []
        yList = []
        bbox = []
        self.lmList = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                # print(id, lm)
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                xList.append(cx)
                yList.append(cy)
                # print(id, cx, cy)
                self.lmList.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 5, (255, 0, 255), cv2.FILLED)
            print("The lmList is: ", self.lmList)
            xmin, xmax = min(xList), max(xList)
            ymin, ymax = min(yList), max(yList)
            bbox = xmin, ymin, xmax, ymax

            if draw:
                cv2.rectangle(img, (xmin - 20, ymin - 20), (xmax + 20, ymax + 20),
                              (0, 255, 0), 2)

        return self.lmList, bbox

    def fingersUp(self):
        fingers = []
        # Thumb
        if len(self.lmList) > 0:
            if self.lmList[self.tipIds[0]][1] > self.lmList[self.tipIds[0] - 1][1]:
                fingers.append(True)
            else:
                fingers.append(False)

        # Fingers
            for id in range(1, 5):

                if self.lmList[self.tipIds[id]][2] < self.lmList[self.tipIds[id] - 2][2]:
                    fingers.append(True)
                else:
                    fingers.append(False)

            if self.lmList[self.tipIds[0]][2] < self.lmList[self.tipIds[0] - 1][2] and self.lmList[self.tipIds[1]][2] < self.lmList[self.tipIds[2]][2] < self.lmList[self.tipIds[3]][2] < self.lmList[self.tipIds[4]][2]  :
                fingers.append(True)
            else:
                fingers.append(False)

            if self.lmList[self.tipIds[0]][2] > self.lmList[self.tipIds[0] - 1][2] and self.lmList[self.tipIds[1]][2] > self.lmList[self.tipIds[2]][2] > self.lmList[self.tipIds[3]][2] > self.lmList[self.tipIds[4]][2]  :
                fingers.append(True)
            else:
                fingers.append(False)
        # totalFingers = fingers.count(1)

        return fingers

    def findDistance(self, p1, p2, img, draw=True,r=15, t=3):
        x1, y1 = self.lmList[p1][1:]
        x2, y2 = self.lmList[p2][1:]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        if draw:
            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), t)
            cv2.circle(img, (x1, y1), r, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), r, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (cx, cy), r, (0, 0, 255), cv2.FILLED)
        length = math.hypot(x2 - x1, y2 - y1)

        return length, img, [x1, y1, x2, y2, cx, cy]

#################### Module for Gesture categories ##########################
#############################################################################

def OnlyIndexFingerUp(fingers):
    if not fingers[0] and fingers[1] and not fingers[2] and not fingers[3] and not fingers[4]:
        return True
    else:
        return False

def IndexAndThumbFinger(fingers):
    if fingers[0] and fingers[1] and not fingers[2] and not fingers[3] and not fingers[4]:
        return True
    else:
        return False

def RingFingerUp(fingers):
    if not fingers[1] and not fingers[2] and fingers[3] and not fingers[4]:
        return True
    else:
        return False

def IndexAndMiddleFingersUp(fingers):
    if fingers[1] and fingers[2] and not fingers[3] and not fingers[4]:
        return True
    else:
        return False

def IndexAndLastFingerUp(fingers):
    if fingers[1] and not fingers[2] and not fingers[3] and fingers[4]:
        return True
    else:
        return False

def AllFingersUp(fingers):
    if fingers[0] and fingers[1] and fingers[2] and fingers[3] and fingers[4]:
        return True
    else:
        return False

def OnlyThumbFingerUp(fingers):
    if fingers[0] and not fingers[1] and not fingers[2] and not fingers[3] and not fingers[4]:
        return True
    else:
        return False

def AllFingersClosed(fingers):
    if not fingers[0] and not fingers[1] and not fingers[2] and not fingers[3] and not fingers[4]:
        return True
    else:
        return False

def four_fingers_open(fingers):
    if fingers[0] and fingers[1] and fingers[2] and fingers[3] and not fingers[4]:
        return True
    else:
        return False

def last_four_up(fingers) :
    if not fingers[0] and fingers[1] and fingers[2] and fingers[3] and fingers[4] :
        return True
    else:
        return False

def IndexMiddleRingUp(fingers):
    if not fingers[0] and fingers[1] and fingers[2] and fingers[3] and not fingers[4]:
        return True
    else:
        return False

def ThumbsUp(fingers):
    if fingers[5]:
        return True
    else :
        return False

def Thumbsdown(fingers) :
    if fingers[6]:
        return False
    else:
        return True

category_id_for_conditions = {
    1: OnlyIndexFingerUp,
    2: IndexAndMiddleFingersUp,
    3: IndexAndThumbFinger,
    4: RingFingerUp,
    5: IndexAndLastFingerUp,
    6: AllFingersUp,
    7: AllFingersClosed,
    8: IndexMiddleRingUp,
    9: last_four_up,
    10: four_fingers_open,
    11: ThumbsUp,
    12: Thumbsdown,
    13: OnlyThumbFingerUp
}

######################## Module for Mouse actions ###########################
#############################################################################

import pyautogui
import cv2

def ZoomIn():
    global last_zoom_in_time

    # Get the current time
    current_time = time.time()
    if current_time - last_zoom_in_time >= 3:
        pyautogui.hotkey('ctrl', '+')

        last_zoom_in_time = current_time


def ZoomOut():
    global last_zoom_out_time

    # Get the current time
    current_time = time.time()
    if current_time - last_zoom_out_time >= 3:
        pyautogui.hotkey('ctrl', '-')

        last_zoom_out_time = current_time

def scrolldown():
    pyautogui.scroll(-1)

def scrollup():
    pyautogui.scroll(1)

def MouseLeftClick():
    global last_left_click_time

    # Get the current time
    current_time = time.time()
    if current_time - last_left_click_time >= 2:
        pyautogui.click()

        last_left_click_time = current_time

def MouseRightClick():
    global last_right_click_time

    # Get the current time
    current_time = time.time()
    if current_time - last_right_click_time >= 2:
        pyautogui.rightClick()

        last_right_click_time = current_time

def ScreenShot():
    global last_ss_time

    # Get the current time
    current_time = time.time()
    if current_time - last_ss_time >= 3:
        pyautogui.screenshot()

        last_ss_time = current_time

def clear(temp):
    if not temp:
        temp = True

def close_app():
    global is_open
    is_open = False


def CursorMovement(x1, y1, frameR, wCam, wScr, hCam, hScr, smoothening, clocX, clocY, plocX, plocY):
    # 5. Convert Coordinates
    x3 = np.interp(x1, (frameR, wCam - frameR), (0, wScr))
    y3 = np.interp(y1, (frameR, hCam - frameR), (0, hScr))
    # 6. Smoothen Values

    clocX = plocX + (x3 - plocX) / smoothening
    clocY = plocY + (y3 - plocY) / smoothening

    # 7. Move Mouse
    pyautogui.moveTo(wScr - clocX, clocY)
    return clocX, clocY

category_id_for_mouse_action = {
    1: CursorMovement,
    2: MouseLeftClick,
    3: MouseRightClick,
    4: ScreenShot,
    5: ZoomIn,
    6: ZoomOut,
    7: clear,
    8: close_app,
    9: scrollup,
    10: scrolldown
}

######################## Desktop app for Hand gesture recognition and computer actions ###########################
##################################################################################################################

def on_button_click():
    global mappings
    wCam, hCam = 1000, 1000
    frameR = 50  # Frame Reduction
    smoothening = 7

    pTime = 0
    plocX, plocY = 0, 0
    clocX, clocY = 0, 0

    cap = cv2.VideoCapture(0)
    cap.set(3, wCam)
    cap.set(4, hCam)
    detector = handDetector(maxHands=1)
    wScr, hScr = pyautogui.size()
    temp = True
    global is_open
    is_open = True

    while is_open:
        try:
            # 1. Find hand Landmarks
            success, img = cap.read()
            img = detector.findHands(img)
            lmList, bbox = detector.findPosition(img)
            # 2. Get the tip of the index and middle fingers
            if len(lmList) != 0:
                x1, y1 = lmList[8][1:]
                x2, y2 = lmList[12][1:]
            # 3. Check which fingers are up
            fingers = detector.fingersUp()
            cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR),
                        (255, 0, 255), 2)
            if len(fingers) > 2:
                for key, value in mappings.items():
                    if category_id_for_conditions[int(value)](fingers) :
                        if int(key) == 1:
                            plocX, plocY = CursorMovement(x1, y1, frameR, wCam, wScr, hCam, hScr, smoothening, clocX, clocY, plocX, plocY)
                        if int(key) == 2:
                            MouseLeftClick()
                        if int(key) == 3:
                            MouseRightClick()
                        if int(key) == 4:
                            ScreenShot()
                        if int(key) == 5:
                            ZoomIn()
                        if int(key) == 6:
                            ZoomOut()
                        if int(key) == 7:
                            temp = clear(temp)
                        if int(key) == 9:
                            scrollup()
                        if int(key) == 10:
                            scrolldown()

                # For stopping the app this is the logic

                if AllFingersUp(fingers):
                    while is_open:
                        success, img1 = cap.read()
                        img1 = detector.findHands(img1)
                        lmList, bbox = detector.findPosition(img1)
                        # 2. Get the tip of the index and middle fingers
                        # 3. Check which fingers are up
                        fingers1 = detector.fingersUp()
                        if AllFingersClosed(fingers1):
                            close_app()



            cTime = time.time()
            fps = 1 / (cTime - pTime)
            pTime = cTime
            cv2.putText(img, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3,
                        (255, 0, 0), 3)
            # 12. Display
            cv2.waitKey(1)
        except IndexError:
            # Handle the IndexError here, for example, you can print a message
            print("IndexError occurred. Skipping frame.")
            pass


def on_submit():
    global mappings
    # Get username and password from entry widgets
    username = username_entry.get()
    password = password_entry.get()

    # Validate the fields
    if not username or not password:
        messagebox.showerror("Error", "Please enter both username and password.")
        return
    api_url = "http://127.0.0.1:8000/api/login"
    data = {"username": username, "password": password}

    try:
        # Send a POST request to the API
        response = requests.get(api_url, params=data)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the response JSON or handle it accordingly
            user_details = response.json()
            mappings = user_details
            print(mappings)
            # Do something with the user details (e.g., display them in a new window)


        else:
            messagebox.showerror("Error", f"Failed to log in. Status Code: {response.status_code}")
            print(response)

    except requests.RequestException as e:
        messagebox.showerror("Error", f"Request failed: {e}")

# Create the main window
def close_window():
    global is_open
    is_open = False

# Create the main window
BACKGROUND_COLOR = "#C1E3ED"
FRAME_COLOR = "#333333"
def_maps=["DEFAULT MAPPINGS\n","\n","1.Only Index Finger:Cursor Movement \n","2.Index&Thumb fingers:Right Click \n","3.Only Ring Finger:Screenshot \n","4.Index&Middle Finger:Left Click \n","5.Index&Last Finger:Zoom \n","6.All Fingers:Clear"]

# Create the main window
app = tk.Tk()
app.title("Hand Gesture Recognition App")
app.configure(bg=BACKGROUND_COLOR)


# Set window size
window_width = 400
window_height = 300

# Get screen width and height
screen_width = app.winfo_screenwidth()
screen_height = app.winfo_screenheight()

# Calculate the x and y coordinates for the Tk root window
x_coordinate = (screen_width - window_width) // 2
y_coordinate = (screen_height - window_height) // 2

# Set the window size and position
app.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")



tab_control = ttk.Notebook(app)
tab2 = ttk.Frame(tab_control)
tab1 = ttk.Frame(tab_control)

listbox = tk.Listbox(tab1, selectmode=tk.SINGLE,background=BACKGROUND_COLOR)
for item in def_maps:
    listbox.insert(tk.END, item)

tab_control.add(tab1, text=" Default Gesture Recognition")
tab_control.add(tab2, text="Login (Optional)")
tab_control.pack(expand=True, fill="both")
#tab_control.configure(background=BACKGROUND_COLOR)
# Create a button with improved formatting
button = tk.Button(
    app,
    text="Start Gesture Recognition",
    command=on_button_click,
    padx=15,
    pady=5,
    foreground="#f57251",  # Ensure visible text
    borderwidth=0  # Remove the border
)
# Pack the button within the frame
button.pack()
listbox.pack(padx=10, pady=10,fill=tk.X)

# Create labels and entry fields with consistent formatting
label_padx = 5
label_pady = 5
entry_padx = 5
entry_pady = 5

frame_padding = 10
frame1 = tk.Frame(tab2, bg=BACKGROUND_COLOR,padx=frame_padding, pady=frame_padding)
frame2 = tk.Frame(tab2, bg=FRAME_COLOR, padx=frame_padding, pady=frame_padding)
frame1.pack(pady=frame_padding)
frame2.pack(pady=frame_padding)

username_label = tk.Label(frame1, text="Username:", padx=label_padx, pady=label_pady)
username_label.grid(row=0, column=0)

username_entry = tk.Entry(frame1)
username_entry.grid(row=0, column=1, padx=entry_padx, pady=entry_pady)

password_label = tk.Label(frame1, text="Password:", padx=label_padx, pady=label_pady)
password_label.grid(row=1, column=0)

password_entry = tk.Entry(frame1, show="*")
password_entry.grid(row=1, column=1, padx=entry_padx, pady=entry_pady)

# Create a submit button with consistent formatting
submit_button = tk.Button(
    frame2,
    text="Submit",
    command=on_submit,
    padx=5,
    pady=5,
    foreground="#f57251",  # Ensure visible text
    borderwidth=0  # Remove the border
)
# Pack the button with spacing
submit_button.pack()

# Run the application
app.mainloop()
