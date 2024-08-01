from OpenGL.GLU import *
from OpenGL.GL import *
from OpenGL.GLUT import *
import math

from Utils import drawLine, drawPolygon, interpolate_color

class Raycasting:
    """A new raycasting"""
    def __init__(self, camera, minimap):
      self.camera = camera
      self.minimap = minimap
      self.run()

    def run(self):
        fov = self.camera.getFov()
        rotation = self.camera.getRotation()
        (px, py) = self.camera.getPosition()
        maxWallHeight = self.minimap.getWallHeight()
        maxRenderDistance = self.camera.getRenderDistance()
        cameraWidth = self.camera.getRenderWidth()
        rayWidth = cameraWidth / fov
        
        polygons = []

        for i in range(fov+1):
            angle = fov * math.pi / 180
            
            # Calculate ray angle
            (tX, tY) = (math.cos(i/fov+rotation-angle/2), math.sin(i/fov+rotation-angle/2))
            
            # Calculate target ray length (radius)
            distance = 0
            step = 2
            intersectedTile = False
            while(True):
                intersectedTile = self.minimap.isInWall(px+tX*distance, py+tY*distance)
                if(intersectedTile != False or distance > maxRenderDistance):
                    break
                else:
                    distance += step
            

            color = interpolate_color((1,0,0), (1,1,1), distance / cameraWidth)
            
            # Apply length
            tX = tX*distance
            tY = tY*distance

            # Trace ray (minimap)
            (minimapX, minimapY) = self.minimap.getPosition()
            (rx1, ry1) = (minimapX+px,minimapY+py)
            (rx2, ry2) = (minimapX+px + tX, minimapY+py + tY)
            drawLine(rx1, ry1, rx2, ry2, color, 1)

            # Trace ray (3d camera)
            wallAngle = (rotation - ((rotation + 30) % 360)) % 360
            h = distance * math.cos(math.radians(wallAngle))
            if(h<1): # In wall? (if collision disabled)
                h = 1
            lineH = (self.minimap.getMatrixSize()**2*maxWallHeight)/(h)
            #lineH = min(maxWallHeight, lineH)
            lineOff = self.camera.getRenderHeight()/2 - (int(lineH) >> 1); 
            (lineX1, lineY1, lineX2, lineY2) = (i*rayWidth, lineOff, i*rayWidth,lineOff+lineH)
            drawLine(lineX1, lineY1, lineX2, lineY2, color, rayWidth)

            intersectedFace = self.minimap.getIntersectedFace([(rx1, ry1), (rx2, ry2)], intersectedTile)
            polygons.append((intersectedTile, intersectedFace, (lineX1, lineY1, lineX2, lineY2), color))
            

        #start = (0,0)
        #lastTile = polygons[0][0]
        #lastFace = polygons[0][1]
        #for i, r in enumerate(polygons[:]):
        #    (tile, face, (x1,y1,x2,y2), color) = r
        #    if i==0:
        #        start = (x1,y1,x2,y2)
        #    else:
        #        previousRay = polygons[i-1]
        #        (ptile, pface, (px1,py1,px2,py2), color) = previousRay
        #        if lastTile != tile or lastFace != face:
        #            drawPolygon(*start, px2+rayWidth,py2, px1+rayWidth,py1, color)
        #            start = (x1,y1,x2,y2)
        #    lastFace = face
        #    lastTile = tile

        # Optional Draw vertices
        start = (0,0)
        lastTile = polygons[0][0]
        lastFace = polygons[0][1]
        for i, r in enumerate(polygons[:]):
            (tile, face, (x1,y1,x2,y2), color) = r
            if i==0:
                start = (x1,y1,x2,y2)
            else:
                previousRay = polygons[i-1]
                (ptile, pface, (px1,py1,px2,py2), color) = previousRay
                if lastTile != tile or lastFace != face or i==len(polygons)-1:
                    drawLine(start[0]-rayWidth/2,start[1], px1+rayWidth/2, py1,(1,1,1),4) # TOP
                    #drawLine(start[0]-rayWidth/2,start[1], start[2]+rayWidth/2, start[3],(1,1,1),3) # LEFT
                    drawLine(start[0]-rayWidth/2,start[3], px1+rayWidth/2, py2,(1,1,1),4) # BOTTOM
                    start = (x1,y1,x2,y2)
            lastFace = face
            lastTile = tile  

                



            
