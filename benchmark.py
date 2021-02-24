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
import sys
from transforms import ortho

def on_display():
    gl.glClearColor(1,1,1,1)
    gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
    if collection:
        collection.draw(uniforms= {'u_projection': u_projection,
                                   'u_model' : u_model,
                                   'u_view' : u_view})
    glut.glutSwapBuffers()


def on_reshape(width, height):
    gl.glViewport(0, 0, width, height)
    u_projection[...] = ortho(0,width,0,height,-1,1)

def on_idle():
    global t, t0, frames, framecount
    if frames == 0:
        t0 = glut.glutGet( glut.GLUT_ELAPSED_TIME )
    frames = frames + 1
    if frames > framecount:
        t = glut.glutGet( glut.GLUT_ELAPSED_TIME )
        print ( (t-t0)/1000.0 )
        #print "Rendered 5000 frames in %g second(s)" % ( (t-t0)/1000.0 )
        #print "1 frame = %f"%( ((t-t0)/1000.0)  / 5000)
        sys.exit()
    glut.glutPostRedisplay()


# -----------------------------------------------------------------------------
if __name__ == '__main__':
    import sys
    import numpy as np
    import OpenGL.GL as gl
    import OpenGL.GLUT as glut
    from raw_lines_2D import RawLines
    from solid_lines_2D import SolidLines
    from dash_lines_2D import DashLines
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-method",
                        help="Rendering method",  type=str, default='none')
    parser.add_argument("-width",
                        help="Window width", type=int, default=800)
    parser.add_argument("-height",
                        help="Window height", type=int, default=800)
    parser.add_argument("-linetype",
                        help="Line type (segment or polyline)", type=str, default='segment')
    parser.add_argument("-linewidth",
                        help="Line width",        type=float, default=1.0)
    parser.add_argument("-linecount",
                        help="Number of segment", type=int, default=10000)
    parser.add_argument("-framecount",
                        help="Number of frame to measure", type=int, default=5000)
    args = parser.parse_args()


    u_projection = np.eye(4).astype( np.float32 )
    u_view = np.eye(4).astype( np.float32 )
    u_model = np.eye(4).astype( np.float32 )
    t0, frames = glut.glutGet(glut.GLUT_ELAPSED_TIME), 0

    width = args.width
    height = args.height
    method = args.method
    framecount = args.framecount
    linetype = args.linetype
    linewidth = args.linewidth
    antialias = 1.0
    linecount = args.linecount
    color = (0,0,0,1)
    np.random.seed(1)

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
    glut.glutInitWindowSize(width, height)
    glut.glutCreateWindow("Benchmark")
    glut.glutDisplayFunc(on_display)
    glut.glutReshapeFunc(on_reshape)
    glut.glutIdleFunc(on_idle)

    # Some init
    gl.glBlendFunc( gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA )
    gl.glDisable( gl.GL_DEPTH_TEST )
    gl.glEnable( gl.GL_BLEND )
    gl.glClearColor(1.0,1.0,1.0,1.0)

    if method == 'none':
        collection = None
        dash = None
    elif method == 'raw':
        collection = RawLines()
        dash = None
    elif method == 'solid':
        collection = SolidLines()
        dash = None
    elif method == 'dash-solid':
        collection = DashLines()
        dash = 'solid'
    elif method == 'dash-dotted':
        collection = DashLines()
        dash = 'dotted'
    else:
        raise RuntimeError("Unknown method")

    if collection is not None:
        if linetype == 'polyline':
            V = np.empty((linecount,2))
            V[:,0] = np.random.uniform(0,width,linecount)
            V[:,1] = np.random.uniform(0,height,linecount)
            if dash:
                collection.append(V, linewidth=linewidth, dash_pattern=dash, color=color)
            else:
                collection.append(V, linewidth=linewidth, color=color)
        elif linetype == 'segment':
            for i in range(linecount):
                V = np.empty((2,2))
                V[:,0] = np.random.uniform(0,width,2)
                V[:,1] = np.random.uniform(0,height,2)
                if dash:
                    collection.append(V, linewidth=linewidth, dash_pattern=dash, color=color)
                else:
                    collection.append(V, linewidth=linewidth, color=color)
        else:
            raise RuntimeError("Unknown method")

    glut.glutMainLoop()
