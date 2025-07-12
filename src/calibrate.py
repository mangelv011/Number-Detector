import os
import cv2
import imageio
import numpy as np
from typing import List, Tuple
import glob
import shutil
import matplotlib.pyplot as plt
from skimage import filters, feature, io, color
import copy
#####################CREAMOS LAS FUNCIONES QUE VAMOS A USAR SEGURO#####################################
def load_images(filenames: List) -> List:
    return [cv2.imread(filename) for filename in filenames]
def show_image(img: np.array, img_name: str = "Image"):
    cv2.imshow(img_name,img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
def write_image(output_folder: str, img_name: str, img: np.array):
    img_path = os.path.join(output_folder, img_name)
    cv2.imwrite(img_path, img)

#####################CREAMOS LA FUNCION QUE VAMOS A USAR################################################
def lista_corners(imgs, pattern_size): 
    corners_list = []
    fails = 0
    i = 0
    for image in imgs:
        flag, corners = cv2.findChessboardCorners(image, pattern_size)
        if flag:
            corners_list.append(corners)
        else:
            fails += 1
        i += 1

    print(f"Total fails: {fails}")
    return corners_list
def lista_corners_refinado(imgs,pattern_size): 
    corners_refined_list = []
    corners_list = lista_corners(imgs,pattern_size)
    for image, corners in zip(imgs, corners_list):
        corners_copy = copy.deepcopy(corners)
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.01)

        # TODO To refine corner detections with cv2.cornerSubPix() you need to input grayscale images. Build a list containing grayscale images.
        imgs_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        corners_refined = cv2.cornerSubPix(
            imgs_gray, corners_copy, (8, 6), (-1, -1), criteria
        )

        corners_refined_list.append(corners_refined)
    return corners_refined_list
def draw_corners(imgs,corners_list,pattern_size):
    imgs_copy = copy.deepcopy(imgs)
    for image, corners in zip(imgs_copy, corners_list):
        cv2.drawChessboardCorners(image, pattern_size, corners, True)
        cv2.imshow("Esquinas del Tablero de Ajedrez", image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
def get_chessboard_points(chessboard_shape, dx, dy):
    num_filas, num_columnas = chessboard_shape
    obj_points = []
    for i in range(num_filas):
        for j in range(num_columnas):
            obj_points.append(
                [j * dx, i * dy, 0]
            )  
    obj_points = np.array(obj_points, dtype=np.float32)
    return obj_points
def calibrar_camara(imgs, pattern_size):
    corners_list = lista_corners_refinado(imgs,pattern_size)
    valid_corners = np.asarray(corners_list, dtype=np.float32)
    chessboard_points = get_chessboard_points(pattern_size, 0.03, 0.03)
    chessboard_points_list = [chessboard_points for i in range(11)]
    image_size = (imgs[0].shape[1], imgs[0].shape[0])  # Tamaño de la imagen (ancho, alto)
    rms, intrinsics, dist_coeffs, rvecs, tvecs = cv2.calibrateCamera(
    chessboard_points_list, valid_corners, image_size, None, None
    )
    # Obtain extrinsics
    extrinsics = list(
    map(lambda rvec, tvec: np.hstack((cv2.Rodrigues(rvec)[0], tvec)), rvecs, tvecs)
    )
    return rms, intrinsics, dist_coeffs, extrinsics
def main():
    pattern_size = (16,16)#Tamaño de nuestro tablero.  
    imgs_path = glob.glob("../imagenes_calibracion/*jpg")
    imgs = load_images(imgs_path)
    lista_corners_refinados = lista_corners_refinado(imgs,pattern_size)
    draw_corners(imgs,lista_corners_refinados,pattern_size)
    calibrar_camara(imgs,pattern_size)
if __name__ == "__main__": 
    main()