#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2013 Nicolas P. Rougier. All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
# 
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
# 
# THIS SOFTWARE IS PROVIDED BY NICOLAS P. ROUGIER ''AS IS'' AND ANY EXPRESS OR
# IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO
# EVENT SHALL NICOLAS P. ROUGIER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT,
# INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF
# THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
# 
# The views and conclusions contained in the software and documentation are
# those of the authors and should not be interpreted as representing official
# policies, either expressed or implied, of Nicolas P. Rougier.
# -----------------------------------------------------------------------------

import sys
import math
import numpy as np
import OpenGL.GL as gl
import OpenGL.GLUT as glut

from shader import Shader
from vertex_buffer import VertexBuffer
from transforms import perspective, translate, rotate, scale


def load_obj(filename):
    '''
    Load vertices and faces from a wavefront .obj file and generate normals.
    '''
    data = np.genfromtxt(filename, dtype=[('type', np.character, 1),
                                          ('points', np.float32, 3)])

    # Get vertices and faces
    vertices = data['points'][data['type'] == 'v']
    faces = (data['points'][data['type'] == 'f']-1).astype(np.uint32)

    # Build normals
    T = vertices[faces]    
    N = np.cross(T[::,1 ]-T[::,0], T[::,2]-T[::,0])
    L = np.sqrt(N[:,0]**2+N[:,1]**2+N[:,2]**2)
    N /= L[:, np.newaxis]
    normals = np.zeros(vertices.shape)
    normals[faces[:,0]] += N
    normals[faces[:,1]] += N
    normals[faces[:,2]] += N
    L = np.sqrt(normals[:,0]**2+normals[:,1]**2+normals[:,2]**2)
    normals /= L[:, np.newaxis]

    # Scale vertices such that object is contained in [-1:+1,-1:+1,-1:+1]
    vmin, vmax =  vertices.min(), vertices.max()
    vertices = 2*(vertices-vmin)/(vmax-vmin) - 1

    # Center
    X,Y,Z = vertices[:,0],vertices[:,1],vertices[:,2]
    xmin, xmax = X.min(), X.max()
    ymin, ymax = Y.min(), Y.max()
    zmin, zmax = Z.min(), Z.max()
    X -= (xmax+xmin)/2.
    Y -= (ymax+ymin)/2.
    Z -= (zmax+zmin)/2.
      
    return vertices, normals, faces


def display():
    global u_projection, u_view
    global theta, phi

    theta += .23
    phi += .29
    gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)

    u_model = np.eye(4, dtype=np.float32)
    rotate(u_model, theta, 0,0,1)
    rotate(u_model, phi, 0,1,0)
    u_viewport = gl.glGetIntegerv( gl.GL_VIEWPORT )
    u_viewport = np.array(u_viewport,dtype=np.float32)

    shader.bind()
    shader.uniformf('u_color', 1.0, 1.0, 0.0, .5 )
    shader.uniform_matrixf('u_view', u_view)
    shader.uniform_matrixf('u_projection', u_projection)
    shader.uniform_matrixf('u_model', u_model)

    gl.glDisable( gl.GL_BLEND )
    gl.glColorMask(gl.GL_FALSE, gl.GL_FALSE, gl.GL_FALSE, gl.GL_FALSE)
    gl.glEnable( gl.GL_DEPTH_TEST )
    obj.draw( gl.GL_TRIANGLES )
    gl.glUseProgram( 0 )


    gl.glEnable( gl.GL_BLEND )
    gl.glColorMask(gl.GL_TRUE, gl.GL_TRUE, gl.GL_TRUE, gl.GL_TRUE)
    gl.glDisable( gl.GL_DEPTH_TEST )
    index, period = outline.dash_atlas['dashed']
    outline.dash_index = index
    outline.fg_color = (.5,.5,.5,1)
    outline.draw( uniforms= {'u_projection': u_projection,
                             'u_model' :     u_model,
                             'u_view' :      u_view,
                             'u_viewport' :  u_viewport})

    gl.glEnable( gl.GL_DEPTH_TEST )
    outline.fg_color = (0,0,0,1)
    index, period = outline.dash_atlas['solid']
    outline.dash_index = index
    outline.draw( uniforms= {'u_projection': u_projection,
                             'u_model' :     u_model,
                             'u_view' :      u_view,
                             'u_viewport' :  u_viewport})

    glut.glutSwapBuffers()


def reshape(width,height):
    global u_projection, u_view
    gl.glViewport(0, 0, width, height)
    u_projection = perspective( 45.0, width/float(height), 2.0, 10.0 )
    u_view = np.identity(4,dtype=np.float32)
    translate(u_view, 0,0,-3.5)

def keyboard( key, x, y ):
    if key == '\033':
        sys.exit( )

def on_timer(fps):
    glut.glutTimerFunc(1000/fps, on_timer, fps)
    glut.glutPostRedisplay()


if __name__ == '__main__':
    fps = 60
    from dash_lines_3D import DashLines

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
    glut.glutCreateWindow('icosahedron')
    glut.glutReshapeWindow(800,800)
    glut.glutDisplayFunc(display)
    glut.glutReshapeFunc(reshape)
    glut.glutKeyboardFunc(keyboard )
    glut.glutTimerFunc(1000/fps, on_timer, fps)

    gl.glClearColor( 1, 1, 1, 1 )
    gl.glBlendFunc( gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA )


    u_projection = np.eye(4,dtype=np.float32)
    u_view       = np.eye(4,dtype=np.float32)
    
    theta, phi = 0,0

    vtype = [('position', np.float32, 3),
             ('normal'  , np.float32, 3),
             ('color',    np.float32, 4)] 
    vertices, normals, faces = load_obj('obj/icosahedron.obj')

    V = np.zeros(len(vertices), dtype=vtype)
    V['position'] = vertices*.99
    V['color'] = 1,1,1,1
    V['normal'] = normals

    obj = VertexBuffer(vtype)
    obj.append(V, faces)
    
    outline = DashLines()
    F = np.roll(faces.repeat(2,axis=1),-1,axis=1)
    F = F.reshape(len(F)*3,2)
    F = np.sort(F,axis=1)
    G = F.view( dtype=[('p0',F.dtype),('p1',F.dtype)] )
    G = np.unique(G)
    for face in G:
        p0 = vertices[face['p0']]
        p1 = vertices[face['p1']]
        outline.append( [p0,p1], fg_color=(0,0,0,1), linewidth = 0.01,
                      dash_pattern = "dashed", dash_caps = ('o','o'))

    shader = Shader(open("shaders/default.vert").read(),
                    open("shaders/default.frag").read())

    glut.glutMainLoop()
