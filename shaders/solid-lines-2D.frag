// -----------------------------------------------------------------------------
// Copyright (C) 2013 Nicolas P. Rougier. All rights reserved.
// 
// Redistribution and use in source and binary forms, with or without
// modification, are permitted provided that the following conditions are met:
// 
// 1. Redistributions of source code must retain the above copyright notice,
//    this list of conditions and the following disclaimer.
// 
// 2. Redistributions in binary form must reproduce the above copyright
//    notice, this list of conditions and the following disclaimer in the
//    documentation and/or other materials provided with the distribution.
// 
// THIS SOFTWARE IS PROVIDED BY NICOLAS P. ROUGIER ''AS IS'' AND ANY EXPRESS OR
// IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
// MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO
// EVENT SHALL NICOLAS P. ROUGIER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT,
// INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
// (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
// LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
// ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
// (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF
// THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
// 
// The views and conclusions contained in the software and documentation are
// those of the authors and should not be interpreted as representing official
// policies, either expressed or implied, of Nicolas P. Rougier.
// -----------------------------------------------------------------------------
const float PI = 3.14159265358979323846264;
const float THETA = 15.0 * 3.14159265358979323846264/180.0;



// Compute distance to cap 
// ----------------------------------------------------------------------------
float
cap( int type, float dx, float dy, float t )
{
    float d = 0.0;
    dx = abs(dx);
    dy = abs(dy);
     
    // None
    if      (type == 0)  discard;
    // Round
    else if (type == 1)  d = sqrt(dx*dx+dy*dy);
    // Triangle in
    else if (type == 3)  d = (dx+abs(dy));
    // Triangle out
    else if (type == 2)  d = max(abs(dy),(t+dx-abs(dy)));
    // Square
    else if (type == 4)  d = max(dx,dy);
    // Butt
    else if (type == 5)  d = max(dx+t,dy);
    
    return d;
}


// Compute distance to join
// ----------------------------------------------------------------------------
float
join( in int type, in float d, in vec2 segment, in vec2 texcoord, in vec2 miter,
      in float miter_limit, in float linewidth )
{
    float dx = texcoord.x;
    
    // Round join
    // --------------------------------
    if( type == 1 )
    {
        if (dx < segment.x) {
            d = max(d,length( texcoord - vec2(segment.x,0.0)));
            //d = length( texcoord - vec2(segment.x,0.0));
        } else if (dx > segment.y) {
            d = max(d,length( texcoord - vec2(segment.y,0.0)));
            //d = length( texcoord - vec2(segment.y,0.0));
        }
    }
    
    // Bevel join
    // --------------------------------
    else if ( type == 2 )
    {
        if( (dx < segment.x) ||  (dx > segment.y) )
            d = max(d, min(abs(miter.x),abs(miter.y)));
    }
    
    // Miter limit
    // --------------------------------
    if( (dx < segment.x) ||  (dx > segment.y) )
    {
        d = max(d, min(abs(miter.x),abs(miter.y)) - miter_limit*linewidth/2.0 );
    }
    
    return d;
}



// Uniforms
// ------------------------------------
uniform sampler2D u_dash_atlas;

// Varying
// ------------------------------------
varying vec4  v_color;
varying vec2  v_segment;
varying vec2  v_angles;
varying vec2  v_linecaps;
varying vec2  v_texcoord;
varying vec2  v_miter;
varying float v_miter_limit;
varying float v_length;
varying float v_linejoin;
varying float v_linewidth;
varying float v_antialias;
varying float v_closed;

void main() 
{
    // Test if path is closed
    bool closed = (v_closed > 0.0);
    
    vec4 color = v_color;
    float dx = v_texcoord.x;
    float dy = v_texcoord.y;
    float t = v_linewidth/2.0-v_antialias;
    float width = v_linewidth;
    float d = 0.0;
   
    vec2 linecaps = v_linecaps;
    float line_start = 0.0;
    float line_stop  = v_length;

    
    d = abs(dy);
    if( (!closed) && (dx < line_start) )
    {
        d = cap( int(v_linecaps.x), abs(dx), abs(dy), t );
    }
    else if( (!closed) &&  (dx > line_stop) )
    {
        d = cap( int(v_linecaps.y), abs(dx)-line_stop, abs(dy), t );
    }
    else
    {
        d = join( int(v_linejoin), abs(dy), v_segment, v_texcoord,
                  v_miter, v_miter_limit, v_linewidth );
    }

    // Distance to border
    // ------------------------------------------------------------------------
    d = d - t;
    if( d < 0.0 )
    {
        gl_FragColor = color;
    }
    else
    {
        d /= v_antialias;
        gl_FragColor = vec4(color.xyz, exp(-d*d)*color.a);
    }
}
