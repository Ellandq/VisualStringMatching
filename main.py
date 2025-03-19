import cv2
import utils
from imageSimilarity import image_similarity
from datetime import datetime

expected_text = "Order100"
ocr_text = "Orcler100"

print(f"Comparing text \nA: {ocr_text}\nB: {expected_text}")
# IMAGE SAVE
# utils.save_images(expected_text, ocr_text)

# TEXT CONVERSION
images = utils.text_to_images(expected_text, ocr_text)
expected_img = images[0]
ocr_img = images[1]

score = image_similarity(expected_img, ocr_img)

print(f"Comparison score: {score}")
