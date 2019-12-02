import cv2
import pickle
import numpy as np
import pyautogui as gui
import json
from pprint import pprint
import os
default_encoding_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "encodings.pickle")




with open("range.pickle", "rb") as f:
	t = pickle.load(f)


#VIDEOIO ERROR: V4L: can't open camera by index 1
cam = cv2.VideoCapture(0)


if cam.read()[0]==False:
	cam=cv2.VideoCapture(1)
if cam.read()[0]==False:
	cam = cv2.VideoCapture(2)
if cam.read()[0]==False:
	cam = cv2.VideoCapture(-1)

hsv_lower = np.array([t[0], t[1], t[2]])	
hsv_upper = np.array([t[3], t[4], t[5]])
width = cam.get(cv2.CAP_PROP_FRAME_WIDTH)	# width of video captured by the webcam
height = cam.get(cv2.CAP_PROP_FRAME_HEIGHT)	# height of the video captured by the webcam

def get_keys():
	"""
	this function is used to design the keyboard.
	it returns the 4 parameter that are needed to design the keys.
	they are key label, top right corner coordinate, bottom left corner coordinate, and center coordinate
	"""
	max_keys_in_a_row = 11						# max number of keys in any row is 10 i.e the first row which contains 1234567890'backspace'
	key_width = int(width/max_keys_in_a_row)	# width of one key. width is divided by 10 as the max number of keys in a single row is 11.
	
	row0_key_width = key_width * 11			# width of zeroth or numeric row of keys
	row1_key_width = key_width * 10			# width of first row
	row2_key_width = key_width * 9			# width of second row
	row3_key_width = key_width * 7			# width of third row
	row4_key_width = key_width * 5			# width of space
	row_keys = []							# stores the keys along with its 2 corner coordinates and the center coordinate

	# for the zeroth row
	x1, y1 = 0, int((height - key_width * 5) / 2)	# 5 is due to the fact that we will have 5 rows. y1 is set such that the whole keyboard has equal margin on both top and bottom
	x2, y2 = key_width + x1, key_width + y1
	c1, c2 = x1, y1					# copying x1, x2, y1 and y2
	keys = "1 2 3 4 5 6 7 8 9 0 <-"
	keys = keys.split(" ")
	for key in keys:
		if key == "<-":
			row_keys.append([key, (x1, y1), (x2, y2), (int((x2+x1)/2) - 25, int((y2+y1)/2) + 10)])
		else:
			row_keys.append([key, (x1, y1), (x2, y2), (int((x2+x1)/2) - 5, int((y2+y1)/2) + 10)])
		x1 += key_width
		x2 += key_width
	x1, y1 = c1, c2					# copying back from c1, c2, c3 and c4

	# for the first row
	x1, y1 = int((row0_key_width - row1_key_width) / 2) + x1, y1 + key_width	
	x2, y2 = key_width + x1, key_width + y1
	c1, c2 = x1, y1					# copying x1, x2, y1 and y2
	keys = "QWERTYUIOP"
	for key in keys:
		row_keys.append([key, (x1, y1), (x2, y2), (int((x2+x1)/2) - 5, int((y2+y1)/2) + 10)])
		x1 += key_width
		x2 += key_width
	x1, y1 = c1, c2					# copying back from c1, c2, c3 and c4

	# for second row
	x1, y1 = int((row1_key_width - row2_key_width) / 2) + x1, y1 + key_width   # x1 is set such that it leaves equal margin on both left and right side
	x2, y2 = key_width + x1, key_width + y1
	c1, c2 = x1, y1
	keys = "ASDFGHJKL"
	for key in keys:
		row_keys.append([key, (x1, y1), (x2, y2), (int((x2+x1)/2) - 5, int((y2+y1)/2) + 10)])
		x1 += key_width
		x2 += key_width
	x1, y1 = c1, c2

	# for third row
	x1, y1 = int((row2_key_width - row3_key_width) / 2) + x1, y1 + key_width
	x2, y2 = key_width + x1, key_width + y1	
	c1, c2 = x1, y1	
	keys = "ZXCVBNM"
	for key in keys:
		row_keys.append([key, (x1, y1), (x2, y2), (int((x2+x1)/2) - 5, int((y2+y1)/2) + 10)])
		x1 += key_width
		x2 += key_width
	x1, y1 = c1, c2

	# for the space bar
	x1, y1 = int((row3_key_width - row4_key_width) / 2) + x1, y1 + key_width
	x2, y2 = 5 * key_width + x1, key_width + y1	
	c1, c2 = x1, y1	
	keys = " "
	for key in keys:
		row_keys.append([key, (x1, y1), (x2, y2), (int((x2+x1)/2) - 5, int((y2+y1)/2) + 10)])
		x1 += key_width
		x2 += key_width
	x1, y1 = c1, c2

	return row_keys


