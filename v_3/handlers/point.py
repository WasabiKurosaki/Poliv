from settings import pixel_meter, x_list, y_list, recommended_fertz_for_pixel
import itertools
import numpy as np


class Point:

    """
    Класс для работы с двумерными точками.
    Является вспомогательным.
    """

    @staticmethod
    def translate_into_our_coordinate_system(
        zero_point_of_our_coordinate_system: list, x_uav: float, y_uav: float
    ) -> tuple:
        x_coord_in_our_system = int(
            (x_uav - zero_point_of_our_coordinate_system[0]) * pixel_meter
        )
        y_coord_in_our_system = int(
            (y_uav - zero_point_of_our_coordinate_system[1]) * pixel_meter
        )
        return x_coord_in_our_system, y_coord_in_our_system

    @staticmethod
    def in_work_zone(x: float, y: float) -> bool:
        """Функция, проверяющая вхождение точки в рабочую зону миссии."""
        xp = x_list
        yp = y_list
        c = 0
        for i in range(len(xp)):
            if ((yp[i] <= y and y < yp[i - 1]) or (yp[i - 1] <= y and y < yp[i])) and (
                x > (xp[i - 1] - xp[i]) * (y - yp[i]) / (yp[i - 1] - yp[i]) + xp[i]
            ):
                c = 1 - c
        return c == 1

    @staticmethod
    def add_pollinating_liquid_values(
        x_center: float,
        y_center: float,
        x_point_in_our_system: float,
        y_point_in_our_system: float,
        coef=400,  # вот этот коэффициент желательно подогнать
    ):
        try:
            if (
                abs(x_center - x_point_in_our_system)
                + abs(y_center - y_point_in_our_system)
                != 0
            ):
                return 0.2 * (
                    100
                    - (
                        abs(x_center - x_point_in_our_system)
                        + abs(y_center - y_point_in_our_system)
                    )
                )
            else:
                # значит мы зашли в центр окружности
                return 0
        except Exception as e:
            print(e)
            print("ERROR:", x_center, x_point_in_our_system)
            return coef * 3

    def calculate_included_spray_points(
        self,
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
        # TODO оптимизировать создание этих списков, много лишних вычислений

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
        ans_array = np.zeros([len(all_points_included_in_our_con), 3])
        for i in range(len(all_points_included_in_our_con)):
            ans_array[i] = (
                all_points_included_in_our_con[i][0],
                all_points_included_in_our_con[i][1],
                self.add_pollinating_liquid_values(
                    all_points_included_in_our_con[i][0],
                    all_points_included_in_our_con[i][1],
                    x_center,
                    y_center,
                ),
            )

        # отсеим наши точки по принципу удаленности от центра:
        def check_if_close(x1, x2, y1, y2, spray_cone_size):
            distance = ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5
            # print(distance, spray_cone_size)

            if distance <= spray_cone_size / 2:
                return True
            else:
                return False

        ans_list = []
        for i in range(len(ans_array)):
            if check_if_close(
                x1=ans_array[i][0],
                y1=ans_array[i][1],
                x2=x_center,
                y2=y_center,
                spray_cone_size=spray_cone_size,
            ):
                ans_list.append(ans_array[i])
            else:
                pass
        ans_list = self.control_fertilize(ans_list)
        return ans_list

    def control_fertilize(self, ans_list: list[np.array]):
        # в милилитрах нормируем массив
        pixels_to_norm = len(ans_list)
        max_val = max(ans_list[:][2])

        # summator = 0
        # for i in range(pixels_to_norm):
        #     summator+=ans_list[i][2]

        # сделаем тупой ход и примем на целую меру от пиксела - центр пикселя под дроном и понадеемся,
        # что это серединный элемент нашего списка (пока не знаю как оптимально выбрать это без нагромаждений)
        # ans_list[pixels_to_norm//2][2] - будем пока что считать именно этим значением эталон - 80% опыления

        self.norm_coeff_80 = recommended_fertz_for_pixel / max_val * 0.8
        for i in range(pixels_to_norm):
            ans_list[i][2] = (
                self.norm_coeff_80 * ans_list[i][2] * 10
            )  # * 10000 возможно стоит добавить, так как коэффициент совсем маленький получается
        return ans_list
