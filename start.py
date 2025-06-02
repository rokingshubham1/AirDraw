import numpy as np
import cv2
from collections import deque
from tkinter import *
from PIL import Image, ImageTk

from pathlib import Path

from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)





def setValues(x):
    print("")

root = Tk()

root.geometry("1400x1000")
root.configure(bg = "#FFFFFF")



cv2.namedWindow("Color detectors")
cv2.createTrackbar("Upper Hue", "Color detectors", 153, 180, setValues)
cv2.createTrackbar("Upper Saturation", "Color detectors", 255, 255, setValues)
cv2.createTrackbar("Upper Value", "Color detectors", 255, 255, setValues)
cv2.createTrackbar("Lower Hue", "Color detectors", 64, 180, setValues)
cv2.createTrackbar("Lower Saturation", "Color detectors", 72, 255, setValues)
cv2.createTrackbar("Lower Value", "Color detectors", 49, 255, setValues)


# The kernel to be used for dilation purpose
kernel = np.ones((5, 5), np.uint8)


colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 255, 255)]
colorIndex = 0



# Loading the default webcam of PC.
cap = cv2.VideoCapture(0)

# function for calibration and masking
def mask():

    while True:
        # Identifying the pointer by making its mask
        ret,frame = cap.read()
        frame = cv2.flip(frame, 1)
    #hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        u_hue = cv2.getTrackbarPos("Upper Hue", "Color detectors")
        u_saturation = cv2.getTrackbarPos("Upper Saturation", "Color detectors")
        u_value = cv2.getTrackbarPos("Upper Value", "Color detectors")
        l_hue = cv2.getTrackbarPos("Lower Hue", "Color detectors")
        l_saturation = cv2.getTrackbarPos("Lower Saturation", "Color detectors")
        l_value = cv2.getTrackbarPos("Lower Value", "Color detectors")
        Upper_hsv = np.array([u_hue, u_saturation, u_value])
        Lower_hsv = np.array([l_hue, l_saturation, l_value])
        Mask = cv2.inRange(hsv, Lower_hsv, Upper_hsv)
        Mask = cv2.erode(Mask, kernel, iterations=1)
        Mask = cv2.morphologyEx(Mask, cv2.MORPH_OPEN, kernel)
        Mask = cv2.dilate(Mask, kernel, iterations=1)
        cv2.imshow("mask", Mask)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

