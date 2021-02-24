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
import math
import itertools
import numpy as np
import matplotlib
matplotlib.rcParams['toolbar'] = 'None'
import matplotlib.pyplot as plt


from glagg import curve3_bezier, curve4_bezier

size = 1200,1000
dpi = 72.0
figsize= size[0]/float(dpi),size[1]/float(dpi)

matplotlib.rcParams['figure.dpi']  = 72.0
matplotlib.rcParams['savefig.dpi'] = 72.0
matplotlib.rcParams['xtick.major.size'] = 0
matplotlib.rcParams['xtick.minor.size'] = 0
matplotlib.rcParams['ytick.major.size'] = 0
matplotlib.rcParams['ytick.minor.size'] = 0

fig = plt.figure(figsize=figsize, dpi=dpi, facecolor="white")
axes = fig.add_axes([0.0, 0.0, 1.0, 1.0], frameon=False, aspect=1)
axes.set_xlim(0,size[0])
axes.set_ylim(0,size[1])
axes.set_xticks([])
axes.set_yticks([])

# ------------------------------------------------------------ intersection ---
def intersection( p1, p2, p3, p4):
    x1,y1 = p1
    x2,y2 = p2
    x3,y3 = p3
    x4,y4 = p4
    den = (x2-x1) * (y4-y3) - (y2-y1) * (x4-x3);
    if math.fabs(den) < 1e-20: return None
    nom1 = (x4-x3) * (y1-y3) - (y4-y3) * (x1-x3)
    nom2 = (x2-x1) * (y1-y3) - (y2-y1) * (x1-x3)
    ua = nom1 / den
    ub = nom2 / den
    if  0.0 <= ua <= 1.0 and  0.0 <= ub <= 1.0:
        return p1 + ua*(p2-p1)
    return None

# ------------------------------------------------------------ intersection ---
def intersection2( p1, p2, p3, p4):
    x1,y1 = p1
    x2,y2 = p2
    x3,y3 = p3
    x4,y4 = p4
    den = (x2-x1) * (y4-y3) - (y2-y1) * (x4-x3);
    if math.fabs(den) < 1e-20: return None
    nom1 = (x4-x3) * (y1-y3) - (y4-y3) * (x1-x3)
    nom2 = (x2-x1) * (y1-y3) - (y2-y1) * (x1-x3)
    ua = nom1 / den
    ub = nom2 / den
    if  0.0 <= ua and  0.0 <= ub <= 1.0:
        return p1 + ua*(p2-p1)
    return None


# ------------------------------------------------------------------- curve ---
def curve_thicken(V, width, unfold=True):
    n = len(V)
    T = V[1:] - V[:-1]
    L = np.sqrt((T**2).sum(axis=1))
    T /= L.reshape(n-1,1)
    T = np.append(T,T[-1]).reshape(n,2)
    N = np.zeros((n,2))
    N[:,0],N[:,1] = -T[:,1], +T[:,0]
    V0 = V + N*width/2.0
    V1 = V - N*width/2.0
    if not unfold:
        return V0,V1

    V0_ = V0.copy()
    V1_ = V1.copy()
    
    i = 0
    while i < (n-1):
        for j in range(n-2,i+2,-1):
            p1,p2 = V0[i], V0[i+1]
            p3,p4 = V0[j], V0[j+1]
            p = intersection( p1, p2, p3, p4)
            if p is not None:
                V0[i+1:j+1] = p
                for k in range(i+1,j+1):
                    for l in range(0,n-1):
                        p = intersection2(V0[k], V[k], V1_[l], V1_[l+1])
                        if p is not None:
                            V1[k] = p
                            break
                i = j
                break
        i += 1

    i = 0
    while i < (n-1):
        for j in range(n-2,i+2,-1):
            p1,p2 = V1[i], V1[i+1]
            p3,p4 = V1[j], V1[j+1]
            p = intersection( p1, p2, p3, p4)
            if p is not None:
                V1[i+1:j+1] = p
                for k in range(i+1,j+1):
                    for l in range(0,n-1):
                        p = intersection2(V1[k], V[k], V0_[l], V0_[l+1])
                        if p is not None:
                            V0[k] = p
                            break
                i = j
                break
        i += 1
    return V0,V1

# -----------------------------------------------------------------------------
def draw_curve(V,V0,V1,T=(0,0)):
    V  = V.copy() + T
    V0 = V0.copy() + T
    V1 = V1.copy() + T
    plt.scatter(V[:,0], V[:,1], s=20, 
                facecolor='w', edgecolor='0.0',zorder=5,lw=.5)
    plt.scatter(V0[:,0], V0[:,1], s=15,
                facecolor='w', edgecolor='.5',zorder=5,lw=.5)
    plt.scatter(V1[:,0], V1[:,1], s=15,
                facecolor='w', edgecolor='.5',zorder=5,lw=.5)
    plt.plot(V[:,0], V[:,1], color='0.0')
    plt.plot(V0[:,0], V0[:,1], color='0.75')
    plt.plot(V1[:,0], V1[:,1], color='0.75')
    for i in range(len(V)):
        A,B = V0[i], V1[i]
        if i == 30:
            plt.plot( [A[0],B[0]], [A[1],B[1]], color='r', lw=2)
        else:
            plt.plot( [A[0],B[0]], [A[1],B[1]], color='k', lw=.5)


width = 175
p0,p1,p2 = np.array([(150.,100.), (300.,700.), (450,100)])
p0,p1,p2 = np.array([p0,p1,p2])
V = curve3_bezier( p0, p1, p2 )

V0,V1 = curve_thicken(V, width, unfold=False)
draw_curve(V,V0,V1,(0,50))
plt.text(300,50,"Folded",ha='center',va='center',fontsize=32)

V0,V1 = curve_thicken(V, width, unfold=True)
draw_curve(V,V0,V1,(600,50))
plt.text(900,50,"Unfolded",ha='center',va='center',fontsize=32)

#p0, p1, p2, p3 = (100.,100.), (450.,500.), (150.,500.),(500,100)
p0, p1, p2, p3 = (100.,300.), (200.,600.), (400,0.), (500.,300.)
#p0, p1, p2, p3 = (200.,150.), (-200.,450.), (800,450.), (400.,150.)

p0,p1,p2,p3 = np.array([p0,p1,p2,p3])
V = curve4_bezier( p0, p1, p2, p3)

V0,V1 = curve_thicken(V, width, unfold=False)
draw_curve(V,V0,V1,(0,500))
#plt.text(300,550,"Folded",ha='center',va='center',fontsize=48)
V0,V1 = curve_thicken(V, width, unfold=True)
draw_curve(V,V0,V1,(600,500))
#plt.text(900,550,"Unfolded",ha='center',va='center',fontsize=48)

plt.savefig("folding.pdf")
plt.show()
