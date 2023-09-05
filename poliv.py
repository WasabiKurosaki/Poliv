import numpy as np
from scipy.spatial import ConvexHull
from scipy.spatial.distance import cdist

class OpencvMatrix:

    def __init__(self):
        ...

    def create_cv_matrix(pix_metr, size_metre_x, size_metre_y):
        ...

    @staticmethod
    def get_width_and_length(np_array_of_points: np.ndarray):
        # попытка найти оптимальнуе размеры матрицы для 
        np_array_of_points = np.array([[1156, 811], [1226, 880], [1050, 1057], [980, 988]], np.int32) # временный хардкод
        hull = ConvexHull(np_array_of_points)

        # Extract the points forming the hull
        hullpoints = np_array_of_points[hull.vertices,:]

        # Naive way of finding the best pair in O(H^2) time if H is number of points on
        # hull
        hdist = cdist(hullpoints, hullpoints, metric='euclidean')
        # Get the farthest apart points
        bestpair = np.unravel_index(hdist.argmax(), hdist.shape)

        #Print them
        print([hullpoints[bestpair[0]],hullpoints[bestpair[1]]])
        # return 
    def put_put_in_matrix():
        ...

    def __spray_on_neigh_cells():
        ...


class Poliv:

    def __init__(self):
        ...

print(OpencvMatrix.get_width_and_length(1))
# A = np.matrix([[1, 0], [0, 1]])
# A_int = np.linalg.inv(A)
# print(A_int)
