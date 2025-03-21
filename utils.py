from PIL import Image, ImageDraw, ImageFont
import cv2
import numpy as np
import os
from datetime import datetime

FONT_PATH = os.path.join(os.path.dirname(__file__), "fonts", "calibri-regular.ttf")


def text_to_images(*texts, font_size=64, padding=10, squish=False, overlap_factor=0.3):
    """
    Converts multiple text strings into images of the same size, with optional squishing (overlapping effect).
    :param texts: Variable-length list of text strings
    :param font_size: Font size for rendering
    :param padding: Padding around text
    :param squish: If True, reduces spacing between letters (overlapping effect)
    :param overlap_factor: Controls how much letters overlap (0.0 = no overlap, 0.5 = half overlap)
    :return: List of images (NumPy arrays)
    """
    try:
        font = ImageFont.truetype(FONT_PATH, font_size)
    except IOError:
        raise ValueError(f"Font file not found: {FONT_PATH}")

    # Get font metrics to determine the max ascender and descender
    ascent, descent = font.getmetrics()
    max_char_height = ascent + descent

    img_height = int(max_char_height + 2 * padding)
    max_width = max(font.getbbox(text)[2] - font.getbbox(text)[0] for text in texts)
    img_width = int(max_width + 2 * padding)

    images = []
    for text in texts:
        image = Image.new("RGB", (img_width, img_height), "white")
        draw = ImageDraw.Draw(image)

        if squish:
            # Overlapping effect
            x_offset = padding
            for char in text:
                char_width = font.getbbox(char)[2] - font.getbbox(char)[0]
                char_ascent, char_descent = font.getmetrics()

                # Aligning all characters to a consistent baseline
                text_y = padding + (ascent - char_ascent)

                draw.text((x_offset, text_y), char, fill="black", font=font)
                x_offset += char_width - (char_width * overlap_factor)
        else:
            # Center entire text block
            text_width = sum(font.getbbox(char)[2] - font.getbbox(char)[0] for char in text)
            text_x = (img_width - text_width) // 2
            text_y = padding

            draw.text((text_x, text_y), text, fill="black", font=font)

        # Convert to OpenCV format
        image_cv = np.array(image, dtype=np.uint8)
        image_cv = cv2.cvtColor(image_cv, cv2.COLOR_RGB2BGR)

        images.append(image_cv)

    return images


def save_images(expected_text, ocr_text, squish=False):
    """
    Saves the expected and OCR text images to a new timestamped folder.
    :param expected_text: Correct text string
    :param ocr_text: OCR-extracted text string
    :param squish: If True, reduces spacing between letters
    """
    # Creating output folder
    base_dir = "output"
    os.makedirs(base_dir, exist_ok=True)

    # Creating sub-folder
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    run_folder = os.path.join(base_dir, timestamp)
    os.makedirs(run_folder, exist_ok=True)

    # Generate images with the same size
    expected_img, ocr_img = text_to_images(expected_text, ocr_text, squish=squish)

    # Save images
    expected_path = os.path.join(run_folder, "expected.png")
    ocr_path = os.path.join(run_folder, "ocr_output.png")

    cv2.imwrite(expected_path, expected_img)
    cv2.imwrite(ocr_path, ocr_img)

    print(f"Images saved in: {run_folder}")


def min_max_scale_list_of_lists(data):
    # Flatten the list of lists to get the global min and max
    flattened = np.array([item for sublist in data for item in sublist])

    # Compute min and max
    min_val, max_val = np.min(flattened), np.max(flattened)
    if max_val == min_val:
        return [[0.0 for _ in sublist] for sublist in data]

    # Scale all values
    scaled_flattened = (flattened - min_val) / (max_val - min_val)

    # Reshape back to original structure
    scaled_data = []
    index = 0
    for sublist in data:
        scaled_data.append(scaled_flattened[index:index + len(sublist)].tolist())
        index += len(sublist)

    return scaled_data
