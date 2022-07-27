import os
import cv2
import numpy as np
import math
from PIL import Image
from retinaface import RetinaFace
import matplotlib.pyplot as plt
from deepface import DeepFace

# resize y
def image_resize_y(img_path: str, output_path: str, length: int) -> None:
    dst = cv2.imread(img_path, cv2.IMREAD_COLOR)
    img_trim = dst[:, :]
    cv2.imwrite(output_path, img_trim) 

# resize x
def image_resize_x(img_path: str, output_path: str, length: int) -> None:
    dst = cv2.imread(img_path, cv2.IMREAD_COLOR)
    img_trim = dst[:, :]
    cv2.imwrite(output_path, img_trim) 

# Contour criteria hand
def image_resize_hand(img_path: str, output_path: str) -> None:
    src = cv2.imread(img_path, cv2.IMREAD_COLOR)

    gray = cv2.cvtColor(src, cv2.COLOR_RGB2GRAY)
    blur = cv2.GaussianBlur(gray, ksize=(3,3), sigmaX=0)
    edged = cv2.Canny(blur, 10, 250)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7,7))
    ret, binary = cv2.threshold(edged, 127, 255, cv2.THRESH_TOZERO)
    binary = cv2.bitwise_not(binary)

    contours, hierarchy = cv2.findContours(binary, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_TC89_KCOS)

    for i in range(len(contours)):
        cv2.drawContours(src, [contours[i]], 0, (0, 255, 0), 2)
        cv2.putText(src, str(i), tuple(contours[i][0][0]), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 255, 0), 1)
    
    contours_xy = np.array(contours)

    hand_x_min, hand_x_max = float('inf'), float('-inf')
    hand_y_left, hand_y_right = 0, 0
    for i in range(len(contours_xy)):
        for j in range(len(contours_xy[i])):
            if not contours_xy[i][j][0][0] == 0 and hand_x_min > contours_xy[i][j][0][0]:
                hand_x_min = contours_xy[i][j][0][0]
                hand_y_left = contours_xy[i][j][0][1]
            if not contours_xy[i][j][0][0] == 500 and hand_x_max < contours_xy[i][j][0][0]:
                hand_x_max = contours_xy[i][j][0][0]
                hand_y_right = contours_xy[i][j][0][1]
        
    y_min, y_max = 0,0
    value = list()
    for i in range(len(contours_xy)):
        for j in range(len(contours_xy[i])):
            value.append(contours_xy[i][j][0][1])
    value.sort()
    y_min = value[2]
    y_max = value[-3]

    x = hand_x_max - hand_x_min
    if x > 256:
        avg_x = x - 256
        hand_x_max -= avg_x / 2
        hand_x_min += avg_x / 2
    elif x < 256:
        avg_x = 256 - x
        hand_x_max += avg_x / 2
        hand_x_min -= avg_x / 2

    hand_x_max = int(round(hand_x_max))
    hand_x_min = int(round(hand_x_min))
    x = hand_x_max - hand_x_min

    hand_y_max = max(hand_y_left, hand_y_right) - 360
    hand_y = hand_y_max - y_min
    if hand_y > 256:
        avg_y = hand_y - 256
        hand_y_max -= avg_y / 2
        y_min += avg_y / 2
    elif hand_y < 256:
        avg_y = 256 - hand_y
        hand_y_max += avg_y / 2
        y_min -= avg_y / 2

    hand_y_max = int(round(hand_y_max))
    y_min = int(round(y_min))
    hand_y = hand_y_max - y_min

    dst = cv2.imread(img_path, cv2.IMREAD_COLOR)
    img_trim = dst[y_min:hand_y_max, hand_x_min-20:hand_x_max-20]
    cv2.imwrite(output_path, img_trim)


