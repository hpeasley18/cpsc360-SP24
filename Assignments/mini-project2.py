import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

import math

width, height = 800, 600                                                    # width and height of the screen created
whichQuestion = 3                                                           # 1: run Q1; 2: run Q2; 3: run Bonus

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

def draw_Scarecrow():                                                  # This is the drawing function drawing all graphics (defined by you)
    glClearColor(0, 0, 0, 1)                                                # set background RGBA color 
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)                        # clear the buffers initialized in the display mode

    # configure quatratic drawing
    quadratic = gluNewQuadric()
    gluQuadricDrawStyle(quadratic, GLU_FILL)  

    # Head (sphere: radius=2.5) 
    glPushMatrix()
    glTranslatef(0.0, 12.5, 0.0)
    glColor3f(0.0, 1.0, 0.0)
    gluSphere(quadratic, 2.5, 32, 32)
    glPopMatrix()

    # Nose (cylinder: radius=0.2, length=2)
    glPushMatrix()
    glTranslatef(0.0, 12.5, 2.5)
    glColor3f(1.0, 0.0, 0.0)
    gluCylinder(quadratic, 0.3, 0.0, 1.8, 32, 32)
    glPopMatrix()    

    # Torso (cylinder: radius=2.5, length=10)
    glPushMatrix()
    glRotatef(-90.0, 1, 0, 0)
    glColor3f(1.0, 1.0, 0.0)
    gluCylinder(quadratic, 2.5, 2.5, 10.0, 32, 32)
    glPopMatrix()

    # Left Leg (cylinders: radius=1.0, length=12)
    glPushMatrix()
    glTranslatef(-1.2, 0.0, 0.0)
    glRotatef(90.0, 1, 0, 0)
    glColor3f(1.0, 0.0, 0.0)
    gluCylinder(quadratic, 1.0, 1.0, 12.0, 32, 32)
    glPopMatrix()

    # Right Leg (cylinders: radius=1.0, length=12)
    glPushMatrix()
    glTranslatef(1.2, 0.0, 0.0)
    glRotatef(90.0, 1, 0, 0)
    glColor3f(1.0, 0.0, 0.0)
    gluCylinder(quadratic, 1.0, 1.0, 12.0, 32, 32)
    glPopMatrix()

    # Left Arm (cylinders: radius=0.8, length=10)
    glPushMatrix()
    glTranslatef(-2.5, 9.0, 0.0)
    glRotatef(-90.0, 0, 1, 0)
    glColor3f(0.0, 0.0, 1.0)
    gluCylinder(quadratic, 1.0, 1.0, 12.0, 32, 32)
    glPopMatrix()

    # Right Arm (cylinders: radius=0.8, length=10)
    glPushMatrix()
    glTranslatef(2.5, 9.0, 0.0)
    glRotatef(90.0, 0, 1, 0)
    glColor3f(0.0, 0.0, 1.0)
    gluCylinder(quadratic, 1.0, 1.0, 12.0, 32, 32)
    glPopMatrix()

