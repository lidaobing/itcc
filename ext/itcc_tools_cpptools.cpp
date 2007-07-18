// $Id$

#include <Python.h>
#include <cmath>
#include "vector.hpp"

using std::sqrt;

static void
_shakeH2(const Vector & p0,
	 const Vector & p1,
	 const Vector & p2,
	 double r03,
	 double r04,
	 Vector & p3,
	 Vector & p4)
{
  static const double lenx = sqrt(1.0/3.0);
  static const double leny = sqrt(2.0/3.0);
  
  Vector v01 = (p1 - p0).normal();
  Vector v02 = (p2 - p0).normal();
  Vector vrx = (v01 + v02).normal(-lenx);
  Vector vry = v01.cross(v02).normal(leny);
  p3 = p0 + (vrx + vry) * r03;
  p4 = p0 + (vrx - vry) * r04;
  return;
}


extern "C" {
  static PyObject *
  shakeH2(PyObject * self, PyObject * args)
  {
    Vector p0, p1, p2;
    double r03, r04;
    Vector p3, p4;
    if(!PyArg_ParseTuple(args, "(ddd)(ddd)(ddd)dd",
			 &p0.x, &p0.y, &p0.z,
			 &p1.x, &p1.y, &p1.z,
			 &p2.x, &p2.y, &p2.z,
			 &r03, &r04)){
      return NULL;
    }

    _shakeH2(p0, p1, p2, r03, r04, p3, p4);
  
    return Py_BuildValue("((ddd)(ddd))",
			 p3.x, p3.y, p3.z,
			 p4.x, p4.y, p4.z);
  }

  static PyMethodDef CpptoolsMethods[] = {
    {"shakeH2", shakeH2, METH_VARARGS,
     "Caculate the H coords"},
    {NULL, NULL, 0, NULL}       
  };

  PyMODINIT_FUNC
  initcpptools(void)
  {
    (void) Py_InitModule("cpptools", CpptoolsMethods);
  }
}

int main(){
  
}
