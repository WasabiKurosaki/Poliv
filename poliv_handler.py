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
        x_arr = np.array(self.matrix_handler.x_point_of_searching_sqr).reshape(4, 1)
        y_arr = np.array(self.matrix_handler.y_point_of_searching_sqr).reshape(4, 1)
        # self.matrix_handler.matrix_columns
        # print(x_arr.reshape(4, 1))
        # print(np.concatenate((x_arr, y_arr), axis=1)) self.matrix_handler.matrix_columns - 
        our_rect_massive = np.concatenate((x_arr, y_arr), axis=1)
        for i in range(len(our_rect_massive)):
            print(our_rect_massive[i], self.matrix_handler.matrix_rows)
            print(abs(int((our_rect_massive[i][0] - self.matrix_handler.matrix_rows/2))))
            our_rect_massive[i] = self.matrix_handler.translate_into_our_coordinate_system((our_rect_massive[i][0]),
                                                                                           our_rect_massive[i][1])
            
        # our_rect_massive = our_rect_massive.T
        print(our_rect_massive)
        
        matrix_to_png = np.rot90(self.matrix_handler.matrix)
        img_mod = cv2.polylines(
            self.matrix_handler.matrix,
            [our_rect_massive],
            True,
            (255, 255, 255),
            thickness=1,
        )
        cv2.imwrite("output.png", img_mod)
        ...

    def save_matrix_to_csv(self):
        df = pd.DataFrame(self.matrix_handler.matrix)
        df.to_csv("data.csv", index=True)
