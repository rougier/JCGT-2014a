#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
import sys
import math
import numpy as np
import OpenGL.GL as gl
import OpenGL.GLUT as glut
import polyhedra

from shader import Shader
from vertex_buffer import VertexBuffer
from transforms import perspective, translate, rotate, scale
from dash_lines_3D import DashLines


def display():
    global projection, view
    global theta, phi

    theta += .025
    phi += .025
    gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
    

    u_model = np.eye(4, dtype=np.float32)
    rotate(u_model, theta, 0,0,1)
    rotate(u_model, phi, 0,1,0)
    translate(u_model, 0,0,-5)

    shader.bind()
    shader.uniformf('u_color', 1.0, 1.0, 1.0, 1.0 )
    shader.uniform_matrixf('u_view', u_view)
    shader.uniform_matrixf('u_projection', u_projection)
    shader.uniform_matrixf('u_model', u_model)
    gl.glEnable( gl.GL_POLYGON_OFFSET_FILL )
    obj.draw( gl.GL_TRIANGLES )
    gl.glDisable( gl.GL_POLYGON_OFFSET_FILL )
    gl.glDepthMask( gl.GL_FALSE );
    shader.uniformf('u_color', 0.0, 0.0, 0.0, 0.1 )
    outline.draw( gl.GL_LINES )
    gl.glDepthMask( gl.GL_TRUE )
    gl.glUseProgram( 0 )


    u_model = np.identity(4,dtype=np.float32)
    rotate(u_model, theta, 0,1,0)
    rotate(u_model, phi, 1,0,0)
    translate(u_model, 0,0,-5)
    u_viewport = gl.glGetIntegerv( gl.GL_VIEWPORT )
    u_viewport = np.array(u_viewport,dtype=np.float32)
    lines.draw( uniforms= {'u_projection': u_projection,
                           'u_model' :     u_model,
                           'u_view' :      u_view,
                           'u_viewport' :  u_viewport})

    glut.glutSwapBuffers()


def reshape(width,height):
    global u_projection
    gl.glViewport(0, 0, width, height)
    u_projection = perspective( 25.0, width/float(height), 2.0, 10.0 )

def keyboard( key, x, y ):
    if key == '\033':
        sys.exit( )

def on_timer(fps):
    lines.dash_phase += 0.1
    glut.glutTimerFunc(1000/fps, on_timer, fps)
    glut.glutPostRedisplay()


# -----------------------------------------------------------------------------
if __name__ == '__main__':
    fps = 60

    glut.glutInit(sys.argv)
    # HiDPI support for retina display
    # This requires glut from http://iihm.imag.fr/blanch/software/glut-macosx/
    if sys.platform == 'darwin':
        import ctypes
        from OpenGL import platform
        try:
            glutInitDisplayString = platform.createBaseFunction( 
                'glutInitDisplayString', dll=platform.GLUT, resultType=None, 
                argTypes=[ctypes.c_char_p],
                doc='glutInitDisplayString(  ) -> None', 
            argNames=() )
            text = ctypes.c_char_p("rgba stencil double samples=8 hidpi")
            glutInitDisplayString(text)
        except:
            pass

    glut.glutInitDisplayMode(glut.GLUT_DOUBLE | glut.GLUT_RGBA | glut.GLUT_DEPTH)
    glut.glutCreateWindow('Dashed lines on sphere')
    glut.glutReshapeWindow(1000,1000)
    glut.glutDisplayFunc(display)
    glut.glutReshapeFunc(reshape)
    glut.glutKeyboardFunc(keyboard )
    glut.glutTimerFunc(1000/fps, on_timer, fps)

    # Some init
    gl.glPolygonOffset( 1, 1 )
    gl.glClearColor( 1, 1, 1, 1 )
    gl.glBlendFunc( gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA )
    gl.glEnable( gl.GL_LINE_SMOOTH )
    gl.glEnable( gl.GL_DEPTH_TEST )
    gl.glEnable( gl.GL_BLEND )


    u_projection = np.eye(4).astype( np.float32 )
    u_view = np.eye(4).astype( np.float32 )
    u_model = np.eye(4).astype( np.float32 )

    theta,phi = 45, 45

    num_subdivisions = 4
    verts, faces = polyhedra.icosahedron()
    for x in xrange(num_subdivisions):
        verts, faces = polyhedra.subdivide(verts, faces)
    vtype = [('position', np.float32, 3),
             ('color',    np.float32, 4)] 
    V = np.zeros(len(verts), dtype=vtype)
    V['position'] = verts
    V['color'] = 1,1,1,1
    obj = VertexBuffer(vtype)
    obj.append(V, faces)
    outline = VertexBuffer(vtype)
    I = []
    for f in faces:
        I.extend([f[0],f[1],f[1],f[2],f[2],f[0]])
    outline.append(V, I)
    shader = Shader(open("shaders/default.vert").read(),
                    open("shaders/default.frag").read())
    

    lines = DashLines()
    n = 2000
    points = np.zeros((n,3))
    T = np.linspace(0,24*2*np.pi,n)
    Z = np.linspace(-1,1,n)
    U = np.sqrt(1-Z*Z)
    X,Y = np.cos(T) * U, np.sin(T) * U
    points[:,0] = 1.02*X
    points[:,1] = 1.02*Y
    points[:,2] = 1.02*Z
    lines.append( points, fg_color=(0,0,0,1),
                  linewidth = 0.015, dash_pattern = "densely dashed", dash_caps = ('>','<'))


    glut.glutMainLoop()
