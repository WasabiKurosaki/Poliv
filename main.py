import settings
from poliv_handler import Poliv
from matrix_handler import OpencvMatrix
import time


test_obj = OpencvMatrix(4, x_list=[1156, 1226, 1050, 980], y_list=[811, 880, 1058, 988])
poliv = Poliv(matrix_handler=test_obj)
for i in range(10):
    poliv.catch_point_and_place_on_matrix()
    time.sleep(2)

poliv.save_matrix_to_jpeg()
