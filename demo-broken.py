#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Copyright (C) 2013 Nicolas P. Rougier. All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#  1. Redistributions of source code must retain the above copyright notice,
#     this list of conditions and the following disclaimer.
#
#  2. Redistributions in binary form must reproduce the above copyright
#     notice, this list of conditions and the following disclaimer in the
#     documentation and/or other materials provided with the distribution.
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
# ----------------------------------------------------------------------------
import numpy as np
import OpenGL.GL as gl
from transforms import ortho

def on_display():
    gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
    path.draw(uniforms= {'u_projection': u_projection,
                         'u_model' : u_model, 'u_view' : u_view})
    glut.glutSwapBuffers()
    
def on_reshape(width, height):
    gl.glViewport(0, 0, width, height)
    u_projection[...] = ortho(0,width,0,height,-1,1)

def on_keyboard(key, x, y):
    if key == '\033':
        sys.exit()

def on_timer(fps):
    path.dash_phase -= .01
    glut.glutTimerFunc(1000/fps, on_timer, fps)
    glut.glutPostRedisplay()

def star(inner=0.5, outer=1.0, n=5):
    R = np.array( [inner,outer]*n)
    T = np.linspace(0,2*np.pi,2*n,endpoint=False)
    P = np.zeros((2*n,2))
    P[:,0]= R*np.cos(T)
    P[:,1]= R*np.sin(T)
    return P

# -----------------------------------------------------------------------------
if __name__ == '__main__':
    import sys
    import math
    import OpenGL.GLUT as glut
    from dash_lines_2D import DashLines

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

    glut.glutInitDisplayMode(glut.GLUT_DOUBLE | glut.GLUT_RGB | glut.GLUT_DEPTH)
    glut.glutInitWindowSize(1600,800)
    glut.glutCreateWindow("2D stroked path")
    glut.glutDisplayFunc(on_display)
    glut.glutReshapeFunc(on_reshape)
    glut.glutKeyboardFunc(on_keyboard)
    fps = 60
    glut.glutTimerFunc(1000/fps, on_timer, fps)
    
    # Some init
    gl.glBlendFunc( gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA )
    gl.glDisable( gl.GL_DEPTH_TEST )
    gl.glEnable( gl.GL_BLEND )
    gl.glClearColor(1.0,1.0,1.0,1.0)

    u_projection = np.eye(4).astype( np.float32 )
    u_view = np.eye(4).astype( np.float32 )
    u_model = np.eye(4).astype( np.float32 )

    path = DashLines()

    points = np.array( [ (100.,450.), (300.,650.), (500.,450.), (700,650) ])
    w = 75
    closed = False

    def add_line(points,dash_pattern, linejoin, dash_caps):
        path.append(points, linewidth = w, closed=closed, linejoin = linejoin,
                    color=(0,0,0,.5), dash_pattern='solid', linecaps = dash_caps)
        path.append(points, linewidth = w-2, closed=closed, linejoin = linejoin, 
                    color=(1,1,1,1), dash_pattern='solid', linecaps = dash_caps)
        path.append(points, linewidth = w-4, closed=closed, dash_caps = dash_caps,
                    linejoin = linejoin, color=(.75,.75,1,1), dash_pattern=dash_pattern,
                    linecaps = dash_caps)

    add_line( points,            'dashed', 'round', ('(',')'))
    add_line( points+(0,-300),   'densely dotted', 'miter', ('<','>'))
    add_line( points+(800,00),   'dotted', 'bevel', ('=','='))
    add_line( points+(800,-300), 'custom', 'miter', ('|','|'))

    glut.glutMainLoop()
