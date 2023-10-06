import numpy as np
from math import pi


e1 = np.array([[1],[0],[0],[0]]) # X
e2 = np.array([[0],[1],[0],[0]]) # Y
e3 = np.array([[0],[0],[1],[0]]) # Z
point =np.array([[0],[0],[0],[1]])

BASE_CANON = np.hstack((e1,e2,e3))

BASE = np.hstack((e1,e2,e3,point))

PX_BASE = 1280

PX_ALTURA = 720

DIST_FOCAL = 50 

CCD = [36,24]

OX = PX_BASE / 2 

OY = PX_ALTURA / 2

THETA = 0