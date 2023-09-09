import numpy as np
from scipy.spatial import ConvexHull
from scipy.spatial.distance import cdist
import math
import itertools
import scipy as sp
from scipy import stats


class OpencvMatrix:
    def __init__(self, pix_meter: int, x_list: list, y_list: list):
        self.x_point_of_searching_sqr = x_list
        self.y_point_of_searching_sqr = y_list
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

    def put_point_in_matrix(self, x_uav: float, y_uav: float, value: int) -> None:
        (
            x_coord_in_our_system,
            y_coord_in_our_system,
        ) = self.translate_into_our_coordinate_system(x_uav, y_uav)
        self.matrix[-y_coord_in_our_system, x_coord_in_our_system] = value

    def put_point_from_our_coord_in_matrix(
        self, x_coord_in_our_system: float, y_coord_in_our_system: float, value: int
    ) -> None:
        """Вносим наши координаты точки и пополяем нашу матрицу переданным значением"""
        self.matrix[-int(y_coord_in_our_system), int(x_coord_in_our_system)] += value

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
    def calculate_spray_cone_size(
        z: float, cone_apex_triangle_angle: float = 20
    ) -> float:
        """
        Высчитываем размеры конуса распыления в метрах, передаем высоту и 2д угол конуса.
        """
        return math.tan(cone_apex_triangle_angle) * z * 2

    @staticmethod
    def calculate_spray_cone_center(
        x_poix_point_in_our_system: float,
        y_point_in_our_system: float,
        n_bias_meter: int = 1,
        x_rad_angle: float = 1,
        y_rad_angle: float = 1,
    ) -> tuple:
        """
        Вычисляем центр конуса в наших координатах (со смещение на n_bias_meter метров)
        """
        # пускай сейчас он просто под собой рисует конус
        return x_poix_point_in_our_system, y_point_in_our_system

    @staticmethod
    def calculate_included_spray_points(
        x_center: float,
        y_center: float,
        x_point_in_our_system: float,
        y_point_in_our_system: float,
        spray_cone_size: float,
    ) -> list:
        """
        По входящим точкам в нашей системе координат выдается списком все возможные точки, находящиеся внутри нашего конуса
        + выдает значения
        """

        def __add_pollinating_liquid_values(
            x_center: float,
            y_center: float,
            x_px_point_in_our_systemoint: float,
            y_point_in_our_system: float,
            coef=10,  # вот этот коэффициент желательно подогнать
        ):
            try:
                if (
                    abs(x_center - x_px_point_in_our_systemoint)
                    + abs(y_center - y_point_in_our_system)
                ):
                    return 10 / (
                        abs(x_center - x_px_point_in_our_systemoint)/5
                        + abs(y_center - y_point_in_our_system)/5
                    )  * coef
                else:
                    return 0  # coef * 4
            except Exception as e:
                print(e)
                print("ERROR:", x_center, x_point_in_our_system)
                return coef * 3

        x_list = np.array(
            [
                x
                for x in range(
                    x_point_in_our_system + int(-spray_cone_size / 2),
                    x_point_in_our_system + int(spray_cone_size / 2) + 1,
                )
            ]
        )
        y_list = np.array(
            [
                y
                for y in range(
                    y_point_in_our_system + int(-spray_cone_size / 2),
                    y_point_in_our_system + int(spray_cone_size / 2) + 1,
                )
            ]
        )
        all_points_included_in_our_con = np.array(
            list(itertools.product(x_list, y_list))
        )
        ans_array = arr = np.zeros([len(all_points_included_in_our_con), 3])
        for i in range(len(all_points_included_in_our_con)):
            ans_array[i] = (
                all_points_included_in_our_con[i][0],
                all_points_included_in_our_con[i][1],
                __add_pollinating_liquid_values(
                    all_points_included_in_our_con[i][0],
                    all_points_included_in_our_con[i][1],
                    x_center,
                    y_center,
                ),
            )

        return ans_array

    def spray_on_neigh_cells(self, point_list: np.array) -> None:
        """
        Заносит в нашу матрицу все точки, которые были указаны во входящих данные
        """

        for point in point_list:
            # print(point)
            self.put_point_from_our_coord_in_matrix(
                x_coord_in_our_system=point[0],
                y_coord_in_our_system=point[1],
                value=point[2],
            )

    def make_one_full_iteration(self, x_uav: float, y_uav: float, z_uav: float):
        """
        Полная итерация для одной точки
        """

        # проверяем находит ли наша точка внутри нашей исследуемой площади
        if self.inPolygon(x=x_uav, y=y_uav):
            # нам приходит точка в координатах симулятор, мы ее переводим в наши координаты
            (
                x_coord_in_our_system,
                y_coord_in_our_system,
            ) = self.translate_into_our_coordinate_system(x_uav=x_uav, y_uav=y_uav)

            # вычисляем необходимые данные о конусе: его ширину основания и координаты центра
            x_center, y_center = self.calculate_spray_cone_center(
                x_poix_point_in_our_system=x_coord_in_our_system,
                y_point_in_our_system=y_coord_in_our_system,
                x_rad_angle=1,
                y_rad_angle=1,
                n_bias_meter=1,
            )
            spray_cone_size = self.calculate_spray_cone_size(
                z=z_uav, cone_apex_triangle_angle=10
            )

            # подсчитываем какие точки попадают под наш конус
            point_list = self.calculate_included_spray_points(
                x_center=x_center,
                y_center=y_center,
                x_point_in_our_system=x_coord_in_our_system,
                y_point_in_our_system=y_coord_in_our_system,
                spray_cone_size=spray_cone_size,
            )

            # нормализуем данные
            Gauss = lambda t: t / max(point_list[:, 2]) * 256  # A*np.exp(-1*B*t**2)
            # print(point_list[:,2])
            point_list[:, 2] = Gauss(point_list[:, 2])

            # отсеим наши точки по принципу удаленности от центра:
            def check_if_close(x1, x2, y1, y2, spray_cone_size):
                distance = ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5
                # print(distance, spray_cone_size)

                if distance <= spray_cone_size / 2:
                    return True
                else:
                    return False

            ans_list = []
            for i in range(len(point_list)):
                if check_if_close(
                    x1=point_list[i][0],
                    y1=point_list[i][1],
                    x2=x_center,
                    y2=y_center,
                    spray_cone_size=spray_cone_size,
                ):
                    ans_list.append(point_list[i])
                else:
                    pass

            # наносим значения распыления на нашу матрицу для этих точек
            self.spray_on_neigh_cells(point_list=ans_list)

            print("\nSucsesfully added point on matrix")

            print("Минимальное значение в нашей матрице:", self.matrix.min())
            print("Среднее значение в нашей матрице:", self.matrix.mean())
            print("Максимальное значение в нашей матрице:", self.matrix.max())
            print("Размер нашей матрицы:", self.matrix.shape)
        else:
            print("\nNow our drone is out of range")

    @staticmethod
    def get_width_and_length(pix_meter: int, x_list: list, y_list: list) -> tuple:
        """
        Находим высоту и ширину для картинки в метрах
        """
        h_matrix = max(y_list) - min(y_list)
        w_matrix = max(x_list) - min(x_list)

        return pix_meter * h_matrix, pix_meter * w_matrix

    def inPolygon(self, x: float, y: float) -> bool:
        xp = self.x_point_of_searching_sqr
        yp = self.y_point_of_searching_sqr
        c = 0
        for i in range(len(xp)):
            if ((yp[i] <= y and y < yp[i - 1]) or (yp[i - 1] <= y and y < yp[i])) and (
                x > (xp[i - 1] - xp[i]) * (y - yp[i]) / (yp[i - 1] - yp[i]) + xp[i]
            ):
                c = 1 - c
        return c == 1


test_obj = OpencvMatrix(4, x_list=[1156, 1226, 1050, 980], y_list=[811, 880, 1058, 988])
test_obj.make_one_full_iteration(1100, 900, 10)


# x_data = np.arange(-5, 5, 0.001)
# y_data = stats.norm.pdf(x_data, 0, 1)
# print(type(y_data))

# print(test_obj.put_point_in_matrix(1000, 811, 2))
# print(test_obj.calculate_included_spray_points(40, 20, 50, 20, 10))


# qt_example = {
#     "x": 0.004066310721529469,
#     "y": 0.011969491783947003,
#     "z": 0.15292339132282898,
#     "w": 0.9881571903143117,
# }
# test_helper = GeometryHelper.euler_from_quaternion(**qt_example)
# print(test_helper)

# def inPolygon(x, y, xp, yp):
#     c=0
#     for i in range(len(xp)):
#         if (((yp[i]<=y and y<yp[i-1]) or (yp[i-1]<=y and y<yp[i])) and
#             (x > (xp[i-1] - xp[i]) * (y - yp[i]) / (yp[i-1] - yp[i]) + xp[i])): c = 1 - c
#     return c==1

# print( inPolygon(100, 1000, (-100, 100, 100, -100), (100, 100, -100, -100)))
