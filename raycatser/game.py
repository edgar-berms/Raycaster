from OpenGL.GLU import *
from OpenGL.GL import *
from OpenGL.GLUT import *
import math
import time
from Camera import Camera
from Minimap import Minimap
from Scene import Scene

# PARAMETERS
WINDOW_SIZE = (1200, 600)
WALL_COLOR = (1,0.5,0.2)
BG_COLOR = (0,0,0) 
map = [  [1,1,1,1,1,1,1,1,1,1,1,1],
         [1,0,0,0,0,0,0,0,0,0,0,1],
         [1,0,0,0,0,0,0,0,0,0,0,1],
         [1,0,1,0,0,1,1,0,0,0,0,1],
         [1,0,0,0,0,1,1,0,0,0,0,1],
         [1,0,0,0,0,0,0,0,0,0,0,1],
         [1,0,0,0,0,0,0,0,0,0,1,1],
         [1,1,0,0,0,0,0,0,0,0,0,1],
         [1,0,0,0,0,0,0,1,0,0,0,1],
         [1,0,0,0,0,0,0,0,0,0,0,1],
         [1,0,0,1,1,1,0,0,0,0,0,1],
         [1,1,1,1,1,1,1,1,1,1,1,1]  ] 

scene = Scene(*WINDOW_SIZE)

# FPS
start_time = time.time()
frame_count = 0
fps = 0.0

# Left screen : Camera
camera = Camera((460,100), WINDOW_SIZE[0]//2, WINDOW_SIZE[1])
camera.setRotation(1.8)

# Right screen : minimap
minimap = Minimap(map)
minimap.setSkyColor(BG_COLOR)
minimap.setWallsColor(WALL_COLOR)

    
def move(key,x,y):
    (translationIncrement, rotationIncrement) = (5, 0.25)
    if key == b'z':
        if minimap.isInWall(*camera.calculateTranslatePos(translationIncrement)) == False:
            camera.forward(translationIncrement)
    if key == b's':
        if minimap.isInWall(*camera.calculateTranslatePos(-translationIncrement)) == False:
            camera.backward(translationIncrement)
    if key == b'q':
        camera.setRotation((camera.getRotation() - rotationIncrement) % (2*math.pi))
    if key == b'd':
        camera.setRotation((camera.getRotation() + rotationIncrement) % (2*math.pi))
        
    glutPostRedisplay()     

# draw text on screen
def draw_text(x, y, text):
    glColor3f(1.0,1.0,1.0)
    glRasterPos2f(x, y)
    for char in text:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_12, ord(char))
        
# calculate fps
def draw_fps():
    global frame_count, start_time, fps
    frame_count += 1
    if time.time() - start_time >= 1.0:
        fps = frame_count // (time.time() - start_time)
        print("FPS :",fps)
        frame_count = 0
        start_time = time.time()

def update():
    """Clear screen & draw a new frame"""
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    
    # Lights settings (comment this part to have the true version)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
    glLightfv(GL_LIGHT0, GL_POSITION, [1.0, 1.0, 0.0, 0.0])
    glLightfv(GL_LIGHT0, GL_AMBIENT, [0.2, 0.2, 0.0, 1.0])
    glLightfv(GL_LIGHT0, GL_DIFFUSE, [1.0, 1.0, 0.0, 1.0])
    
    draw_fps()
    
    minimap.draw()
    camera.draw(minimap)
    minimap.drawPlayer(camera.getPosition(), camera.getRotation())
       
    draw_text(800,15,str(camera.getPosition()))
    draw_text(800,25,str(camera.getRotation()))
    draw_text(800,35,str(fps))   
    
    glutSwapBuffers()
    glutPostRedisplay()

def main():
    """Open window & handle user events"""
    global scene    
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(*WINDOW_SIZE)
    glutCreateWindow("Raycasting ({}x{} px)".format(WINDOW_SIZE[0], WINDOW_SIZE[1]))
    scene.init()
    glutDisplayFunc(update)
    glutKeyboardFunc(move)
    glutMainLoop()

if __name__ == "__main__":
    main()
    
    


