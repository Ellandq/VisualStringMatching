import pandas as pd
from imageSimilarity import image_similarity
from utils import text_to_images, min_max_scale_list_of_lists

characters = [
    "A", "Ą", "B", "C", "Ć", "D", "E", "Ę", "F", "G", "H", "I", "J", "K", "L", "Ł", "M", "N", "Ń", "O", "Ó", "P", "Q",
    "R", "S", "Ś", "T", "U", "V", "W", "X", "Y", "Z", "Ż", "Ź", "a", "ą", "b", "c", "ć", "d", "e", "ę", "f", "g", "h",
    "i", "j", "k", "l", "ł", "m", "n", "ń", "o", "ó", "p", "q", "r", "s", "ś", "t", "u", "v", "w", "x", "y", "z", "ż",
    "ź", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "rn", "cl", "cI", "rt", "vv", "ri", "I3", "l3"
]


def construct_confusion_matrix():
    char_count = len(characters)
    data = [[0.0 for _ in range(len(characters))] for _ in range(len(characters))]

    for i in range(char_count):
        for j in range(i + 1):
            if i == j:
                data[i][j] = 1.0
                continue

            images = text_to_images(characters[i], characters[j], font_size=64, squish=True)
            img1 = images[0]
            img2 = images[1]

            similarity_score = image_similarity(img1, img2)
            data[i][j] = similarity_score
            data[j][i] = similarity_score

    data = min_max_scale_list_of_lists(data)
    df = pd.DataFrame(data, columns=characters, index=characters)
    print(df)

    excel_filename = "confusion_matrix.xlsx"
    df.to_excel(excel_filename, sheet_name="Confusion Matrix")
    print(f"Confusion matrix saved to {excel_filename}")
