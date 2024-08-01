from OpenGL.GLU import *
from OpenGL.GL import *
from OpenGL.GLUT import *
import math
from Raycasting import Raycasting

from Utils import drawSquare, interpolate_color, read_texture

class Camera:
    """A object to store a camera"""
    def __init__(self, position, renderWidth=600, renderHeight=600, fov=60):
      self.position = position
      self.rotation = 0.0
      self.fov = fov # Field of view (!! in degrees NOT in radians)
      self.renderDistance = math.sqrt(renderWidth**2 + renderHeight**2) # max render distance = diagonale de la map
      self.renderWidth = renderWidth
      self.renderHeight = renderHeight

    def getRotation(self):
       return self.rotation
    
    def setRotation(self, angle=0.5):
       self.rotation = angle

    def setPosition(self, pos=(150,150)): # in range renderWidth / renderHeight
       self.position = pos

    def getPosition(self):
       return self.position
    
    def getRenderHeight(self):
       return self.renderHeight
    
    def getRenderWidth(self):
      return self.renderWidth
    
    def getFov(self):
       return self.fov
    
    def getRenderDistance(self):
       return self.renderDistance
    
    def calculateTranslatePos(self, distance):
       (x,y) = self.getPosition()
       angle = self.getRotation()
       return (x + math.cos(angle) * distance, y + math.sin(angle) * distance)
    
    def forward(self, distance=5):
       (x,y) = self.calculateTranslatePos(distance)
       self.setPosition((x, y))

    def backward(self, distance):
       (x,y) = self.calculateTranslatePos(-distance)
       self.setPosition((x, y))

    def draw(self, minimap):
        """Draw camera view"""
        # How many horizontal segments to draw roof / floor ?
        n = 15
        h = int(self.renderHeight/2/ n)

        # Draw roof
        for i in range(0, int(self.renderHeight/2), h):
           k = i / self.renderHeight / 2
           drawSquare(0,i,self.renderWidth,i+h,interpolate_color((1,0,1), (0,0,0.1), 1-k))

        # Draw floor
        # (x1,y1,x2,y2) = (0,self.renderHeight/2,self.renderWidth,self.renderHeight)
        # drawSquare(x1,y1,x2,y2,(0,2.4,0.1))
        for i in range(int(self.renderHeight/2), self.renderHeight, h):
           k = i / self.renderHeight / 2
           drawSquare(0,i,self.renderWidth,i+h,interpolate_color((0.5,0.4,0.4), (1,0,0.1), 1-k))

        # Draw walls (raycast)
        raycast = Raycasting(self, minimap)


