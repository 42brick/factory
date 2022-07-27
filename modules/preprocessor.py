import os
import cv2
import numpy as np
import math
from PIL import Image
from retinaface import RetinaFace
import matplotlib.pyplot as plt

def plt_test(img_path):
    img = cv2.imread(img_path, cv2.IMREAD_COLOR)

    # resp = RetinaFace.detect_faces(img_path = img_path)
    resp = RetinaFace.extract_faces(img_path = img_path, align=True)
    for face in resp:
        plt.imshow(face)
        plt.show()

    x1, y1 = resp["face_1"]["landmarks"]["right_eye"]
    x2, y2 = resp["face_1"]["landmarks"]["left_eye"]

    y = abs(y1 - y2)
    x = abs(x2 - x1)
    sq = math.sqrt(y**2 + x**2)

    cos_alpha = (x**2 + sq**2 - y**2) / (2*x*sq)
    alpha = np.arccos(cos_alpha)
    alpha = (alpha * 180) / math.pi

    aligned_img = Image.fromarray(img)
    aligned_img = np.array(aligned_img.rotate(alpha))

    plt.imshow(aligned_img)
    plt.show()

def main():
    img_path = "C:/SGM_AI/42Brick/factory/img_human_filter/4-juniors/4j001.jpg"
    plt_test(img_path)

if __name__ == "__main__":
    main()