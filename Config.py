import numpy as np
from math import pi


e1 = np.array([[1],[0],[0],[0]]) # X
e2 = np.array([[0],[1],[0],[0]]) # Y
e3 = np.array([[0],[0],[1],[0]]) # Z
POINT =np.array([[0],[0],[0],[1]])

BASE_CANON = np.hstack((e1,e2,e3))

BASE = np.hstack((e1,e2,e3,POINT))
