import cv2

import numpy as np

track_window = None

def show_image(img: np.array, img_name: str = "Image"):
    cv2.imshow(img_name,img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
def color_segment(img):
    hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
    # Definir el rango de verde claro en HSV
    # Aproximación: H para verde claro ~ 40-80, S alta (por ejemplo, 100-255) y V moderado a alto (50-255)
    lower_green = np.array([40, 30, 20])   # Rango inferior para verde muy oscuro (S y V más bajos)
    upper_green = np.array([80, 255, 255])  # Rango superior para verde claro a verde más oscuro
    
    
    # Crear la máscara para el verde claro
    green_mask = cv2.inRange(hsv_img, lower_green, upper_green)

    
    
    # Aplicar la máscara para obtener solo el segmento verde
    green_segmented = cv2.bitwise_and(img, img, mask=green_mask)

     # Definir un kernel para la dilatación (puede ser rectangular, elíptico, o cruzado)
    kernel = np.ones((8, 8), np.uint8)  # Un kernel de 5x5 de unos (puedes ajustarlo)
    
    # Aplicar dilatación para unir las áreas cercanas
    dilated_mask = cv2.dilate(green_mask, kernel, iterations=1)  # Puedes ajustar el número de iteraciones
    
    # Aplicar la máscara dilatada para obtener solo el segmento verde
    green_segmented = cv2.bitwise_and(img, img, mask=dilated_mask)

    return dilated_mask, green_segmented




def extract_number_from_image(green_mask: np.array, img: np.array) -> np.array:
    global track_window
    # Encontrar los contornos en la máscara roja
    contours, _ = cv2.findContours(green_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if contours:
        # Encontrar el contorno más grande, que debería corresponder al número
        largest_contour = max(contours, key=cv2.contourArea)
        
        # Obtener la caja delimitadora (bounding box) del contorno más grande
        x, y, w, h = cv2.boundingRect(largest_contour)


        ## SEGUIMIENTO
        track_window = (x, y, w, h)

        # Recortar la imagen usando la caja delimitadora
        cropped_img = img[y:y+h, x:x+w]
        return cv2.resize(cropped_img, (264,264), interpolation=cv2.INTER_LINEAR)
    else:
        # Si no se encuentra un contorno, devolver la imagen original
        return img



def detect_number(cropped_resized_img):
    '''Función para detectar número comparando los templates de las fotos'''
    digit_templates = [cv2.imread(f'../images/cropped_images/{i}.png', cv2.IMREAD_GRAYSCALE) for i in range(10)]
    cropped_resized_img = np.uint8(cropped_resized_img)
    digit_templates = [np.uint8(template) for template in digit_templates]
    cropped_resized_img = cv2.cvtColor(cropped_resized_img, cv2.COLOR_BGR2GRAY)
    best_match = None
    best_match_score = -1
    for i, template in enumerate(digit_templates):
        res = cv2.matchTemplate(cropped_resized_img, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        # Si encontramos una coincidencia mejor que la anterior
        if max_val > best_match_score:
            best_match_score = max_val
            best_match = i
    return best_match




def make_detection():
    img = cv2.imread(f'../images/temp.jpg')
    img = cv2.resize(img, (264,264), interpolation=cv2.INTER_LINEAR)
    green_mask,green_segmented = color_segment(img)
    resized_image = extract_number_from_image(green_mask, img)
    cv2.imwrite('../images/cropped.jpg', resized_image)
    detected = detect_number(resized_image)
    return detected

