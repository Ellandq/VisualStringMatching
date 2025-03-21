import cv2
import numpy as np
from skimage.metrics import structural_similarity as ssim

isLogging = False


def image_similarity(img1, img2) -> float:
    if img1 is None or img2 is None:
        raise ValueError("One or both images are invalid (None). Check image loading.")

    # Resize to a fixed size while maintaining aspect ratio
    standard_size = (150, 150)
    img1 = cv2.resize(img1, standard_size, interpolation=cv2.INTER_CUBIC)
    img2 = cv2.resize(img2, standard_size, interpolation=cv2.INTER_CUBIC)

    # Convert to grayscale
    gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

    # SSIM Score
    ssim_score, _ = ssim(gray1, gray2, full=True)

    # MSE Score
    mse = np.mean((gray1 - gray2) ** 2)
    mse_score = 1 / (1 + mse)

    # Histogram Comparison
    hist1 = cv2.calcHist([gray1], [0], None, [256], [0, 256])
    hist2 = cv2.calcHist([gray2], [0], None, [256], [0, 256])
    cv2.normalize(hist1, hist1)
    cv2.normalize(hist2, hist2)
    hist_score = cv2.compareHist(hist1, hist2, cv2.HISTCMP_CORREL)

    # Edge Difference using Canny
    edges1 = cv2.Canny(gray1, 100, 200)
    edges2 = cv2.Canny(gray2, 100, 200)
    edge_diff = abs(np.mean(np.abs(edges1 - edges2)) / 255.0 - 1)

    # Combine scores (weighted)
    if isLogging:
        print(f"SSIM: {ssim_score}")
        print(f"MSE: {mse_score}")
        print(f"HIST: {hist_score}")
        print(f"EDGE: {edge_diff}")
    final_score = (0.4 * ssim_score) + (0.2 * mse_score) + (0.3 * hist_score) + (0.1 * edge_diff)

    return round(final_score, 4)
