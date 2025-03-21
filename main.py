import cv2
import utils
from imageSimilarity import image_similarity
from datetime import datetime
from confusionMatrixConstructor import construct_confusion_matrix

construct_confusion_matrix()
#
# expected_text = "C"
# ocr_text = "Ć"
#
# print(f"Comparing text \nA: {ocr_text}\nB: {expected_text}")
# # IMAGE SAVE
# utils.save_images(expected_text, ocr_text, squish=True)
#
# # TEXT CONVERSION
# images = utils.text_to_images(expected_text, ocr_text)
# expected_img = images[0]
# ocr_img = images[1]
#
# score = image_similarity(expected_img, ocr_img)
#
# print(f"Comparison score: {score}")