def do_keypress(img, center, row_keys_points):
    pressed = ''

    for row in row_keys_points:
        arr1 = list(np.int0(np.array(center) >= np.array(row[1])))
        arr2 = list(np.int0(np.array(center) <= np.array(row[2])))


        if arr1==[1,1] and arr2 == [1,1]:

            if row[0] == '<-':
                gui.press('backspace')
                pressed+= '<'
            else:
                gui.press(row[0])
                pressed+=(row[0])
            cv2.fillConvexPoly(img, np.array([np.array(row[1]), np.array([row[1][0], row[2][1]]), np.array(row[2]), np.array([row[2][0], row[1][1]])]), (255, 0, 0))

            #print("PRESSED!!!! :", pressed)
    return img, pressed


def update_text(sen):
    #print("start",sen)
    global toString
    toString = ''.join(sen)
    for i in range(0,len(toString)):
        if (toString[i] == '<') and (toString[i-1] != '<'):
            #print("inLoop",toString)
            toString = toString[:i-1] + toString[i+1:]
            break
    #print("break",toString)
    if toString.count('<') > 0:
        #print("again",sen)
        update_text(list(toString))

    else:
        pass
       # print("done",toString)
    return toString








def main():
    #load comment.txt for specific stduent
    f = open('writting.txt', 'r+', encoding='utf-8')



    row_keys_points = get_keys()
    new_area, old_area = 0, 0
    c, c2 = 0, 0
    flag_keypress = False
    global sen
    sen = list(f.read())
    print("LOADING...",sen)
    cv2.namedWindow('POSCO', cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty('POSCO', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    while(True):
        img = cam.read()[1]
        # FLIP
        #img = cv2.flip(img, 1)
        imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(imgHSV, hsv_lower, hsv_upper)
        blur = cv2.medianBlur(mask, 15)
        blur = cv2.GaussianBlur(blur , (5,5), 0)
        thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1]
        # error : None type --> cv2.findContours(thresh.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)[1] -> [0]
        contours = cv2.findContours(thresh.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)[0]
        text_ = update_text(sen)
        cv2.putText(img, "TYPE: "+text_, (90, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2, cv2.LINE_AA)

        if len(contours) > 0:
            cnt = max(contours, key = cv2.contourArea)

            if cv2.contourArea(cnt) > 350:
                rect = cv2.minAreaRect(cnt)
                center = list(rect[0])
                box = cv2.boxPoints(rect)
                box = np.int0(box)
                cv2.circle(img, tuple(np.int0(center)), 2, (0, 255, 0), 2)
                cv2.drawContours(img,[box],0,(0,0,255),2)
                #calculation of difference of area and center
                new_area = cv2.contourArea(cnt)
                new_center = np.int0(center)
                if c == 0:
                    old_area = new_area
                c += 1
                diff_area = 0
                if c > 3:
                    diff_area = new_area - old_area
                    c = 0
                if c2 == 0:
                    old_center = new_center
                c2 += 1
                diff_center = np.array([0, 0])
                if c2 > 5:
                    diff_center = new_center - old_center
                    c2 = 0

                center_threshold = 10
                area_threshold = 200
                if abs(diff_center[0]) < center_threshold or abs(diff_center[1]) < center_threshold:

                    if diff_area > area_threshold and flag_keypress == False:
                        #좌표와 입력된 키 값 동시에 return 하게 만듬
                        img,pressed = do_keypress(img, new_center, row_keys_points)
                        print("********* PRESSED KEY: ", pressed)
                        sen.append(pressed)
                        #cv.putText(img, 'OpenCV', location, font, fontScale, yellow, thickness)
                        flag_keypress = True
                    elif diff_area < -(area_threshold) and flag_keypress == True:
                        flag_keypress = False
            else:
                flag_keypress = False
        else:
            flag_keypress = False

        # displaying the keyboard

        for key in row_keys_points:
            # RGB -> BGR

            #cv2.putText(img, sen, (100, 20), cv2.FONT_HERSHEY_PLAIN, 2.5, (0, 255, 0), 2)
            cv2.putText(img, key[0], key[3], cv2.FONT_HERSHEY_DUPLEX, 1, (262, 173, 93))
            cv2.rectangle(img, key[1], key[2], (255, 128,0), thickness = 3)

        cv2.imshow("POSCO",img)

        # '\x08' = ASCII Table = backsapce (chr(), ord() function)
        if cv2.waitKey(1) == ord('\x08'):
            text_ = update_text(sen)
            print(text_)
            continue


        ######


        #####

        from_motion = None

        elif cv2.waitKey(1) == ord('q'):
            text_ = update_text(sen)
            f.truncate(0)
            f.write(text_)
            #print("CLOSING...",text_)
            f.close()
            break
        else:
            continue
    cam.release()
    cv2.destroyAllWindows()

main()


