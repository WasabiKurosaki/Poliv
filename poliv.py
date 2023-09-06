import numpy as np
from scipy.spatial import ConvexHull
from scipy.spatial.distance import cdist
import math


class GeometryHelper:

    @staticmethod
    def euler_from_quaternion(x, y, z, w):
        """
        Convert a quaternion into euler angles (roll, pitch, yaw)
        roll is rotation around x in radians (counterclockwise)
        pitch is rotation around y in radians (counterclockwise)
        yaw is rotation around z in radians (counterclockwise)
        """
        t0 = +2.0 * (w * x + y * z)
        t1 = +1.0 - 2.0 * (x * x + y * y)
        roll_x = math.atan2(t0, t1)

        t2 = +2.0 * (w * y - z * x)
        t2 = +1.0 if t2 > +1.0 else t2
        t2 = -1.0 if t2 < -1.0 else t2
        pitch_y = math.asin(t2)

        t3 = +2.0 * (w * z + x * y)
        t4 = +1.0 - 2.0 * (y * y + z * z)
        yaw_z = math.atan2(t3, t4)

        return roll_x, pitch_y, yaw_z  # in radians
    
    # @staticmethod
    # def tg_from_angle(angle):
    #     return math.tan(angle)


class OpencvMatrix:
    def __init__(self, pix_meter: int, x_list: list, y_list: list):
        self.create_cv_matrix(
            pix_meter, x_list, y_list
        )  # создается наша матрица np и задается ск

    def create_cv_matrix(self, pix_meter: int, x_list: list, y_list: list) -> None:
        matrix_rows, matrix_columns = self.get_width_and_length(
            pix_meter, x_list, y_list
        )
        self.pix_meter = pix_meter
        self.zero_point_of_our_coordinate_system = min(x_list), min(y_list)
        self.matrix_rows = matrix_rows
        self.matrix_columns = matrix_columns
        self.matrix = np.zeros((matrix_rows, matrix_columns))

    def put_point_in_matrix(self, x_uav: float, y_uav: float, value: int) -> tuple:
        (
            x_coord_in_our_system,
            y_coord_in_our_system,
        ) = self.translate_into_our_coordinate_system(x_uav, y_uav)
        self.matrix[-y_coord_in_our_system, x_coord_in_our_system] = value
        # print(self.matrix[-y_coord_in_our_system, x_coord_in_our_system])

    def translate_into_our_coordinate_system(self, x_uav: float, y_uav: float) -> tuple:
        """
        Перемещаем саму СК в левый нижний угол нашей матрицы + домножаем на pixel_meter.
        Возвращаем координаты в нашей ск в виде tuple(int, int).
        После следует перевести в виде индексов в матрицу numpy, не забыть!
        """
        x_coord_in_our_system = int(
            (x_uav - self.zero_point_of_our_coordinate_system[0]) * self.pix_meter
        )
        y_coord_in_our_system = int(
            (y_uav - self.zero_point_of_our_coordinate_system[1]) * self.pix_meter
        )
        return x_coord_in_our_system, y_coord_in_our_system

    @staticmethod
    def calculate_spray_cone_size(z: float, cone_apex_triangle_angle: float):
        """
        Высчитываем размеры конуса распыления в метрах 
        """

        return math.tan(cone_apex_triangle_angle) * z * 2
    
    def calculate_spray_cone_centre(self, ):
        pass
    
    def spray_on_neigh_cells():
        ...

    @staticmethod
    def get_width_and_length(pix_meter: int, x_list: list, y_list: list) -> tuple:
        """
        Находим высоту и ширину для картинки в метрах
        """
        h_matrix = max(y_list) - min(y_list)
        w_matrix = max(x_list) - min(x_list)

        return pix_meter * h_matrix, pix_meter * w_matrix


class Poliv:
    def __init__(self):
        ...


test_obj = OpencvMatrix(3, x_list=[1156, 1226, 1050, 980], y_list=[811, 880, 1058, 988])
# print(test_obj.put_point_in_matrix(1000, 811, 2))
print(test_obj.calculate_spray_cone_size(10, 0.349066))
