from PIL import Image, ImageDraw, ImageFont
import cv2
import numpy as np
import os
from datetime import datetime


def text_to_images(*texts, font_size=32, padding=10):
    """
    Converts multiple text strings into images of the same size.
    :param texts: Variable-length list of text strings
    :param font_size: Font size for rendering
    :param padding: Padding around text
    :return: List of images (NumPy arrays)
    """
    font = ImageFont.load_default()

    # Determine max width & height needed
    max_width = 0
    max_height = 0

    for text in texts:
        dummy_img = Image.new("RGB", (1, 1))
        draw = ImageDraw.Draw(dummy_img)
        text_bbox = draw.textbbox((0, 0), text, font=font)

        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]

        max_width = max(max_width, text_width)
        max_height = max(max_height, text_height)

    # Add padding
    img_width = int(max_width + 2 * padding)
    img_height = int(max_height + 2 * padding)

    images = []
    for text in texts:
        # Create image with consistent size
        image = Image.new("RGB", (img_width, img_height), "white")
        draw = ImageDraw.Draw(image)

        # Center the text within the image
        text_x = padding
        text_y = padding
        draw.text((text_x, text_y), text, fill="black", font=font)

        # Convert to OpenCV format (NumPy array)
        image_cv = np.array(image, dtype=np.uint8)
        image_cv = cv2.cvtColor(image_cv, cv2.COLOR_RGB2BGR)

        images.append(image_cv)

    return images


def save_images(expected_text, ocr_text):
    """
    Saves the expected and OCR text images to a new timestamped folder.
    :param expected_text: Correct text string
    :param ocr_text: OCR-extracted text string
    """
    # Creating output folder
    base_dir = "output"
    os.makedirs(base_dir, exist_ok=True)

    # Creating sub-folder
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    run_folder = os.path.join(base_dir, timestamp)
    os.makedirs(run_folder, exist_ok=True)

    # Generate images with the same size
    expected_img, ocr_img = text_to_images(expected_text, ocr_text)

    # Save images
    expected_path = os.path.join(run_folder, "expected.png")
    ocr_path = os.path.join(run_folder, "ocr_output.png")

    cv2.imwrite(expected_path, expected_img)
    cv2.imwrite(ocr_path, ocr_img)

    print(f"Images saved in: {run_folder}")

