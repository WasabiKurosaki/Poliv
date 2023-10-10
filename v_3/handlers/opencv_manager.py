import numpy as np
import cv2
from PIL import Image
from settings import recommended_fertz_for_pixel, common_folder_to_save_png
import settings


gradient_dict = {
    "red_hight": (8, 8, 224),
    "red_medium": (71, 71, 180),
    "red_low": (65, 65, 146),
    "yellow_hight": (94, 194, 211),
    "yellow_low": (91, 214, 199),
    "green_hight": (76, 162, 122),
    "green_medium": (61, 203, 137),
    "green_low": (0, 212, 114),
    "gray": (207, 217, 216),
}


class OpencvManager:
    def __init__(self) -> None:
        pass

    def pil2numpy(img: Image = None) -> np.ndarray:
        """
        Convert an HxW pixels RGB Image into an HxWx3 numpy ndarray
        """

        if img is None:
            img = Image.open(
                "/home/wasabi/Desktop/UAF/PolivProcessing/Poliv/img_1.jpeg"
            )

        np_array = np.asarray(img)
        return np_array

    def save_matrix_to_png(self, matrix_to_save):
        cv2.imwrite(common_folder_to_save_png + "/output.png", matrix_to_save)

    def prepare_matrix_to_colour(self, matrix_to_save: np.array) -> np.array:
        image_blank = np.zeros(
            (matrix_to_save.shape[0], matrix_to_save.shape[1], 3), np.uint8
        )
        for y_val in range(len(matrix_to_save)):  # это мы проходим по условной длине
            for x_val in range(len(matrix_to_save[y_val])):
                # print(x_val)
                if matrix_to_save[y_val][x_val] >= recommended_fertz_for_pixel * 2.5:
                    image_blank[y_val][x_val] = gradient_dict.get("red_hight")
                elif matrix_to_save[y_val][x_val] >= recommended_fertz_for_pixel * 2.2:
                    image_blank[y_val][x_val] = gradient_dict.get("red_medium")
                elif matrix_to_save[y_val][x_val] >= recommended_fertz_for_pixel * 2:
                    image_blank[y_val][x_val] = gradient_dict.get("red_low")
                elif matrix_to_save[y_val][x_val] >= recommended_fertz_for_pixel * 1.7:
                    image_blank[y_val][x_val] = gradient_dict.get("yellow_hight")
                elif matrix_to_save[y_val][x_val] >= recommended_fertz_for_pixel * 1.4:
                    image_blank[y_val][x_val] = gradient_dict.get("yellow_low")
                elif matrix_to_save[y_val][x_val] >= recommended_fertz_for_pixel * 1.3:
                    image_blank[y_val][x_val] = gradient_dict.get("green_hight")
                elif matrix_to_save[y_val][x_val] >= recommended_fertz_for_pixel * 0.8:
                    image_blank[y_val][x_val] = gradient_dict.get("green_medium")
                elif matrix_to_save[y_val][x_val] >= recommended_fertz_for_pixel * 0.6:
                    image_blank[y_val][x_val] = gradient_dict.get("green_low")
                elif matrix_to_save[y_val][x_val] >= recommended_fertz_for_pixel * 0.2:
                    image_blank[y_val][x_val] = gradient_dict.get("gray")

        return image_blank

    def try_to_transporant(self):
        src = cv2.imread(
            common_folder_to_save_png + "/output_new_colour.png",
            1,
        )
        tmp = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
        _, alpha = cv2.threshold(tmp, 0, 255, cv2.THRESH_BINARY)

        b, g, r = cv2.split(src)
        rgba = [b, g, r, alpha]
        dst = cv2.merge(rgba, 4)

        cv2.imwrite(common_folder_to_save_png + "/try_to_transport.png", dst)

    def open_small_map(slef):
        src = cv2.imread(common_folder_to_save_png + "/small_map.png", 1)
        print(type(src))

    def colour_image_matrix(self, matrix_to_save: np.array, norm_coeff_80):
        self.norm_coeff_80 = norm_coeff_80
        ans = self.prepare_matrix_to_colour(matrix_to_save)
        cv2.imwrite(common_folder_to_save_png + "/output.png", matrix_to_save)
        cv2.imwrite(common_folder_to_save_png + "/output_new_colour.png", ans)
        self.try_to_transporant()
        self.overlay_images()

    def blur_image(self):
        image = cv2.imread("/home/wasabi/Desktop/UAF/PolivProcessing/Poliv/v_2/png_try/output_new_colour_black_back.png")

        # Gaussian Blur
        Gaussian = cv2.GaussianBlur(image,(15,15), 0) 
        cv2.imwrite("Median Blurring" + ".jpg", Gaussian)

    def overlay_images(self):
        background = cv2.imread(settings.path_to_small_map)
        dim = background.shape
        width_pers = 5
        height_pesr = 5
        background = background[200:4400, 200:4300][:]

        overlay = cv2.imread(settings.path_to_saved_mission)
        background = cv2.resize(background, (overlay.shape[1], overlay.shape[0]))
        added_image = cv2.addWeighted(background, 0.9, overlay, 0.8, 0)

        cv2.imwrite(common_folder_to_save_png + "/combined.png", added_image)
