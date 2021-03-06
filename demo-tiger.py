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

# -------------------------------------
def on_keyboard(key, x, y):
    if key == '\033': sys.exit()

# -------------------------------------
def on_idle():
    collection.dash_phase += 0.025
    global t, t0, frames
    t = glut.glutGet( glut.GLUT_ELAPSED_TIME )
    frames = frames + 1
    if t-t0 > 2500:
        print "FPS : %.2f (%d frames in %.2f second)" % (
            (frames*1000.0/(t-t0), frames, (t-t0)/1000.0))
        t0, frames = t,0
    glut.glutPostRedisplay()


# -------------------------------------
def on_motion( x, y ):
    global mouse,translate,scale
    _,_,w,h = gl.glGetIntegerv(gl.GL_VIEWPORT)
    y = h-y
    dx,dy = x-mouse[0], y-mouse[1]
    translate = [translate[0]+dx,translate[1]+dy]
    mouse = x,y
    collection.translate = translate
    glut.glutPostRedisplay()

# -------------------------------------
def on_passive_motion( x, y ):
    global mouse
    _,_,w,h = gl.glGetIntegerv(gl.GL_VIEWPORT)
    mouse = x, h-y

# -------------------------------------
def on_mouse( x, y ):
    global mouse
    _,_,w,h = gl.glGetIntegerv(gl.GL_VIEWPORT)
    mouse = x, h-y

# -------------------------------------
def on_scroll(dx, dy):
    global mouse,translate,scale

    x,y = mouse
    s = min(max(0.25,scale+.001*dy*scale), 200)
    translate[0] = x-s*(x-translate[0])/scale
    translate[1] = y-s*(y-translate[1])/scale
    translate = [translate[0], translate[1]]
    scale = s
    collection.scale = s
    collection.linewidth = s/4.0
    collection.translate = translate
    glut.glutPostRedisplay()

# -------------------------------------
def on_mouse(button, state, x, y):
    if button == 3:
        on_scroll(0,+3)
    elif button == 4:
        on_scroll(0,-3)
    else:
        return

# -------------------------------------
def on_wheel(wheel, direction, x, y):
    if wheel == 0:
        on_scroll(0,direction)
    elif wheel == 1:
        on_scroll(direction,0)


# -------------------------------------
def svg_open(filename):
    dom = xml.dom.minidom.parse(filename)
    tag = dom.documentElement
    if tag.tagName != 'svg':
        raise ValueError('document is <%s> instead of <svg>'%tag.tagName)
    path_re = re.compile(r'([MLHVCSQTAZ])([^MLHVCSQTAZ]+)', re.IGNORECASE)
    float_re = re.compile(r'(?:[\s,]*)([+-]?\d+(?:\.\d+)?)')
    path = Path()
    for tag in tag.getElementsByTagName('g'):
        for tag in tag.getElementsByTagName('path'):
            for cmd, values in path_re.findall(tag.getAttribute('d')):
                points = [float(v) for v in float_re.findall(values)]
                path.svg_parse(cmd, points)
    return path.vertices


# -----------------------------------------------------------------------------
if __name__ == '__main__':
    import sys
    import numpy as np
    import OpenGL.GL as gl
    import OpenGL.GLUT as glut
    import re
    import xml.dom
    import xml.dom.minidom
    from path import Path
    from dash_lines_2D import DashLines

    u_projection = np.eye(4).astype( np.float32 )
    u_view = np.eye(4).astype( np.float32 )
    u_model = np.eye(4).astype( np.float32 )

    t0, frames, t = glut.glutGet(glut.GLUT_ELAPSED_TIME), 0, 0
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

    glut.glutInitDisplayMode(glut.GLUT_DOUBLE | glut.GLUT_RGB)
    glut.glutInitWindowSize(1000, 1000)
    glut.glutCreateWindow("Tiger [scroll and zoom with mouse]")
    glut.glutDisplayFunc(on_display)
    glut.glutReshapeFunc(on_reshape)
    glut.glutKeyboardFunc(on_keyboard)
    glut.glutIdleFunc(on_idle)
    glut.glutMotionFunc(on_motion)
    glut.glutMouseFunc(on_mouse)
    glut.glutPassiveMotionFunc(on_passive_motion)

    # Some init
    gl.glBlendFunc( gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA )
    gl.glDisable( gl.GL_DEPTH_TEST )
    gl.glEnable( gl.GL_BLEND )
    gl.glClearColor(1.0,1.0,1.0,1.0)

    mouse = 400,400
    translate = [350,650]
    scale = 1.75

    collection = DashLines()
    def dist(v0,v1):
        x0,y0 = v0
        x1,y1 = v1
        dx,dy = (x1-x0), (y1-y0)
        return dx*dx+dy*dy

    vertices = svg_open('data/tiger.svg')

    for V in vertices:
        closed = dist(V[0],V[-1]) < 1e-10
        V = np.array(V)
        V[:,1] = -V[:,1]
        collection.append(V, closed=closed, linewidth=scale/4.0,
                          translate=translate, scale=scale,
                          dash_pattern = 'loosely dashed')

    glut.glutMainLoop()
