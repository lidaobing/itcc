# -*- coding: utf8 -*-
# $Id$
import Numeric
import math
from Scientific.Geometry import Tensor, Vector
from Scientific.Geometry.Transformation import Translation, \
     RotationTranslation

__all__ = ['pyramid']
__revision__ = '$Rev$'

def construct_transform_matrixA(O, Ox, Oy, Oz):
    """建坐标变换矩阵，新的坐标系的原点位于O, x轴在Ox上，
    ..., 坐标变换从frame->WC"""
    tensor = Tensor([[Ox[0], Oy[0], Oz[0]],
                     [Ox[1], Oy[1], Oz[1]],
                     [Ox[2], Oy[2], Oz[2]]])
    vector = O
    trans = RotationTranslation(tensor, vector)
    return trans

def construct_both_transform_matrix(A, B, C):
    """建坐标变换矩阵，新的坐标系的原点位于A,
    x轴在AB上，z轴垂直于ABC平面,
    result[1] = frame->WC
    result[0] = WC->frame"""

    O = A
    Ox = (B-A).normal()
    Oz = Ox.cross(C-A).normal()
    Oy = Oz.cross(Ox)

    result1 = construct_transform_matrixA(O, Ox, Oy, Oz)
    result2 = result1.inverse()
    return (result2, result1)

def pyramid(A, B, C, rAX, rBX, rCX):
    # 新坐标系，原点在A, x轴在AB上， z轴垂直于ABC平面
    trans = Translation(-A)
    
    trans, revtrans = construct_both_transform_matrix(A, B, C)

    A = trans(A)
    B = trans(B)
    C = trans(C)

    # 此时A,B,C坐标应为
    # A = [0.0, 0.0, 0.0]
    # B = [Bx,  0.0, 0.0]
    # C = [Cx,  Cy,  0.0]
    # 此时三个方程为
    # X[0]^2 + X[1]^2 + X[2]^2 = rAX^2
    # (X[0]-B[0])^2 + X[1]^2 + X[2]^2 = rBX^2
    # (X[0]-C[0])^2 + (X[1]-C[1])^2 + X[2]^2 = rCX^2
    #
    # X[0] = (rAX^2 - rBX^2 + B[0]^2) / (2B[0])
    # X[1] = (rAX^2 - rCX^2 + C[1]^2 + C[0]^2 - 2C[0]X[0])/2C[1]
    # X[2] = +/- sqrt(rAX^2 - X[0]^2 - X[1]^2)

    rAX2 = rAX * rAX
    rBX2 = rBX * rBX
    rCX2 = rCX * rCX

    X = Numeric.zeros(3, Numeric.Float)
    X[0] = (rAX2 - rBX2 + B[0]*B[0]) / (2 * B[0])
    X[1] = (rAX2 - rCX2 + C[1]*C[1] + C[0]*C[0] - 2*C[0]*X[0]) / (2 * C[1])

    X22 = rAX2 - X[0]*X[0] - X[1]*X[1]

    X[2] = math.sqrt(max(0.0, X22))
    result1 = revtrans(Vector(X))
    
    X[2] = -X[2]
    result2 = revtrans(Vector(X))
    return ((result1, result2), X22)

def pyramid2(A, B, rAX, rBX):
    '''known the coords of A, B and rAX, rBX, then X will be on a
    circle. return the circle center and 2 vertical axis.
    '''
    AB = B - A
    rAB = AB.length()
    if rAX + rBX < rAB or abs(rAX - rBX) > rAB:
        return (None, None, None)
    
    c = (rAX * rAX - rBX * rBX) / ( 2 * rAB * rAB) + 0.5
    rXO = math.sqrt(rAX * rAX - rXO * rXO)
    O = A + c * AB

    ABn = AB.normal()
    if abs(ABn.x()) < 0.7071:
        OXx = ABn.cross(Vector(1.0, 0.0, 0.0)).normal() * rXO
    else:
        OXx = ABn.cross(Vector(0.0, 1.0, 0.0)).normal() * rXO
    OXy = OXx.cross(ABn)
    return (O, OXx, OXy)