# Function for cam board
def Tracking():

    bpoints = [deque(maxlen=1024)]
    gpoints = [deque(maxlen=1024)]
    rpoints = [deque(maxlen=1024)]
    ypoints = [deque(maxlen=1024)]

    blue_index = 0
    green_index = 0
    red_index = 0
    yellow_index = 0

    colorIndex = 0
    while True:
        # Reading the frame from the camera
        ret, frame = cap.read()
        # Flipping the frame to see same side of yours
        frame = cv2.flip(frame, 1)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
         
        u_hue = cv2.getTrackbarPos("Upper Hue", "Color detectors")
        u_saturation = cv2.getTrackbarPos("Upper Saturation", "Color detectors")
        u_value = cv2.getTrackbarPos("Upper Value", "Color detectors")
        l_hue = cv2.getTrackbarPos("Lower Hue", "Color detectors")
        l_saturation = cv2.getTrackbarPos("Lower Saturation", "Color detectors")
        l_value = cv2.getTrackbarPos("Lower Value", "Color detectors")
        Upper_hsv = np.array([u_hue, u_saturation, u_value])
        Lower_hsv = np.array([l_hue, l_saturation, l_value])

        frame = cv2.rectangle(frame, (40, 1), (140, 65), (122, 122, 122), -1)
        frame = cv2.rectangle(frame, (160, 1), (255, 65), colors[0], -1)
        frame = cv2.rectangle(frame, (275, 1), (370, 65), colors[1], -1)
        frame = cv2.rectangle(frame, (390, 1), (485, 65), colors[2], -1)
        frame = cv2.rectangle(frame, (505, 1), (600, 65), colors[3], -1)
        cv2.putText(frame, "CLEAR ALL", (49, 33),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.putText(frame, "BLUE", (185, 33), cv2.FONT_HERSHEY_SIMPLEX,
                0.5, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.putText(frame, "GREEN", (298, 33), cv2.FONT_HERSHEY_SIMPLEX,
                0.5, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.putText(frame, "RED", (420, 33), cv2.FONT_HERSHEY_SIMPLEX,
                0.5, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.putText(frame, "YELLOW", (520, 33), cv2.FONT_HERSHEY_SIMPLEX,
                0.5, (150, 150, 150), 2, cv2.LINE_AA)

        Mask = cv2.inRange(hsv, Lower_hsv, Upper_hsv)
        Mask = cv2.erode(Mask, kernel, iterations=1)
        Mask = cv2.morphologyEx(Mask, cv2.MORPH_OPEN, kernel)
        Mask = cv2.dilate(Mask, kernel, iterations=1)
        cnts, _ = cv2.findContours(Mask.copy(), cv2.RETR_EXTERNAL,
                cv2.CHAIN_APPROX_SIMPLE)
        center = None
        if len(cnts) > 0:
            cnt = sorted(cnts, key=cv2.contourArea, reverse=True)[0]
            ((x, y), radius) = cv2.minEnclosingCircle(cnt)
            cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
            M = cv2.moments(cnt)
            center = (int(M['m10'] / M['m00']), int(M['m01'] / M['m00']))

            # Now checking if the user wants to click on any button above the screen
            if center[1] <= 65:
                if 40 <= center[0] <= 140:  # Clear Button
                    bpoints = [deque(maxlen=512)]
                    gpoints = [deque(maxlen=512)]
                    rpoints = [deque(maxlen=512)]
                    ypoints = [deque(maxlen=512)]

                    blue_index = 0
                    green_index = 0
                    red_index = 0
                    yellow_index = 0

                    #paintWindow[67:, :, :] = 255
                elif 160 <= center[0] <= 255:
                    colorIndex = 0  # Blue
                elif 275 <= center[0] <= 370:
                    colorIndex = 1  # Green
                elif 390 <= center[0] <= 485:
                    colorIndex = 2  # Red
                elif 505 <= center[0] <= 600:
                    colorIndex = 3  # Yellow
            else:
                if colorIndex == 0:
                    bpoints[blue_index].appendleft(center)
                elif colorIndex == 1:
                    gpoints[green_index].appendleft(center)
                elif colorIndex == 2:
                    rpoints[red_index].appendleft(center)
                elif colorIndex == 3:
                    ypoints[yellow_index].appendleft(center)
        # Append the next deques when nothing is detected to avois messing up
        else:
            bpoints.append(deque(maxlen=512))
            blue_index += 1
            gpoints.append(deque(maxlen=512))
            green_index += 1
            rpoints.append(deque(maxlen=512))
            red_index += 1
            ypoints.append(deque(maxlen=512))
            yellow_index += 1

        # Draw lines of all the colors on the canvas and frame
        points = [bpoints, gpoints, rpoints, ypoints]
        for i in range(len(points)):
            for j in range(len(points[i])):
                for k in range(1, len(points[i][j])):
                    if points[i][j][k - 1] is None or points[i][j][k] is None:
                        continue
                    cv2.line(frame, points[i][j][k - 1],
                            points[i][j][k], colors[i], 2)
        cv2.imshow("Tracking", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
                

# Function for white board
def Paint():
    # Giving different arrays to handle colour points of different colour
    bpoints = [deque(maxlen=1024)]
    gpoints = [deque(maxlen=1024)]
    rpoints = [deque(maxlen=1024)]
    ypoints = [deque(maxlen=1024)]
    # These indexes will be used to mark the points in particular arrays of specific colour
    blue_index = 0
    green_index = 0
    red_index = 0
    yellow_index = 0

    colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 255, 255)]
    colorIndex = 0

    # Here is code for Canvas setup
    paintWindow = np.zeros((1071, 6360, 3)) + 255
    paintWindow = cv2.rectangle(paintWindow, (40, 1), (140, 65), (0, 0, 0), 2)
    paintWindow = cv2.rectangle(paintWindow, (160, 1), (255, 65), colors[0], -1)
    paintWindow = cv2.rectangle(paintWindow, (275, 1), (370, 65), colors[1], -1)
    paintWindow = cv2.rectangle(paintWindow, (390, 1), (485, 65), colors[2], -1)
    paintWindow = cv2.rectangle(paintWindow, (505, 1), (600, 65), colors[3], -1)

    cv2.putText(paintWindow, "CLEAR", (49, 33),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
    cv2.putText(paintWindow, "BLUE", (185, 33), cv2.FONT_HERSHEY_SIMPLEX,
                0.5, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(paintWindow, "GREEN", (298, 33),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(paintWindow, "RED", (420, 33), cv2.FONT_HERSHEY_SIMPLEX,
                0.5, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(paintWindow, "YELLOW", (520, 33),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (150, 150, 150), 2, cv2.LINE_AA)
    while True:
        # Reading the frame from the camera
        ret, frame = cap.read()
        # Flipping the frame to see same side of yours
        frame = cv2.flip(frame, 1)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        u_hue = cv2.getTrackbarPos("Upper Hue", "Color detectors")
        u_saturation = cv2.getTrackbarPos("Upper Saturation", "Color detectors")
        u_value = cv2.getTrackbarPos("Upper Value", "Color detectors")
        l_hue = cv2.getTrackbarPos("Lower Hue", "Color detectors")
        l_saturation = cv2.getTrackbarPos("Lower Saturation", "Color detectors")
        l_value = cv2.getTrackbarPos("Lower Value", "Color detectors")
        Upper_hsv = np.array([u_hue, u_saturation, u_value])
        Lower_hsv = np.array([l_hue, l_saturation, l_value])

        frame = cv2.rectangle(frame, (40, 1), (140, 65), (122, 122, 122), -1)
        frame = cv2.rectangle(frame, (160, 1), (255, 65), colors[0], -1)
        frame = cv2.rectangle(frame, (275, 1), (370, 65), colors[1], -1)
        frame = cv2.rectangle(frame, (390, 1), (485, 65), colors[2], -1)
        frame = cv2.rectangle(frame, (505, 1), (600, 65), colors[3], -1)
        cv2.putText(frame, "CLEAR ALL", (49, 33),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.putText(frame, "BLUE", (185, 33), cv2.FONT_HERSHEY_SIMPLEX,
                0.5, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.putText(frame, "GREEN", (298, 33), cv2.FONT_HERSHEY_SIMPLEX,
                0.5, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.putText(frame, "RED", (420, 33), cv2.FONT_HERSHEY_SIMPLEX,
                0.5, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.putText(frame, "YELLOW", (520, 33), cv2.FONT_HERSHEY_SIMPLEX,
                0.5, (150, 150, 150), 2, cv2.LINE_AA)
        Mask = cv2.inRange(hsv, Lower_hsv, Upper_hsv)
        Mask = cv2.erode(Mask, kernel, iterations=1)
        Mask = cv2.morphologyEx(Mask, cv2.MORPH_OPEN, kernel)
        Mask = cv2.dilate(Mask, kernel, iterations=1)
        cnts, _ = cv2.findContours(Mask.copy(), cv2.RETR_EXTERNAL,
                cv2.CHAIN_APPROX_SIMPLE)
        center = None
        ## Ifthe contours are formed
        if len(cnts) > 0:
            # sorting the contours to find biggest
            cnt = sorted(cnts, key=cv2.contourArea, reverse=True)[0]
            # Get the radius of the enclosing circle around the found contour
            ((x, y), radius) = cv2.minEnclosingCircle(cnt)
            # Draw the circle around the contour
            cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
            # Calculating the center of the detected contour
            M = cv2.moments(cnt)
            center = (int(M['m10'] / M['m00']), int(M['m01'] / M['m00']))
            # Now checking if the user wants to click on any button above the screen
            if center[1] <= 65:
                if 40 <= center[0] <= 140:  # Clear Button
                    bpoints = [deque(maxlen=512)]
                    gpoints = [deque(maxlen=512)]
                    rpoints = [deque(maxlen=512)]
                    ypoints = [deque(maxlen=512)]
                    blue_index = 0
                    green_index = 0
                    red_index = 0
                    yellow_index = 0
                    paintWindow[67:, :, :] = 255
                elif 160 <= center[0] <= 255:
                    colorIndex = 0  # Blue
                elif 275 <= center[0] <= 370:
                    colorIndex = 1  # Green
                elif 390 <= center[0] <= 485:
                    colorIndex = 2  # Red
                elif 505 <= center[0] <= 600:
                    colorIndex = 3  # Yellow
            else:
                if colorIndex == 0:
                    bpoints[blue_index].appendleft(center)
                elif colorIndex == 1:
                    gpoints[green_index].appendleft(center)
                elif colorIndex == 2:
                    rpoints[red_index].appendleft(center)
                elif colorIndex == 3:
                    ypoints[yellow_index].appendleft(center)
        # Append the next deques when nothing is detected to avois messing up
        else:
            bpoints.append(deque(maxlen=512))
            blue_index += 1
            gpoints.append(deque(maxlen=512))
            green_index += 1
            rpoints.append(deque(maxlen=512))
            red_index += 1
            ypoints.append(deque(maxlen=512))
            yellow_index += 1
        # Draw lines of all the colors on the canvas and frame
        points = [bpoints, gpoints, rpoints, ypoints]
        for i in range(len(points)):
            for j in range(len(points[i])):
                for k in range(1, len(points[i][j])):
                    if points[i][j][k - 1] is None or points[i][j][k] is None:
                        continue
                    #cv2.line(frame, points[i][j][k - 1],
                         #points[i][j][k], colors[i], 2)
                    cv2.line(paintWindow, points[i][j]
                         [k - 1], points[i][j][k], colors[i], 2)
        cv2.imshow("Paint", paintWindow)
        cv2.namedWindow('Paint', cv2.WINDOW_AUTOSIZE)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
        if cv2.waitKey(3) & 0xFF == ord("s"):
            i+=1
            cv2.imshow("imshow2",frame)
            cv2.imwrite('D:/AirDraw_Saved_Slides/slide_'+str(i)+'.png', frame)
            print("Wrote Image")
            continue

#main-menu User Interface, designed using figma

canvas = Canvas(    # main frame for UI
    root,
    bg = "#FFFFFF",
    height = 1025,
    width = 1440,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)   # this locates coordinates for images on main frame
image_image_1 = PhotoImage(
    master = canvas,
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    720.0,
    512.0,
    image=image_image_1
)

image_image_2 = PhotoImage(
    master=canvas,
    file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(
    1333.3726196289062,
    745.0,
    image=image_image_2
)

# UI for buttons on main menu

button_image_1 = PhotoImage(             
    master = canvas,
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=Paint,
    relief="flat"

)
button_1.place(
    x=113.9999771118164,
    y=338.0,
    width=606.0,
    height=146.51031494140625
)

button_image_2 = PhotoImage(
    master=canvas,
    file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=Tracking,
    relief="flat"
)
button_2.place(
    x=114.00003814697266,
    y=534.0,
    width=605.9999389648438,
    height=137.0
)

button_image_3 = PhotoImage(
    master=canvas,
    file=relative_to_assets("button_3.png"))
button_3 = Button(
    image=button_image_3,
    borderwidth=0,
    highlightthickness=0,
    command=mask,
    relief="flat"
)
button_3.place(
    x=114.00003814697266,
    y=723.6097412109375,
    width=605.9999389648438,
    height=184.3902587890625
)

image_image_3 = PhotoImage(
    master = canvas,
    file=relative_to_assets("image_3.png"))
image_3 = canvas.create_image(
    1111.0,
    566.0,
    image=image_image_3
)

image_image_4 = PhotoImage(
    master = canvas,
    file=relative_to_assets("image_4.png"))
image_4 = canvas.create_image(
    258.00000762939453,
    216.0,
    image=image_image_4
)

canvas.create_text(
    423.0,
    105.0,
    anchor="nw",
    text="  Air   Draw",
    fill="#FFFFFF",
    font=("Rosario Bold", 144 * -1)
)
root.resizable(False, False)
# callback function for GUI
root.mainloop()

    
# Release the camera and all resources

cap.release()
cv2.destroyAllWindows()
