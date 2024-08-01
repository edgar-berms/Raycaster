from OpenGL.GLU import *
from OpenGL.GL import *
from OpenGL.GLUT import *
import math

from Utils import drawLine, segmentsIntersects

class Minimap:
   """A object to store a map based on a 2D array"""

   def __init__(self, map, position=(600,0), width=600, height=600):
      self.map = map
      self.skyColor = (0,0,0)
      self.wallsColor = (1,0,0)
      self.playerColor = (0,1,1)
      self.position = position
      self.width = width
      self.height = height

   def getIntersectedFace(self, ray, intersectedWall=(1,1)):
      self.faces = []
      (i,j) = intersectedWall
      TILE_SIZE = self.getTileSize()
      #    A +-----+ B    (A,B) / (D/C) are TOP / BOTTOM segments
      #      |     |      (B,C) / (A/D) are RIGHT / LEFT segments
      #    D +-----+ C    
      #            \
      #             + R  (ray source position, here intersects (DC) segment)
      (xA, yA) = (self.position[0]+i*TILE_SIZE, self.position[1]+j*TILE_SIZE)
      (xB, yB) = (xA + TILE_SIZE, yA)
      (xC, yC) = (xB, yB+TILE_SIZE)
      (xD, yD) = (xA, yA+TILE_SIZE)
      AB = [(xA,yA),(xB,yB)]
      BC = [(xB,yB),(xC,yC)]
      CD = [(xC,yC),(xD,yD)]
      AD = [(xA,yA),(xD,yD)]
      if(segmentsIntersects(ray, AB)):
         drawLine(xA, yA, xB, yB, color=(1,0,1), width=2)
         return "top"
      if(segmentsIntersects(ray, BC)): 
         drawLine(xB, yB, xC, yC, color=(1,0,1), width=2)
         return "right"
      if(segmentsIntersects(ray, CD)):
         drawLine(xC, yC, xD, yD, color=(1,0,1), width=2)
         return "bottom"
      if(segmentsIntersects(ray, AD)):
         drawLine(xA, yA, xD, yD, color=(1,0,1), width=2)
         return "left"


   def getPosition(self):
      return self.position

   def getWallHeight(self):
      return int(self.height)

   def getSkyColor(self):
      return self.skyColor

   def setSkyColor(self, color):
      self.skyColor = color
      return self

   def getWallsColor(self):
      return self.wallsColor

   def setWallsColor(self, color):
      self.wallsColor = color
      return self

   def draw(self):
      self.drawWalls()

   def drawWalls(self):
      """draw map walls"""
      (x0, y0) = self.position
      TILE_SIZE = self.getTileSize()
      # Draw walls
      for i in range(len(self.map)):               # for each line
         for j in range(len(self.map[i])):         # for each column
               if self.map[i][j] == 1:             # is wall tile ?
                  glColor3f(*self.getWallsColor())
                  glPointSize(TILE_SIZE)
                  glBegin(GL_POINTS)
                  glVertex2f(x0+i*TILE_SIZE + TILE_SIZE/2,y0+j*TILE_SIZE + TILE_SIZE/2)
                  glEnd()

      # Draw grid
      gridColor = (0.6,0.6,0.6)
      for i in range(len(self.map)):
         glLineWidth(1)
         glColor3f(*gridColor)
         glBegin(GL_LINES)
         glVertex2f(x0+i*TILE_SIZE, 0)
         glVertex2f(x0+i*TILE_SIZE, self.height)
         glEnd()

      for i in range(len(self.map)):
         glLineWidth(1)
         glColor3f(*gridColor)
         glBegin(GL_LINES)
         glVertex2f(x0, y0+i*TILE_SIZE)
         glVertex2f(x0+self.width, y0+i*TILE_SIZE)
         glEnd()





   def drawPlayer(self, pos=(150,150), angle=0.5):
      pos = (pos[0]+self.position[0], pos[1]+self.position[1])

      # Draw player
      glColor3f(*self.playerColor)
      glPointSize(8)
      glBegin(GL_POINTS)
      glVertex2f(pos[0], pos[1])
      glEnd()

      # Draw directional vector
      vLen = 30
      (tX, tY) = (math.cos(angle)*vLen, math.sin(angle)*vLen)
      glLineWidth(1)
      glColor3f(1,0,1)
      glBegin(GL_LINES)
      glVertex2f(pos[0], pos[1])
      glVertex2f(pos[0] + tX, pos[1] + tY)
      glEnd()

   def getMatrixSize(self):
      return len(self.map)

   def getTileSize(self):
      return self.width // len(self.map)
   
   def isInWall(self, x, y):
      (iX,iY) = self.getMatrixPosition(x,y)
      if(self.map[iX][iY] == 1):
         return (iX,iY)
      else:
         return False
   
   def getMatrixPosition(self, x,y):
      TILE_SIZE = self.getTileSize()
      iX = int(x // TILE_SIZE)
      iY = int(y // TILE_SIZE)
      # Get corresponding x/y indexes included in range [0, len(carte)-1]
      (minIdx,maxIdx) = (0, len(self.map)-1)
      iX = max(minIdx, iX)
      iY = max(minIdx, iY)
      iY = min(maxIdx, iY)
      iX = min(maxIdx, iX)
      return (iX,iY)