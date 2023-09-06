from matrix_handler import OpencvMatrix
from subprocess import PIPE, Popen
import json
import math

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