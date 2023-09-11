from settings import pixel_meter
from handlers.mission_manager import SprayMission
from handlers.matrix_manager import Matrix
from handlers.point import Point
from handlers.conus import Conus
from handlers.gazebo_manager import GazeboListener
from handlers.opencv_manager import OpencvManager


matrix_manager = Matrix(
    x_mission_list_origin=[1156, 1226, 1050, 980],
    y_mission_list_origin=[811, 880, 1058, 988],
)

point_manager = Point()
conus_manager = Conus()
gazebo_listener = GazeboListener()
opencv_manager = OpencvManager()


mission_manager = SprayMission(
    matrix_manager=matrix_manager,
    point_manager=point_manager,
    conus_manager=conus_manager,
    gazebo_listener = gazebo_listener,
    opencv_manager=opencv_manager
)

# mission_manager.make_one_full_iteration(x_uav=1100, y_uav=900, z_uav=10)


# test_obj = OpencvMatrix(4, x_list=[1156, 1226, 1050, 980], y_list=[811, 880, 1058, 988])
# test_obj.make_one_full_iteration(1100, 900, 10)
