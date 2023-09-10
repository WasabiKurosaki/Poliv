from subprocess import PIPE, Popen
import json
import math


def get_pose_drone_coord():
    cmd = "gz topic -e --json-output -t /world/sitl/pose/info -n 1"  # вот отсюда тягаем координаты
    with Popen(cmd, stdout=PIPE, stderr=None, shell=True) as process:
        output = process.communicate()[0].decode("utf-8")
        json_object = json.loads(output)
        # print(json_object.get('pose')[1]) #.get('position'))
        return json_object.get("pose")[1]


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


# print(get_pose_drone_coord().get('orientation')['x'])
test_rot = get_pose_drone_coord().get("orientation")
x = test_rot["x"]
y = test_rot["y"]
z = test_rot["z"]
w = test_rot["w"]

print(get_pose_drone_coord())
# print(euler_from_quaternion(x, y, z, w))  # реально печатает ориентацию дрона в радианах
