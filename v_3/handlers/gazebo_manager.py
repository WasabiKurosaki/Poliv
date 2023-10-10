from subprocess import PIPE, Popen
import json
from settings import cmd


class GazeboListener:
    @staticmethod
    def get_pose_drone_coord():
        """
        Возвращает полнео положенеи дрона
        """
        with Popen(cmd, stdout=PIPE, stderr=None, shell=True) as process:
            output = process.communicate()[0].decode("utf-8")
            json_object = json.loads(output)
            # print(json_object.get('pose')[1]) #.get('position'))
            return json_object.get("pose")[1]

    @staticmethod
    def get_pose_drone_coord_xyz():
        """
        Возвращает xyz положение дрона
        """
        with Popen(cmd, stdout=PIPE, stderr=None, shell=True) as process:
            output = process.communicate()[0].decode("utf-8")
            json_object = json.loads(output)
            return json_object.get("pose")[1].get("position")
