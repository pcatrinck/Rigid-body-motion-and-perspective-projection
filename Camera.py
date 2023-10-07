import matplotlib.pyplot as plt
import numpy as np
from math import pi,cos,sin 
from Config import *


class Camera:
    def __init__(self):
        self.M = BASE 
        self.px_base = PX_BASE
        self.px_altura = PX_ALTURA
        self.ccd = CCD
        self.dist_focal = DIST_FOCAL
        self.ox = OX
        self.oy = OY
        self.fsx = self.dist_focal * (self.px_base / self.ccd[0])
        self.fsy = self.dist_focal * (self.px_altura / self.ccd[1])
        self.fstheta = THETA

    def generate_intrinsic_matrix(self):
        self.K = np.array([[self.fsx,self.fstheta,self.ox],[0,self.fsy,self.oy],[0,0,1]])
        self.M_canon = BASE_CANON

        X = self.K@self.M_canon
        return X
    
    def move(self,dx,dy,dz):
        T = np.eye(4)
        T[0,-1] = dx
        T[1,-1] = dy
        T[2,-1] = dz
        return T

    def x_rotation(angle):
        rotation_matrix=np.array([[1,0,0,0],[0, cos(angle),-sin(angle),0],[0, sin(angle), cos(angle),0],[0,0,0,1]])
        return rotation_matrix

    def y_rotation(angle):
        rotation_matrix=np.array([[cos(angle),0, sin(angle),0],[0,1,0,0],[-sin(angle), 0, cos(angle),0],[0,0,0,1]])
        return rotation_matrix

    def z_rotation(angle):
        rotation_matrix=np.array([[cos(angle),-sin(angle),0,0],[sin(angle),cos(angle),0,0],[0,0,1,0],[0,0,0,1]])
        return rotation_matrix
    
    def generate_extrinsic_matrix(self):
        g = self.x_rotation@self.y_rotation@self.z_rotation@self.move