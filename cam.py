import matplotlib.pyplot as plt
import numpy as np
from math import pi,cos,sin 
from Config import *
from math import radians

class Camera:
    def __init__(self):
        self.M = BASE 
        self.px_base = 1280
        self.px_altura = 720
        self.ccdx = 4
        self.ccdy = 3
        self.dist_focal = 1
        self.fstheta = 0
        self.rotation_matrix = np.eye(4)
        self.T = np.eye(4)

    def generate_intrinsix_matrix(self):
        self.ox = self.px_base / 2 
        self.oy = self.px_altura / 2

        self.fsx = self.dist_focal * (self.px_base / self.ccdx)
        self.fsy = self.dist_focal * (self.px_altura / self.ccdy)
        self.fstheta = self.fstheta * self.dist_focal

        self.K = np.array([[self.fsx , self.fstheta , self.ox],
                           [   0     ,   self.fsy   , self.oy],
                           [   0     ,    0         ,    1   ]])
    
        return self.K
    
    def update_intrinsix_matrix(self, update):
        params_list = [self.px_base,self.px_altura,self.ccdx,self.ccdy,self.dist_focal,self.fstheta]
        
        for param in range(len(update)):
            if update[param] != 0:
                params_list[param] = update[param]

        self.px_base = params_list[0]
        self.px_altura = params_list[1]
        self.ccdx = params_list[2]
        self.ccdy = params_list[3]
        self.dist_focal = params_list[4]
        self.fstheta = params_list[5]
    
    def generate_move_world(self,dx,dy,dz):
        self.T = np.eye(4)
        self.T[0,-1] = dx
        self.T[1,-1] = dy
        self.T[2,-1] = dz
        
        return self.T
    
    def move_world(self):
        self.M = self.T@self.M
        return self.M

    def move_cam(self,dx,dy,dz):
        self.new_cam = self.M
        self.M_inv = np.linalg.inv(self.new_cam)
        self.cam_orig = self.M_inv@self.new_cam
        self.move = self.generate_move_world(dx,dy,dz)
        self.new_cam = self.move@self.cam_orig
        self.M = self.M@self.new_cam
        return self.M
    
    def generate_rotation_world(self, ax, ay, az):
        ax = radians(ax)
        ay = radians(ay)
        az = radians(az)

        self.rotation_matrix_x = np.array([[1,0,0,0],[0, cos(ax),-sin(ax),0],[0, sin(ax), cos(ax),0],[0,0,0,1]])
        self.rotation_matrix_y = np.array([[cos(ay),0, sin(ay),0],[0,1,0,0],[-sin(ay), 0, cos(ay),0],[0,0,0,1]])
        self.rotation_matrix_z = np.array([[cos(az),-sin(az),0,0],[sin(az),cos(az),0,0],[0,0,1,0],[0,0,0,1]])

        self.rotation_matrix = self.rotation_matrix_x@self.rotation_matrix_y@self.rotation_matrix_z
       
        return self.rotation_matrix

    def rotation_world(self):
        self.M = self.rotation_matrix@self.M
        return self.M
    
    def rotation_cam(self, ax, ay, az):
        self.new_cam = self.M
        self.M_inv = np.linalg.inv(self.new_cam)
        self.cam_orig = self.M_inv@self.new_cam
        self.rotation = self.generate_rotation_world(ax,ay,az)
        self.new_cam = self.rotation@self.cam_orig
        self.M = self.M@self.new_cam
        return self.M
    
    def generate_extrinsix_matrix(self):
        #self.g = self.rotation_matrix@self.T  #tava antes
        self.g = np.linalg.inv(self.M) #raquel
        return self.g

    def camera_matrix(self):
        self.M = self.g@self.M
        return self.M

        
         