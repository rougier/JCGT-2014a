GPU-accelerated Antialiased Dashed Stroked Polylines
Copyright (C) 2013 Nicolas P. Rougier. All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice,
   this list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright
   notice, this list of conditions and the following disclaimer in the
   documentation and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY NICOLAS P. ROUGIER ''AS IS'' AND ANY EXPRESS OR
IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO
EVENT SHALL NICOLAS P. ROUGIER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT,
INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF
THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

The views and conclusions contained in the software and documentation are
those of the authors and should not be interpreted as representing official
policies, either expressed or implied, of Nicolas P. Rougier.


Accompanying code for the article "GPU-accelerated Antialiased Dashed Stroked
Polylines" submitted to the Journal of Computer Graphic Techniques


Abstract 
--------

Dashed stroked path is a widely-used feature to be found in the vast majority
of vector drawing software and/or library. They allow, for example, to
highlight a given path such as the current selection in a drawing software or
to distinguish curves in the case of a scientific plotting package. I introduce
in this paper a GPU-accelerated method for rendering arbitrary dash patterns
along any continuous polyline as long as an arc-length parametrization can be
found. The proposed method does not tesselate individual dash patterns and
allow for fast and nearly accurate rendering of any user-defined dash pattern
and caps.

Content
-------

• README.txt This file
• data/ Data directory (*.svg)
• obj/ Objects directory (*.obj)
• shaders/ Shaders directory (*.vert, *.frag)
• arc.py Arc/elliptical arc (translated from AGG library)
• curves.py Bezier curves (translated from AGG library)
• path.py Path objects
• polyhedra.py Polyhedra construction (icosahedron)
• shader.py Shaders object
• dynamic_buffer.py Dynamically resizeable buffer
• vertex_buffer.py Vertex Buffer class
• collection.py Dynamic collection as vertex buffer
• transforms.py Standard transforms
• dash_atlas.py Dash atlas
• dash_lines_2D.py Dash line colection (2D)
• dash_lines_3D.py Dash line colection (3D)
• raw_lines_2D.py Raw line colection (2D, for benchmark only)
• solid_lines_2D.py Solid line colection (2D, for benchmark only)
• demo-*.py Actual demos
• unfold-bezier.py Show how to unfold a folded polyline
• benchmark.py Benchmark script


Benchmarks
----------

To run benchmarks, just ran the benchmark.sh script and wait for all the results.
Then, report output and into benchmark.txt and run the file using python.
