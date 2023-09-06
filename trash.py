# import numpy as np
# from scipy.spatial import ConvexHull
# from scipy.spatial.distance import cdist

# @staticmethod
# def get_width_and_length(np_array_of_points: np.ndarray):
#     # попытка найти оптимальнуе размеры матрицы для матрицы, функцию лучше оставить на потом
#     np_array_of_points = np.array([[1156, 811], [1226, 880], [1050, 1057], [980, 988]], np.int32) # временный хардкод
#     hull = ConvexHull(np_array_of_points)

#     # Extract the points forming the hull
#     hullpoints = np_array_of_points[hull.vertices,:]

#     # Naive way of finding the best pair in O(H^2) time if H is number of points on
#     # hull
#     hdist = cdist(hullpoints, hullpoints, metric='euclidean')
#     # Get the farthest apart points
#     bestpair = np.unravel_index(hdist.argmax(), hdist.shape)

#     #Print them
#     print([hullpoints[bestpair[0]],hullpoints[bestpair[1]]])
#     # return



# class GeometryHelper:
#     @staticmethod
#     def euler_from_quaternion(x, y, z, w):
#         """
#         Convert a quaternion into euler angles (roll, pitch, yaw)
#         roll is rotation around x in radians (counterclockwise)
#         pitch is rotation around y in radians (counterclockwise)
#         yaw is rotation around z in radians (counterclockwise)
#         """
#         t0 = +2.0 * (w * x + y * z)
#         t1 = +1.0 - 2.0 * (x * x + y * y)
#         roll_x = math.atan2(t0, t1)

#         t2 = +2.0 * (w * y - z * x)
#         t2 = +1.0 if t2 > +1.0 else t2
#         t2 = -1.0 if t2 < -1.0 else t2
#         pitch_y = math.asin(t2)

#         t3 = +2.0 * (w * z + x * y)
#         t4 = +1.0 - 2.0 * (y * y + z * z)
#         yaw_z = math.atan2(t3, t4)

#         return roll_x, pitch_y, yaw_z  # in radians

#     # @staticmethod
#     # def tg_from_angle(angle):
#     #     return math.tan(angle)
