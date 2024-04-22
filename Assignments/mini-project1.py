import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

width, height = 800, 600                                                    # width and height of the screen created

def drawAxes():                                                             # draw x-axis and y-axis
    glLineWidth(3.0)                                                        # specify line size (1.0 default)
    glBegin(GL_LINES)                                                       # replace GL_LINES with GL_LINE_STRIP or GL_LINE_LOOP
    glColor3f(1.0, 0.0, 0.0)                                                # x-axis: red
    glVertex3f(0.0, 0.0, 0.0)                                               # v0
    glVertex3f(100.0, 0.0, 0.0)                                             # v1
    glColor3f(0.0, 1.0, 0.0)                                                # y-axis: green
    glVertex3f(0.0, 0.0, 0.0)                                               # v0
    glVertex3f(0.0, 100.0, 0.0)                                             # v1
    glColor3f(0.0, 0.0, 1.0)                                                # z-axis: blue
    glVertex3f(0.0, 0.0, 0.0)                                               # v0
    glVertex3f(0.0, 0.0, 100.0)                                             # v1
    glEnd()

# For Mini-project 1:
# TODO: 1) Create a scarecrow as instructed and 2) Constantly rotate head and nose ONLY
rotation_angle = 0  # Global variable to store rotation angle

def draw_Scarecrow():
    global rotation_angle

    rotation_angle += 1

    glClearColor(0, 0, 0, 1)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    quadratic = gluNewQuadric()
    gluQuadricDrawStyle(quadratic, GLU_FILL)

    # Torso (cylinder: radius=2.5, length=10)
    glColor3f(1.0, 1.0, 0.0)
    glPushMatrix()
    glTranslatef(0, 10, 0)  # Move the torso to y=5
    glRotatef(90, 1, 0, 0)  # Rotate the torso to align along y-axis
    gluCylinder(quadratic, 2.5, 2.5, 10.0, 32, 32)
    glPopMatrix()

    # Left Leg (cylinders: radius=1.0, length=12)
    glColor3f(1.0, 0.0, 0.0)
    glPushMatrix()
    glTranslatef(-1.2, 0, 0)  # Move the left leg to x=-1.2
    glRotatef(90, 1, 0, 0)  # Rotate the left leg to point in -y direction
    gluCylinder(quadratic, 1.0, 1.0, 12.0, 32, 32)
    glPopMatrix()

    # Right Leg (cylinders: radius=1.0, length=12)
    glColor3f(1.0, 0.0, 0.0)
    glPushMatrix()
    glTranslatef(1.2, 0, 0)  # Move the right leg to x=1.2
    glRotatef(90, 1, 0, 0)  # Rotate the right leg to point in -y direction
    gluCylinder(quadratic, 1.0, 1.0, 12.0, 32, 32)
    glPopMatrix()

    # Left Arm (cylinders: radius=1.0, length=10)
    glColor3f(0.0, 0.0, 1.0)
    glPushMatrix()
    glTranslatef(-1.2, 9, 0)  # Move the left arm to x=-1.2, y=9
    glRotatef(90, 0, 1, 0)  # Rotate the left arm to point in -y direction
    gluCylinder(quadratic, 1.0, 1.0, 12.0, 32, 32)
    glPopMatrix()

    # Right Arm (cylinders: radius=1.0, length=10)
    glColor3f(0.0, 0.0, 1.0)
    glPushMatrix()
    glTranslatef(1.2, 9, 0)  # Move the right arm to x=1.2, y=9
    glRotatef(-90, 0, 1, 0)  # Rotate the right arm to point in -y direction
    gluCylinder(quadratic, 1.0, 1.0, 12.0, 32, 32)
    glPopMatrix()

    # Head (sphere: radius=2.5)
    glColor3f(0.0, 1.0, 0.0)
    glPushMatrix()
    glTranslatef(0, 12.5, 0)  # Move the head to y=12.5
    glRotatef(rotation_angle, 0, 1, 0)  # Rotate the head around y-axis
    gluSphere(quadratic, 2.5, 32, 32)
    glPopMatrix()

    # Nose (cylinder: base-radius=0.3, top-radius=0, length=1.8)
    glColor3f(1.0, 0.0, 0.0)
    glPushMatrix()
    glRotatef(rotation_angle, 0, 1, 0)  # Apply the same rotation as the head
    glTranslatef(0, 0, 2.5)  # Move the nose to a position 2.5 units in front of the head
    glTranslatef(0, 12.5, 0)  # Move the nose up to the head's position
    
    gluCylinder(quadratic, 0.3, 0.0, 1.8, 32, 32)
    glPopMatrix()
    
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

    while True:
        bResetModelMatrix = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.MOUSEMOTION:
                if pygame.mouse.get_pressed()[0]:
                    glRotatef(event.rel[1], 1, 0, 0)
                    glRotatef(event.rel[0], 0, 1, 0)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_0:
                    bResetModelMatrix = True
        
        # ONLY write your code inside the function below 
        #   You don't need to modify any other code in this file.
        draw_Scarecrow()

        # reset the current model-view back to the initial matrix
        if (bResetModelMatrix):
            glLoadMatrixf(initmodelMatrix)

        # draw x, y, z axes without involving any transformations
        glPushMatrix()
        glLoadMatrixf(initmodelMatrix)
        drawAxes()
        glPopMatrix()
        pygame.display.flip()
        pygame.time.wait(10)

main()