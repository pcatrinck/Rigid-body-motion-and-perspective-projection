from Config import *
from cam import Camera
from stl import mesh

class Object():
    def __init__(self):
        self.cam = Camera()
        self.file = 'mario.stl'

    def STL(self):
        self.your_mesh = mesh.Mesh.from_file(self.file)
        self.x = self.your_mesh.x.flatten()
        self.y = self.your_mesh.y.flatten()
        self.z = self.your_mesh.z.flatten()

        self.vectors = self.your_mesh.vectors

        self.stl = np.array([self.x.T,self.y.T,self.z.T,np.ones(self.x.size)])
        return self.stl
    
    def STL_vetor(self):
        self.your_mesh = mesh.Mesh.from_file(self.file)

        self.vectors = self.your_mesh.vectors
        return self.vectors
