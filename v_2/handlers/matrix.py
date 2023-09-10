import numpy as np
from settings import pixel_meter

class Matrix:

    """
    Класс, который должен хранить в себе матрицу, с которой мы работаем.
    По ходу выполнения миссии, будет обновляться внутри себя."""

    def __init__(self, point_manager, x_list: list, y_list: list) -> None:
        self.create_cv_matrix()
        self.point_manager = point_manager

    def create_cv_matrix(self, x_list: list, y_list: list) -> None:
        matrix_rows, matrix_columns = self.get_width_and_length(
            x_list, y_list
        )
        # self.pixel_meter = pixel_meter
        self.origin_point_of_our_coordinate_system = min(x_list), min(y_list)
        self.matrix_rows = matrix_rows
        self.matrix_columns = matrix_columns
        self.matrix = np.zeros((matrix_rows, matrix_columns))

    def translate_into_our_coordinate_system(self, x_uav: float, y_uav: float) -> tuple:
        """
        Перемещаем саму СК в левый нижний угол нашей матрицы + домножаем на pixel_meter.
        Возвращаем координаты в нашей ск в виде tuple(int, int).
        После следует перевести в виде индексов в матрицу numpy, не забыть!
        """
        x_coord_in_our_system = int(
            (x_uav - self.zero_point_of_our_coordinate_system[0]) * pixel_meter
        )
        y_coord_in_our_system = int(
            (y_uav - self.zero_point_of_our_coordinate_system[1]) * pixel_meter
        )
        return x_coord_in_our_system, y_coord_in_our_system
    
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
    
    @staticmethod
    def get_width_and_length(x_list: list, y_list: list) -> tuple:
        """
        Находим высоту и ширину для картинки в метрах
        """
        h_matrix = max(y_list) - min(y_list)
        w_matrix = max(x_list) - min(x_list)

        return pixel_meter * h_matrix, pixel_meter * w_matrix