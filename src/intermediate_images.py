import cv2
import numpy as np

track_window = None

def show_image(img: np.array, img_name: str = "Image"):
    cv2.imshow(img_name, img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def color_segment(img):
    hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    show_image(hsv_img, "HSV Image")
    
    # Definir el rango de verde claro en HSV
    lower_green = np.array([40, 30, 20])   # Rango inferior para verde muy oscuro (S y V más bajos)
    upper_green = np.array([80, 255, 255])  # Rango superior para verde claro a verde más oscuro
    
    # Crear la máscara para el verde claro
    green_mask = cv2.inRange(hsv_img, lower_green, upper_green)
    show_image(green_mask, "Green Mask")
    
    # Aplicar la máscara para obtener solo el segmento verde
    green_segmented = cv2.bitwise_and(img, img, mask=green_mask)
    show_image(green_segmented, "Green Segmented (Before Dilation)")

    # Definir un kernel para la dilatación
    kernel = np.ones((8, 8), np.uint8)  # Kernel de 8x8
    dilated_mask = cv2.dilate(green_mask, kernel, iterations=1)
    show_image(dilated_mask, "Dilated Mask")
    
    # Aplicar la máscara dilatada
    green_segmented = cv2.bitwise_and(img, img, mask=dilated_mask)
    show_image(green_segmented, "Green Segmented (After Dilation)")

    return dilated_mask, green_segmented

def extract_number_from_image(green_mask: np.array, img: np.array) -> np.array:
    global track_window
    contours, _ = cv2.findContours(green_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if contours:
        largest_contour = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(largest_contour)
        track_window = (x, y, w, h)
        cropped_img = img[y:y+h, x:x+w]
        cropped_img_resized = cv2.resize(cropped_img, (264, 264), interpolation=cv2.INTER_LINEAR)
        show_image(cropped_img_resized, "Cropped and Resized Image")
        return cropped_img_resized
    else:
        show_image(img, "Original Image (No Contour Found)")
        return img

def detect_number(cropped_resized_img):
    digit_templates = [cv2.imread(f'../images/cropped_images/{i}.png', cv2.IMREAD_GRAYSCALE) for i in range(10)]
    cropped_resized_img_gray = cv2.cvtColor(cropped_resized_img, cv2.COLOR_BGR2GRAY)
    show_image(cropped_resized_img_gray, "Cropped Image in Grayscale")
    best_match = None
    best_match_score = -1
    for i, template in enumerate(digit_templates):
        res = cv2.matchTemplate(cropped_resized_img_gray, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        if max_val > best_match_score:
            best_match_score = max_val
            best_match = i
    return best_match

def make_detection():
    img = cv2.imread(f'../images/temp.jpg')
    img = cv2.resize(img, (264, 264), interpolation=cv2.INTER_LINEAR)
    show_image(img, "Original Image")
    
    green_mask, green_segmented = color_segment(img)
    resized_image = extract_number_from_image(green_mask, img)
    cv2.imwrite('../images/cropped.jpg', resized_image)
    detected = detect_number(resized_image)
    
    print(f"Detected Number: {detected}")
    return detected
make_detection()