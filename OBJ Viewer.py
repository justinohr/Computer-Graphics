import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
from OpenGL.arrays import vbo
import ctypes

gCamAng = 0.
gCamHeight = 3.
gCamDistance = 8

def render():
    global gCamAng, gCamHeight, gCamDistance
    global semaphore
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

    glEnable(GL_DEPTH_TEST)

    glMatrixMode(GL_PROJECTION) # use projection matrix stack for projection transformation for correct lighting
    glLoadIdentity()
    gluPerspective(45, 1, 1,10)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(gCamDistance*np.sin(gCamAng),gCamHeight,gCamDistance*np.cos(gCamAng), 0,0,0, 0,1,0)

    drawFrame()

    glEnable(GL_LIGHTING)   # enable lighting
    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHT1)

    # position for LIGHT0
    glPushMatrix()

    lightPos = (1.,2.,3.,1.)
    glLightfv(GL_LIGHT0, GL_POSITION, lightPos)

    glPopMatrix()

    # position for LIGHT1
    glPushMatrix()

    glRotatef(120,0,1,0)
    lightPos = (1.,2.,3.,1.)
    glLightfv(GL_LIGHT1, GL_POSITION, lightPos)

    glPopMatrix()
    
    # light intensity for each color channel
    ambientLightColor0 = (.1,.1,.1,1.)
    diffuseLightColor0 = (.8,.8,.8,1.)
    
    glLightfv(GL_LIGHT0, GL_AMBIENT, ambientLightColor0)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, diffuseLightColor0)

    ambientLightColor1 = (.1,.1,.1,1.)
    diffuseLightColor1 = (.5,.5,.5,0.)
    glLightfv(GL_LIGHT1, GL_AMBIENT, ambientLightColor1)
    glLightfv(GL_LIGHT1, GL_DIFFUSE, diffuseLightColor1)
    
    # material reflectance for each color channel
    diffuseObjectColor = (1.,0.,0.,1.)
    specularObjectColor = (1.,0.,0.,1.)
    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, diffuseObjectColor)
    
    glPushMatrix()
    if semaphore > 0:
        drawObject()
    glPopMatrix()

    glDisable(GL_LIGHTING)

def drawObject():
    global gVertexArray, gNormalArray, gFaceArray
    for face in gFaceArray:
        glBegin(GL_POLYGON)
        for vertex in face:
            parse = vertex.split('/')
            if len(parse) > 2:
                if int(parse[2]) > 0 :
                    glNormal3fv(gNormalArray[int(parse[2]) - 1])
                else:
                    glNormal3fv(gNormalArray[int(parse[2])])
            if int(parse[0]) > 0 :
                glVertex3fv(gVertexArray[int(parse[0]) - 1])
            else :
                glVertex3fv(gVertexArray[int(parse[0])])
        glEnd()
            
        
def drawFrame():
    glBegin(GL_LINES)
    glColor3ub(255, 0, 0)
    glVertex3fv(np.array([0.,0.,0.]))
    glVertex3fv(np.array([1.,0.,0.]))
    glColor3ub(0, 255, 0)
    glVertex3fv(np.array([0.,0.,0.]))
    glVertex3fv(np.array([0.,1.,0.]))
    glColor3ub(0, 0, 255)
    glVertex3fv(np.array([0.,0.,0]))
    glVertex3fv(np.array([0.,0.,1.]))
    glEnd()

def key_callback(window, key, scancode, action, mods):
    global gCamAng, gCamHeight, gCamDistance
    global flag
    if action==glfw.PRESS or action==glfw.REPEAT:
        if key==glfw.KEY_1:
            gCamAng += np.radians(-10)
        elif key==glfw.KEY_3:
            gCamAng += np.radians(10)
        elif key==glfw.KEY_2:
            gCamHeight += .1
        elif key==glfw.KEY_W:
            gCamHeight += -.1
        elif key==glfw.KEY_A:
            gCamDistance -= .1
        elif key==glfw.KEY_S:
            gCamDistance += .1
        elif key==glfw.KEY_Z:
            if flag == 0:
                glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
                flag += 1
            else:
                glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
                flag -= 1

def drop_callback(window, paths):
    global gVertexArray, gNormalArray, gFaceArray, semaphore
    semaphore = 1
    gVertexArray = list()
    gNormalArray = list()
    gFaceArray = list()
    face3 = 0
    face4 = 0
    face5 = 0
    print("File name: " + paths[0])
    file = open(paths[0], "r")
    while(True):
        temp = list()
        line = file.readline()
        if not line:
            break
        parse = line.split()
        if len(parse) == 0: # handle empty line
            continue
        elif parse[0] == 'v':
            for unit in parse[1:]:
                temp.append(float(unit))
            gVertexArray.append(temp)
        elif parse[0] == 'vn':
            for unit in parse[1:]:
                temp.append(float(unit))
            gNormalArray.append(temp)
        elif parse[0] == 'f':
            if len(parse[1:]) == 3:
                face3 += 1
            elif len(parse[1:]) == 4:
                face4 += 1
            else:
                face5 += 1
            gFaceArray.append(parse[1:])
    print("Total number of faces: " + str(face3 + face4 + face5))
    print("Number of faces with 3 vertices: " + str(face3))
    print("Number of faces with 4 vertices: " + str(face4))
    print("Number of faces with more than 4 vertices: " + str(face5))
    file.close()
    
def main():
    global semaphore, flag
    semaphore = 0
    flag = 0
    if not glfw.init():
        return
    window = glfw.create_window(640,640,'2016025587', None,None)
    if not window:
        glfw.terminate()
        return
    glfw.make_context_current(window)
    glfw.set_key_callback(window, key_callback)
    glfw.set_drop_callback(window, drop_callback)
    glfw.swap_interval(1)
    
    while not glfw.window_should_close(window):
        glfw.poll_events()
        render()
        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()
			
