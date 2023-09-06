from matrix_handler import OpencvMatrix
from subprocess import PIPE, Popen
import json
import math
from PIL import Image
import pandas as pd
import numpy as np
import sys
import cv2


class Poliv:
    def __init__(self, matrix_handler: OpencvMatrix):
        self.matrix_handler = matrix_handler

    def get_pose_drone_coord(self):
        """
        Возвращает полнео положенеи дрона
        """
        cmd = "gz topic -e --json-output -t /world/sitl/pose/info -n 1"  # вот отсюда тягаем координаты
        with Popen(cmd, stdout=PIPE, stderr=None, shell=True) as process:
            output = process.communicate()[0].decode("utf-8")
            json_object = json.loads(output)
            # print(json_object.get('pose')[1]) #.get('position'))
            return json_object.get("pose")[1]

    def get_pose_drone_coord_xyz(self):
        """
        Возвращает xyz положение дрона
        """
        cmd = "gz topic -e --json-output -t /world/sitl/pose/info -n 1"  # вот отсюда тягаем координаты
        with Popen(cmd, stdout=PIPE, stderr=None, shell=True) as process:
            output = process.communicate()[0].decode("utf-8")
            json_object = json.loads(output)
            return json_object.get("pose")[1].get("position")

    def catch_point_and_place_on_matrix(self):
        xyz_dict = self.get_pose_drone_coord_xyz()
        self.matrix_handler.make_one_full_iteration(
            x_uav=xyz_dict.get("x"), y_uav=xyz_dict.get("y"), z_uav=xyz_dict.get("z")
        )

    def save_matrix_to_jpeg(self):
        # img = Image.fromarray(self.matrix_handler.matrix)
        # image_filename = "our_territory.jpeg"
        # img.save(image_filename)
        cv2.imwrite('output.png', self.matrix_handler.matrix)

    def save_matrix_to_csv(self):
        # np.set_printoptions(threshold=sys.maxsize)
        # print(self.matrix_handler.matrix)
        df = pd.DataFrame(self.matrix_handler.matrix)
        df.to_csv('data.csv', index=True)
