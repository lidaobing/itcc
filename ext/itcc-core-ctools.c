/* $Id$ */

#include <Python.h>
#include <math.h>

typedef struct {
  double x;
  double y;
  double z;
} Point;

static Point
_vector(Point a, Point b) {
  Point c;
  c.x = b.x - a.x;
  c.y = b.y - a.y;
  c.z = b.z - a.z;
  return c;
}

static Point
_crossmulti(Point a, Point b) {
  Point c;
  c.x = a.y * b.z - a.z * b.y;
  c.y = a.z * b.x - a.x * b.z;
  c.z = a.x * b.y - a.y * b.x;
  return c;
}

static double
_dotmulti(Point a, Point b) {
  return a.x * b.x + a.y * b.y + a.z * b.z;
}


static double
_angle(Point a, Point b, Point c) {
  Point rba, rbc;
  double cosine;

  rba = _vector(b,a);
  rbc = _vector(b,c);

  cosine = _dotmulti(rba, rbc)/sqrt(_dotmulti(rba, rba) * _dotmulti(rbc,rbc));

  return acos(cosine);
}



static double 
_torsionangle(Point a, Point b, Point c, Point d) {
  Point rab, rbc, rcd;
  Point rt, ru;
  double cosine;
  double phi;

  rab = _vector(a,b);
  rbc = _vector(b,c);
  rcd = _vector(c,d);

  rt = _crossmulti(rab, rbc);
  ru = _crossmulti(rbc, rcd);

  cosine = _dotmulti(rt, ru) / sqrt(_dotmulti(rt, rt) * _dotmulti(ru,ru));

  if(cosine > 1.0) {
    cosine = 1.0;
  } else if(cosine < -1.0) {
    cosine = -1.0;
  }

  phi = acos(cosine);

  if(_dotmulti(rab, ru) < 0.0) {
    phi = -phi;
  }

  return phi;
}


static PyObject *
angle(PyObject *self, PyObject *args)
{
  Point a, b, c;
  double result;

  if (!PyArg_ParseTuple(args, "(ddd)(ddd)(ddd)", 
			&a.x, &a.y, &a.z,
			&b.x, &b.y, &b.z,
			&c.x, &c.y, &c.z)) {
        return NULL;
  }

  result = _angle(a,b,c);

  return Py_BuildValue("d", result);
}




static PyObject *
torsionangle(PyObject *self, PyObject *args)
{
  Point a, b, c, d;
  double result;

  if (!PyArg_ParseTuple(args, "(ddd)(ddd)(ddd)(ddd)", 
			&a.x, &a.y, &a.z,
			&b.x, &b.y, &b.z,
			&c.x, &c.y, &c.z,
			&d.x, &d.y, &d.z)) {

        return NULL;
  }

  result = _torsionangle(a,b,c,d);

  return Py_BuildValue("d", result);
}

static PyMethodDef CtoolsMethods[] = {
  {"torsionangle",  torsionangle, METH_VARARGS,
   "Caculate torsion angle, return in radian, range is (-pi, pi] or nan"},
  {"angle", angle, METH_VARARGS,
   "Caculate angle, return in radian"},
  {NULL, NULL, 0, NULL}       
};

PyMODINIT_FUNC
initctools(void)
{
    (void) Py_InitModule("ctools", CtoolsMethods);
}


