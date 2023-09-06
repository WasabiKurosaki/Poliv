import numpy as np
from scipy.spatial import ConvexHull
from scipy.spatial.distance import cdist
import math
import itertools

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

    def put_point_in_matrix(self, x_uav: float, y_uav: float, value: int) -> None:
        (
            x_coord_in_our_system,
            y_coord_in_our_system,
        ) = self.translate_into_our_coordinate_system(x_uav, y_uav)
        self.matrix[-y_coord_in_our_system, x_coord_in_our_system] = value
        # print(self.matrix[-y_coord_in_our_system, x_coord_in_our_system])

    def put_point_from_our_coord_in_matrix(
        self, x_coord_in_our_system: float, y_coord_in_our_system: float, value: int
    ) -> None:
        """Вносим наши координаты точки и пополяем нашу матрицу переданным значением"""
        # print(self.matrix[0, 0])
        # print(y_coord_in_our_system, x_coord_in_our_system)
        # print(-y_coord_in_our_system, x_coord_in_our_system)
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
                # print(x_center, x_point_in_our_system)
                # print((
                #         100
                #         / (
                #             (x_center - x_px_point_in_our_systemoint) ** 2
                #             + (y_center - y_point_in_our_system) ** 2
                #         )
                #     ) * coef)
                if (
                    # (x_center != x_point_in_our_system)
                    # and (y_center != y_point_in_our_system)
                    (x_center != 0)
                    and (x_point_in_our_system != 0)
                    and (y_center != 0)
                    and (y_point_in_our_system != 0)
                ):

                    return (
                        100
                        / (
                            (x_center - x_px_point_in_our_systemoint) ** 2
                            + (y_center - y_point_in_our_system) ** 2
                        )
                    ) * coef
                else:
                    return coef * 4
            except Exception as e:
                print("ERROR")
                return coef * 4

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
            z=z_uav, cone_apex_triangle_angle=20
        )

        # подсчитываем какие точки попадают под наш конус
        point_list = self.calculate_included_spray_points(
            x_center=x_center,
            y_center=y_center,
            x_point_in_our_system=x_coord_in_our_system,
            y_point_in_our_system=y_coord_in_our_system,
            spray_cone_size=spray_cone_size,
        )

        # наносим значения распыления на нашу матрицу для этих точек
        self.spray_on_neigh_cells(point_list=point_list)

        # print(self.matrix.min())
        # print(np.count_nonzero(self.matrix == 0 ))

    @staticmethod
    def get_width_and_length(pix_meter: int, x_list: list, y_list: list) -> tuple:
        """
        Находим высоту и ширину для картинки в метрах
        """
        h_matrix = max(y_list) - min(y_list)
        w_matrix = max(x_list) - min(x_list)

        return pix_meter * h_matrix, pix_meter * w_matrix


class Poliv:
    def __init__(self, matrix_handler: OpencvMatrix):
        self.matrix_handler = matrix_handler

    def get_pose_drone_coord():
        cmd = "gz topic -e --json-output -t /world/sitl/pose/info -n 1"  # вот отсюда тягаем координаты
        with Popen(cmd, stdout=PIPE, stderr=None, shell=True) as process:
            output = process.communicate()[0].decode("utf-8")
            json_object = json.loads(output)
            # print(json_object.get('pose')[1]) #.get('position'))
            return json_object.get("pose")[1]

test_obj = OpencvMatrix(3, x_list=[1156, 1226, 1050, 980], y_list=[811, 880, 1058, 988])
test_obj.make_one_full_iteration(1000, 811, 10)


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
