from settings import pixel_meter

class Point:

    """Класс для работы с двумерными точками"""

    def __init__(self, x_origin, y_origin) -> None:
        # self.x_origin = x_origin
        # self.y_origin = y_origin
        pass

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
    