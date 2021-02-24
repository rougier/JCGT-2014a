#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (C) 2013 Nicolas P. Rougier. All rights reserved.
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
import numpy as np
import OpenGL.GL as gl
from transforms import ortho

# -------------------------------------
def on_display():
    gl.glClearColor(1,1,1,1)
    gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
    collection.draw(uniforms= {'u_projection': u_projection,
                               'u_model' : u_model,
                               'u_view' : u_view})
    glut.glutSwapBuffers()

# -------------------------------------
def on_reshape(width, height):
    gl.glViewport(0, 0, width, height)
    u_projection[...] = ortho(0,width,0,height,-1,1)
    collection.scale = min(width, height)

# -------------------------------------
def on_keyboard(key, x, y):
    if key == '\033': sys.exit()

# -------------------------------------
def on_special( key, x, y ):
    if key == glut.GLUT_KEY_LEFT:
        collection.dash_phase += 0.05
    elif key == glut.GLUT_KEY_RIGHT:
        collection.dash_phase -= 0.05
    glut.glutPostRedisplay()


# -------------------------------------
if __name__ == '__main__':
    import sys
    import OpenGL.GLUT as glut

    from curves import curve3_bezier, curve4_bezier
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
    glut.glutInitWindowSize(1000, 1000)
    glut.glutCreateWindow("Dashed & antialiased bezier curve [Arrow keys change offset]")
    glut.glutDisplayFunc(on_display)
    glut.glutReshapeFunc(on_reshape)
    glut.glutKeyboardFunc(on_keyboard)
    glut.glutSpecialFunc(on_special)

    # Some init
    gl.glBlendFunc( gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA )
    gl.glDisable( gl.GL_DEPTH_TEST )
    gl.glEnable( gl.GL_BLEND )
    gl.glClearColor(1.0,1.0,1.0,1.0)
    u_projection = np.eye(4).astype( np.float32 )
    u_view = np.eye(4).astype( np.float32 )
    u_model = np.eye(4).astype( np.float32 )

    collection = DashLines()

    # ---------------------------------
    points = np.array([[.1, .6], [.5, 1.], [.9, .6]])
    vertices = curve3_bezier(*points)

    closed = False
    collection.append(vertices, color=(0,0,0,1), linewidth=104,
                      dash_pattern = 'solid', linecaps=('>','<'), closed=closed)
    collection.append(vertices, color=(1,1,1,1), linewidth=102,
                      dash_pattern = 'solid', linecaps=('>','<'), closed=closed)
    collection.append(vertices, color=(0.75,0.75,1.00,1.00), linewidth=100,
                      dash_pattern = 'dashed', dash_caps=('>','<'),
                      linecaps=('>','<'), closed=closed)


    # ---------------------------------
    vertices = curve3_bezier(*(points + [0, -0.4]))
    collection.append(vertices, color=(0,0,0,1), linewidth=104,
                      dash_pattern = 'solid', linecaps=('=','='), closed=closed)
    collection.append(vertices, color=(1,1,1,1), linewidth=102,
                      dash_pattern = 'solid', linecaps=('=','='), closed=closed)
    collection.append( vertices, color=(0.75,0.75,1.00,1.0),
                       linewidth=100,  linecaps = ('|','|'), closed=closed,
                       dash_pattern = 'custom', dash_caps=('|','|') )

    # ---------------------------------
    vertices = curve3_bezier(*(points + [0, -0.2]))
    collection.append(vertices, color=(0,0,0,1), linewidth=104,
                      dash_pattern = 'solid', linecaps=('o','o'), closed=closed)
    collection.append(vertices, color=(1,1,1,1), linewidth=102,
                      dash_pattern = 'solid', linecaps=('o','o'), closed=closed)
    collection.append( vertices, color=(0.75,0.75,1.00,1.0),
                       linewidth=100,  linecaps = ('o','o'), closed=closed,
                       dash_pattern = 'densely dotted', dash_caps=('o','o') )


    glut.glutMainLoop()
