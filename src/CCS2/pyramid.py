# -*- coding: utf8 -*-
import Numeric
import math
from Scientific.Geometry import Tensor, Vector
from Scientific.Geometry.Transformation import Translation, Rotation, RotationTranslation

__all__ = ['pyramid']

def construct_transform_matrixA(O, Ox, Oy, Oz):
    "建坐标变换矩阵，新的坐标系的原点位于O, x轴在Ox上，..., 坐标变换从frame->WC"
    tensor = Tensor([[Ox[0], Oy[0], Oz[0]],
                     [Ox[1], Oy[1], Oz[1]],
                     [Ox[2], Oy[2], Oz[2]]])
    vector = O
    trans = RotationTranslation(tensor, vector)
    return trans

def construct_both_transform_matrix(A, B, C):
    """建坐标变换矩阵，新的坐标系的原点位于A, x轴在AB上，z轴垂直于ABC平面,
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

if __name__ == '__main__':
    A = Vector([0.147056, 1.359141, 1.933333])
    B = Vector([1.274109, 1.429382, 2.842904])
    C = Vector([1.654506, 2.815342, 3.035033])
    #  3.089963    2.901247    3.220999 
 
    print pyramid(A,B,C,3.563, 2.368, 1.450)
