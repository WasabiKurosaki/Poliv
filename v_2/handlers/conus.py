import math


class Conus:
    """
    Класс, который производит все необходимые вычисления для конуса опления.
    """

    @staticmethod
    def calculate_spray_cone_size(
        z: float, cone_apex_triangle_angle: float = 20
    ) -> float:
        """
        Высчитываем размеры конуса распыления в метрах, передаем высоту и 2д угол конуса.
        """
        return abs(math.tan(cone_apex_triangle_angle) * z * 2)

    @staticmethod
    def calculate_spray_cone_center(
        x_poix_point_in_our_system: float,
        y_point_in_our_system: float,
        n_bias_meter: int = 1,
        x_rad_angle: float = 1,
        y_rad_angle: float = 1,
    ) -> tuple:
        """
        Вычисляем центр конуса в наших координатах (со смещение на n_bias_meter метров).
        Пока оставим нетронутым, для MVP.
        """
        # пускай сейчас он просто под собой рисует конус
        return x_poix_point_in_our_system, y_point_in_our_system

    def conus_calculate(
        self,
        z: float,
        cone_apex_triangle_angle: float,
        x_coord_in_our_system: float,
        y_coord_in_our_system: float,
    ) -> (float, tuple):
        return self.calculate_spray_cone_size(
            z, cone_apex_triangle_angle
        ), self.calculate_spray_cone_center(
            x_coord_in_our_system, y_coord_in_our_system
        )