def main():
    pygame.init()                                                           # initialize a pygame program
    glutInit()                                                              # initialize glut library 

    screen = (width, height)                                                # specify the screen size of the new program window
    display_surface = pygame.display.set_mode(screen, DOUBLEBUF | OPENGL)   # create a display of size 'screen', use double-buffers and OpenGL
    pygame.display.set_caption('CPSC 360 - Hunter Peasley')                      # set title of the program window

    glEnable(GL_DEPTH_TEST)
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)                                             # set mode to projection transformation
    glLoadIdentity()

    # Q1, Q2 Setup:                                                         # reset transf matrix to an identity
    # glOrtho(-40, 40, -30, 30, 20, 80)
    
    # Bonus Setup: perspective projection
    gluPerspective(45, (width/height), 0.1, 100.0)
    # ----------------------------------------------------------------------------------------------
    glMatrixMode(GL_MODELVIEW)                                              # set mode to modelview (geometric + view transf)
    initmodelMatrix = glGetFloat(GL_MODELVIEW_MATRIX)

    # Bonus: Automatic camera rotation settings
    angle = 0
    rotation_speed = 1  # Initial rotation speed

    #Q1 Presets
    Q1_offset_x = 0
    Q1_offset_y = 0

    #Q2 Presets
    Q2_View_x = 0
    Q2_View_y = 0
    Q2_View_z = 50
    Q2_Rotation_x = 0
    Q2_Rotation_y = 0
    Q2_Rotation_z = 0
    Q2_Lookup_x = 0
    Q2_Lookup_y = 1
    Q2_Lookup_z = 0
    
    while True:
        bResetModelMatrix = False

        # user interface event handling
        for event in pygame.event.get():

            # quit the window
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            # mouse event
            if event.type == pygame.MOUSEMOTION:
                if pygame.mouse.get_pressed()[0]:
                    glRotatef(event.rel[1], 1, 0, 0)
                    glRotatef(event.rel[0], 0, 1, 0)

            # keyboard event
            # TODO: keyboard event - Add your keyboard events here
            # Q1 Keyboard inputs
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_0:
                    bResetModelMatrix = True
                elif event.key == pygame.K_RIGHT:
                    Q1_offset_x += 1
                elif event.key == pygame.K_LEFT:
                    Q1_offset_x -= 1
                elif event.key == pygame.K_UP:
                    Q1_offset_y += 1
                elif event.key == pygame.K_DOWN:
                    Q1_offset_y -= 1

            # Q2 Keyboard inputs
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_0:
                    bResetModelMatrix = True
                elif event.key == pygame.K_a:
                    Q2_View_x = -50
                    Q2_View_y = 0
                    Q2_View_z = 0
                    Q2_Rotation_x = 0
                    Q2_Rotation_y = 0
                    Q2_Rotation_z = 0
                    Q2_Lookup_x = 0
                    Q2_Lookup_y = 1
                    Q2_Lookup_z = 0
                elif event.key == pygame.K_d:
                    Q2_View_x = 50
                    Q2_View_y = 0
                    Q2_View_z = 0
                    Q2_Rotation_x = 0
                    Q2_Rotation_y = 0
                    Q2_Rotation_z = 0
                    Q2_Lookup_x = 0
                    Q2_Lookup_y = 1
                    Q2_Lookup_z = 0
                elif event.key == pygame.K_s:
                    Q2_View_x = 0
                    Q2_View_y = 0
                    Q2_View_z = 50
                    Q2_Rotation_x = 0
                    Q2_Rotation_y = 0
                    Q2_Rotation_z = 0
                    Q2_Lookup_x = 0
                    Q2_Lookup_y = 1
                    Q2_Lookup_z = 0
                elif event.key == pygame.K_w:
                    Q2_View_x = 0
                    Q2_View_y = 0
                    Q2_View_z = -50
                    Q2_Rotation_x = 0
                    Q2_Rotation_y = 0
                    Q2_Rotation_z = 0
                    Q2_Lookup_x = 0
                    Q2_Lookup_y = 1
                    Q2_Lookup_z = 0
                elif event.key == pygame.K_q:
                    Q2_View_x = 0
                    Q2_View_y = 50
                    Q2_View_z = 0
                    Q2_Rotation_x = 0
                    Q2_Rotation_y = 0
                    Q2_Rotation_z = 0
                    Q2_Lookup_x = 0
                    Q2_Lookup_y = 0
                    Q2_Lookup_z = 1
                elif event.key == pygame.K_e:
                    Q2_View_x = 0
                    Q2_View_y = -50
                    Q2_View_z = 0
                    Q2_Rotation_x = 0
                    Q2_Rotation_y = 0
                    Q2_Rotation_z = 0
                    Q2_Lookup_x = 0
                    Q2_Lookup_y = 0
                    Q2_Lookup_z = 1

            # Q3 Keyboard Inputs: EXTRA CREDIT: ROTATION CONTROL
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    rotation_speed += 1  # Increase rotation speed
                elif event.key == pygame.K_DOWN:
                    rotation_speed = max(1, rotation_speed - 1)  # Decrease rotation speed, minimum speed of 1


        # obtain the current model-view matrix after mouse rotation (if any)
        curmodelMatrix = glGetFloat(GL_MODELVIEW_MATRIX)

        # reset the current view to the initial view
        if (bResetModelMatrix):
            glLoadMatrixf(initmodelMatrix)
            
            #Q1 Values
            Q1_offset_x = 0
            Q1_offset_y = 0

            #Q2 Values
            Q2_View_x = 0
            Q2_View_y = 0
            Q2_View_z = 50
            Q2_Rotation_x = 0
            Q2_Rotation_y = 0
            Q2_Rotation_z = 0
            Q2_Lookup_x = 0
            Q2_Lookup_y = 1
            Q2_Lookup_z = 0
            

        
        # transform the camera and draw the model
        glPushMatrix()
        glLoadMatrixf(initmodelMatrix)

        #TODO: Q1: Modify the below gluLookAt()
        if whichQuestion == 1:
            gluLookAt(Q1_offset_x, Q1_offset_y, 50, Q1_offset_x, Q1_offset_y, 0, 0, 1, 0) 
        
        #TODO: Q2: Modify the below gluLookAt()
        elif whichQuestion == 2:
            gluLookAt(Q2_View_x, Q2_View_y, Q2_View_z, Q2_Rotation_x, Q2_Rotation_y, Q2_Rotation_z, Q2_Lookup_x, Q2_Lookup_y, Q2_Lookup_z)
        
        #TODO: Bonus: Modify the below gluLookAt()
        elif whichQuestion == 3:
            eyeX = 50 * math.cos(math.radians(angle))
            eyeZ = 50 * math.sin(math.radians(angle))
            eyeY = 20  # camera height
            centerX, centerY, centerZ = 0, 0, 0  # Looking at the center
            gluLookAt(eyeX, eyeY, eyeZ, centerX, centerY, centerZ, 0, 1, 0)
            angle = (angle + rotation_speed) % 360  # Increment angle, reset after 360


        glPushMatrix()
        glMultMatrixf(curmodelMatrix) # multiply with the m-v matrix after mouse rotation
        draw_Scarecrow()
        glPopMatrix()
        drawAxes()
        glPopMatrix()

        pygame.display.flip()
        pygame.time.wait(10)

main()