from OpenGL.GLU import *
from OpenGL.GL import *
from OpenGL.GLUT import *
import math

class Scene:

    def __init__(self, width, height, backgroundColor=(0,0,0)):
      self.width = width
      self.height = height
      self.backgroundColor = backgroundColor

    def init(self):
        glClearColor(*self.backgroundColor,0)
        gluOrtho2D(0,self.width,self.height,0)

 
