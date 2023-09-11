import numpy as np
import cv2
from PIL import Image



gradient_dict = {
    1: 2
}

class OpencvManager:
    def __init__(self) -> None:
        pass



    def pil2numpy(img: Image = None) -> np.ndarray:
        """
        Convert an HxW pixels RGB Image into an HxWx3 numpy ndarray
        """

        if img is None:
            img = Image.open('/home/wasabi/Desktop/UAF/PolivProcessing/Poliv/img_1.jpeg')

        np_array = np.asarray(img)
        return np_array

    def save_matrix_to_png(self, matrix_to_save):
        cv2.imwrite("output.png", matrix_to_save)

    def colour_image_matrix(self, matrix_to_save: np.array):
        try_to_colour = np.zeros((*matrix_to_save.shape, 3))
        for i in range(len(matrix_to_save)):
            # print(matrix_to_save[i][2])
            if matrix_to_save[i][2] >=0:
                try_to_colour[i][1:50] = (0, 0, 250) # bgr

        cv2.imwrite("try_to_colour.png", try_to_colour)

    def blur_image(image_path):
        image = cv2.imread(image_path)

        # Gaussian Blur
        Gaussian = cv2.medianBlur(image, 5)# (15, 15), cv2.BORDER_DEFAULT)
        cv2.imwrite('Median Blurring' + '.jpg', Gaussian)

    def overlay_images(self):

        # read foreground image
        img = cv2.imread('output.png', cv2.IMREAD_UNCHANGED)

        # read background image
        back = cv2.imread('small_map.png')

        # extract alpha channel from foreground image as mask and make 3 channels
        alpha = img[:,:,3]
        alpha = cv2.merge([alpha,alpha,alpha])

        # extract bgr channels from foreground image
        front = img[:,:,0:3]

        # blend the two images using the alpha channel as controlling mask
        result = np.where(alpha==(0,0,0), back, front)

        # save result
        cv2.imwrite("front_back.png", result)


# OpencvManager.blur_image('/home/wasabi/Desktop/UAF/PolivProcessing/Poliv/v_2/output.png')
# print(OpencvManager.pil2numpy())
