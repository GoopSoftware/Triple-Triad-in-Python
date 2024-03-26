import cv2
import pytesseract
import numpy as np

image_path = 'downloaded_images/testocr.png'

image = cv2.imread(image_path)

gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

_, binary_image = cv2.threshold(gray_image, 0, 255,
                                cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

for contour in contours:
    x, y, w, h = cv2.boundingRect(contour)

    roi = binary_image[y:y+h, x:x+w]

    number = pytesseract.image_to_string(roi, config='--psm 6 digits')

    print("Extracted Number:", number)

cv2.imshow('Original Image', image)
cv2.waitKey(0)
cv2.destroyAllWindows()