from handlers.point import Point
from handlers.conus import Conus


class SprayMission:
    def __init__(self, matrix_manager, point_manager, conus_manager, gazebo_listener, opencv_manager) -> None:
        self.matrix_manager = matrix_manager
        self.point_manager = point_manager
        self.conus_manager = conus_manager
        self.gazebo_listener = gazebo_listener
        self.opencv_manager = opencv_manager

    def make_one_full_iteration(self, x_uav: float, y_uav: float, z_uav: float):
        """
        Полная итерация для одной точки
        """
        # проверяем находит ли наша точка внутри нашей исследуемой площади
        if self.point_manager.in_work_zone(x_uav, y_uav):
            # нам приходит точка в координатах симулятор, мы ее переводим в наши координаты
            (
                x_coord_in_our_system,
                y_coord_in_our_system,
            ) = self.point_manager.translate_into_our_coordinate_system(
                zero_point_of_our_coordinate_system=self.matrix_manager.origin_point_of_our_coordinate_system,
                x_uav=x_uav,
                y_uav=y_uav,
            )

            # вычисляем необходимые данные о конусе: его ширину основания и координаты центра
            spray_cone_size, (
                x_conus_center,
                y_conus_center,
            ) = self.conus_manager.conus_calculate(
                z=z_uav,
                cone_apex_triangle_angle=40,
                x_coord_in_our_system=x_coord_in_our_system,
                y_coord_in_our_system=y_coord_in_our_system,
            )

            # подсчитываем какие точки попадают под наш конус
            point_list = self.point_manager.calculate_included_spray_points(
                x_center=x_conus_center,
                y_center=y_conus_center,
                x_point_in_our_system=x_coord_in_our_system,
                y_point_in_our_system=y_coord_in_our_system,
                spray_cone_size=spray_cone_size,
            )

            # наносим значения распыления на нашу матрицу для этих точек
            self.matrix_manager.spray_on_neigh_cells(point_list=point_list)

            print("\nSucsesfully added point on matrix")

            print(
                "Минимальное значение в нашей матрице:",
                self.matrix_manager.matrix.min(),
            )
            print(
                "Среднее значение в нашей матрице:", self.matrix_manager.matrix.mean()
            )
            print(
                "Максимальное значение в нашей матрице:",
                self.matrix_manager.matrix.max(),
            )
            print("Размер нашей матрицы:", self.matrix_manager.matrix.shape)
        else:
            print("\nNow our drone is out of range")


    def catch_point_and_place_on_matrix(self):
        xyz_dict = self.gazebo_listener.get_pose_drone_coord_xyz()
        self.make_one_full_iteration(
            x_uav=xyz_dict.get("x"), y_uav=xyz_dict.get("y"), z_uav=xyz_dict.get("z")
        )

    def save_to_png(self):
        self.opencv_manager.save_matrix_to_png(self.matrix_manager.matrix)

    def colour_image_matrix(self):
        self.opencv_manager.colour_image_matrix(self.matrix_manager.matrix)