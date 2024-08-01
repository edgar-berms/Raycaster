from OpenGL.GLU import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from PIL import Image
import numpy

def interpolate_color(source=(1,0,0), target=(0,1,0), k=0.5):
    """Interpolate (lerp) between source and target RGB tuples with coefficient k."""
    k = max(0, min(1, k)) # k in range [0,1]
    r = source[0] + (target[0] - source[0]) * k
    g = source[1] + (target[1] - source[1]) * k
    b = source[2] + (target[2] - source[2]) * k
    return (r, g, b)


def segmentsIntersects(s0=[(0,0),(1,0)],s1=[(3,0),(4,0)]):
    """returns true if s0 and s1 intersects."""
    dx0 = s0[1][0]-s0[0][0]
    dx1 = s1[1][0]-s1[0][0]
    dy0 = s0[1][1]-s0[0][1]
    dy1 = s1[1][1]-s1[0][1]
    p0 = dy1*(s1[1][0]-s0[0][0]) - dx1*(s1[1][1]-s0[0][1])
    p1 = dy1*(s1[1][0]-s0[1][0]) - dx1*(s1[1][1]-s0[1][1])
    p2 = dy0*(s0[1][0]-s1[0][0]) - dx0*(s0[1][1]-s1[0][1])
    p3 = dy0*(s0[1][0]-s1[1][0]) - dx0*(s0[1][1]-s1[1][1])
    return (p0*p1<=0) & (p2*p3<=0)


def drawLine(x1, y1, x2, y2, color=(1,1,1), width=1):
    """draw a line between (x1,y1) and (x2,y2) points"""
    glLineWidth(width)
    glColor3f(*color)
    glBegin(GL_LINES)
    glVertex2f(x1, y1)
    glVertex2f(x2, y2)
    glEnd()

def drawSquare(x1, y1, x2, y2, color=(0,0.5,0.8), texture=False):
    drawPolygon(x1, y1, x2, y1, x2, y2, x1, y2, color, texture)

def drawPolygon(xa, ya, xb, yb, xc, yc, xd, yd, color=(0,0.5,0.8), texture=False):
    glEnable(GL_TEXTURE_2D)
    if(texture != False):
        glBindTexture(GL_TEXTURE_2D, texture)

    glColor3f(*color)
    glBegin(GL_POLYGON)
    glVertex2f(xa, ya)
    glVertex2f(xb, yb)
    glVertex2f(xc, yc)
    glVertex2f(xd, yd)
    glEnd()


def read_texture(filename="textures/floor.jpg"):
    img = Image.open(filename)
    # img = img.convert("RGB") # to remove alpha channel, if necessary with .PNG
    img_data = numpy.array(list(img.getdata()), numpy.int8)
    textID = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, textID)
    glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)
    format = GL_RGB if img.mode == "RGB" else GL_RGBA
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, img.size[0], img.size[1], 0,
                format, GL_UNSIGNED_BYTE, img_data)
    return textID