# Contour criteria foot
def image_resize_foot(img_path: str, output_path: str) -> None:
    src = cv2.imread(img_path, cv2.IMREAD_COLOR)

    gray = cv2.cvtColor(src, cv2.COLOR_RGB2GRAY)
    blur = cv2.GaussianBlur(gray, ksize=(3,3), sigmaX=0)
    edged = cv2.Canny(blur, 10, 250)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7,7))
    ret, binary = cv2.threshold(edged, 127, 255, cv2.THRESH_TOZERO)
    binary = cv2.bitwise_not(binary)

    contours, hierarchy = cv2.findContours(binary, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_TC89_KCOS)

    for i in range(len(contours)):
        cv2.drawContours(src, [contours[i]], 0, (0, 255, 0), 2)
        cv2.putText(src, str(i), tuple(contours[i][0][0]), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 255, 0), 1)
    
    contours_xy = np.array(contours)

    hand_x_min, hand_x_max = float('inf'), float('-inf')
    hand_y_left, hand_y_right = 0, 0
    for i in range(len(contours_xy)):
        for j in range(len(contours_xy[i])):
            if not contours_xy[i][j][0][0] == 0 and hand_x_min > contours_xy[i][j][0][0]:
                hand_x_min = contours_xy[i][j][0][0]
                hand_y_left = contours_xy[i][j][0][1]
            if not contours_xy[i][j][0][0] == 500 and hand_x_max < contours_xy[i][j][0][0]:
                hand_x_max = contours_xy[i][j][0][0]
                hand_y_right = contours_xy[i][j][0][1]
        
    y_min, y_max = 0,0
    value = list()
    for i in range(len(contours_xy)):
        for j in range(len(contours_xy[i])):
            value.append(contours_xy[i][j][0][1])
    value.sort()
    y_min = value[2]
    y_max = value[-3]

    x = hand_x_max - hand_x_min
    if x > 256:
        avg_x = x - 256
        hand_x_max -= avg_x / 2
        hand_x_min += avg_x / 2
    elif x < 256:
        avg_x = 256 - x
        hand_x_max += avg_x / 2
        hand_x_min -= avg_x / 2

    hand_x_max = int(round(hand_x_max))
    hand_x_min = int(round(hand_x_min))
    x = hand_x_max - hand_x_min

    point_y = (y_max + y_min) / 2
    point_y = int(point_y)

    w = (point_y - y_min) / 4
    w = int(w)
    
    new_y_min = y_min + w
    new_y_max = point_y + w
    y = new_y_max - new_y_min
    if y > 256:
        avg_y = y - 256
        new_y_max -= avg_y / 2
        new_y_min += avg_y / 2
    elif y < 256:
        avg_y = 256 - y
        new_y_max += avg_y / 2
        new_y_min -= avg_y / 2

    new_y_max = int(round(new_y_max))
    new_y_min = int(round(new_y_min))
    y = new_y_max - new_y_min

    dst = cv2.imread(img_path, cv2.IMREAD_COLOR)
    img_trim = dst[new_y_min-50:new_y_max-50, hand_x_min-20:hand_x_max-20]
    cv2.imwrite(output_path, img_trim)

def process(opt: str) -> None:
    error_hand = []
    error_foot = []

    root_dir = 'C:/SGM_AI/42Brick/img_human_filter'

    for (root, dirs, files) in os.walk(root_dir):
        if len(files) > 0: 
            for file_name in files:
                if os.path.splitext(file_name)[1] == '.jpg':
                    img_url = root.replace('\\', '/') + '/' + file_name
                    if opt == "hand":
                        try:
                            output_url = 'C:/SGM_AI/42Brick/img_resize_hand/' + file_name
                            image_resize_hand(img_url, output_url)
                        except:
                            error_hand.append(file_name) #serial number만 저장하기
                            continue
                    else:
                        try:
                            output_url = 'C:/SGM_AI/42Brick/img_resize_foot/' + file_name
                            image_resize_foot(img_url, output_url)
                        except:
                            error_foot.append(file_name)
                            continue

    print("-" * 50)

    if opt == "hand":
        print(len(error_hand),"개 문제 발생")
    else:
        print(len(error_foot),"개 문제 발생")
    

def main():
    
    if not os.path.exists("C:/SGM_AI/42Brick/img_resize_hand"):
        os.makedirs("C:/SGM_AI/42Brick/img_resize_hand")
    if not os.path.exists("C:/SGM_AI/42Brick/img_resize_foot"):
        os.makedirs("C:/SGM_AI/42Brick/img_resize_foot")

    opt = "foot"
    process(opt)
    
if __name__ == "__main__":
    main()