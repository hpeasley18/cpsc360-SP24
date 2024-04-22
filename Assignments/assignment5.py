import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

width, height = 800, 600                                                    # width and height of the screen created

########################################### DO NOT MODIFY CODE BELOW ####################################################

vertices = (
    (1, -1, -1),
    (1, 1, -1),
    (-1, 1, -1),
    (-1, -1, -1),
    (1, -1, 1),
    (1, 1, 1),
    (-1, -1, 1),
    (-1, 1, 1)
)

edges = (
    (0, 1),
    (0, 3),
    (0, 4),
    (2, 1),
    (2, 3),
    (2, 7),
    (6, 3),
    (6, 4),
    (6, 7),
    (5, 1),
    (5, 4),
    (5, 7)
)

faces = (
    (0, 1, 2, 3),
    (3, 2, 7, 6),
    (6, 7, 5, 4),
    (4, 5, 1, 0),
    (1, 5, 7, 2),
    (4, 0, 3, 6)
)

def cube():
    glColor3f(0.2, 0.5, 0.4)
    glBegin(GL_QUADS)
    for face in faces:
        x = 0
        for vertex in face:
            x += 1
            vertexPos = vertices[vertex]
            vertexPos = tuple(5*v+7 for v in vertexPos)
            glVertex3fv(vertexPos)
    glEnd()

    glColor3f(1.0, 1.0, 1.0)
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            vertexPos = vertices[vertex]
            vertexPos = tuple(5*v+7 for v in vertexPos)
            glVertex3fv(vertexPos)
    glEnd()

def draw():                                                                 # This is the drawing function drawing all graphics (defined by you)
    glClearColor(0, 0, 0, 1)                                                # set background RGBA color 
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)                        # clear the buffers initialized in the display mode
    cube()

def drawAxes():                                                             # draw x-axis and y-axis
    glLineWidth(3.0)                                                        # specify line size (1.0 default)
    glBegin(GL_LINES)                                                       # replace GL_LINES with GL_LINE_STRIP or GL_LINE_LOOP
    glColor3f(1.0, 0.0, 0.0)                                                # x-axis: red
    glVertex3f(0.0, 0.0, 0.0)                                               # v0
    glVertex3f(100.0, 0.0, 0.0)                                             # v1
    glColor3f(0.0, 1.0, 0.0)                                                # y-axis: green
    glVertex3f(0.0, 0.0, 0.0)                                               # v0
    glVertex3f(0.0, 100.0, 0.0)                                             # v1
    glColor3f(0.0, 0.0, 1.0)                                                # z-axis: green
    glVertex3f(0.0, 0.0, 0.0)                                               # v0
    glVertex3f(0.0, 0.0, 100.0)                                             # v1
    glEnd()
########################################### ASSIGNMENT CODE ####################################################
def drawRotationAxis():
    glLineWidth(5.0)
    glColor3f(1.0, 1.0, 0.0)
    glBegin(GL_LINES)
    glVertex3f(7.0, 20.0, 7.0)
    glVertex3f(7.0, 0.0, 7.0)
    glEnd()

# For Assignment 5: Complete the two functions below
# Q1:
def spinningTransform():
    
    # Define the rotation angle
    angle = 1.0

    # Apply rotation around the y-axis passing through the cube's center
    glTranslatef(14.0, 0.0, 14.0)  # Translate to the center of the cube
    glRotatef(angle, 0.0, 1.0, 0.0)  # Rotate around the y-axis
    glTranslatef(-14.0, 0.0, -14.0)  # Translate back to original position

# Q2:
def scaleByHalf():

    # Apply scaling transformation to scale the cube uniformly by half
    glScalef(0.5, 0.5, 0.5)
    

def main():
    pygame.init()                                                           # initialize a pygame program
    glutInit()                                                              # initialize glut library 

    screen = (width, height)                                                # specify the screen size of the new program window
    display_surface = pygame.display.set_mode(screen, DOUBLEBUF | OPENGL)   # create a display of size 'screen', use double-buffers and OpenGL
    pygame.display.set_caption('CPSC 360 - Hunter Peasley')                      # set title of the program window

    glEnable(GL_DEPTH_TEST)
    glMatrixMode(GL_PROJECTION)                                             # set mode to projection transformation
    glLoadIdentity()                                                        # reset transf matrix to an identity
    gluPerspective(45, (width / height), 0.1, 100.0)                        # specify perspective projection view volume

    glMatrixMode(GL_MODELVIEW)                                              # set mode to modelview (geometric + view transf)
    gluLookAt(0, 0, 50, 0, 0, -1, 0, 1, 0)
    initmodelMatrix = glGetFloat(GL_MODELVIEW_MATRIX)
    scaleByHalf()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        
        
        draw() # function to draw the object
        spinningTransform()

        # below are the code irrelevant to the assignment
        glPushMatrix()
        glLoadMatrixf(initmodelMatrix)
        drawAxes()
        drawRotationAxis()
        glPopMatrix()
        pygame.display.flip()
        pygame.time.wait(10)
        
        
    
main()
