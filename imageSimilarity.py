import cv2
import numpy as np
from skimage.metrics import structural_similarity as ssim

color = cv2.COLOR_BGR2GRAY


def image_similarity(img1, img2):
    gray1 = cv2.cvtColor(img1, color)
    gray2 = cv2.cvtColor(img2, color)
    score, _ = ssim(gray1, gray2, full=True)
    return score
