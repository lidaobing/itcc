/* $Id$ */

#include <Python.h>
#include <xtcio.h>

/* extern int open_xtc(char *filename,char *mode); */

static PyObject*
open_xtc_wrap(PyObject* self, PyObject* args)
{
  char* filename;
  char* mode;
  int result;
  if(!PyArg_ParseTuple(args, "ss",
		       &filename, &mode)) {
    return NULL;
  }

  result = open_xtc(filename, mode);
  return Py_BuildValue("i", result);
}

/* extern void close_xtc(int fp); */

static PyObject*
close_xtc_wrap(PyObject* self, PyObject* args)
{
  int fp;
  if(!PyArg_ParseTuple(args, "i",
		       &fp)) {
    return NULL;
  }
  close_xtc(fp);
  Py_INCREF(Py_None);
  return Py_None;
}

/* extern int write_xtc(int fp, */
/* 	       	        int natoms,int step,real time, */
/* 		        matrix box,rvec *x,real prec); */

static PyObject*
write_xtc_wrap(PyObject* self, PyObject* args)
{
  int fp;
  int natoms;
  int step;
  double time;
  matrix box;
  rvec* x;
  double prec;

  int result;

  PyObject* py_box;
  PyObject* py_x;

  int i, j;
  
  if(!PyArg_ParseTuple(args, "iiidOOd",
		       &fp, &natoms, &step, &time,
		       &py_box, &py_x, &prec)) {
    return NULL;
  }

  assert(PyTuple_Size(py_box) == 3);
  for(i = 0; i < 3; ++i) {
    PyObject* vec;
    vec = PyTuple_GET_ITEM(py_box, i);
    assert(PyTuple_Size(vec) == 3);
    for(j = 0; j < 3; ++j) {
      box[i][j] = PyFloat_AsDouble(PyTuple_GET_ITEM(vec, j));
    }
  }

  x = malloc(sizeof(rvec) * natoms);
  if(x == 0) {
    perror("write_xtc");
    return NULL;
  }
  
  assert(PyTuple_Size(py_x) == natoms);
  for(i = 0; i < natoms; ++i) {
    PyObject* vec;
    vec = PyTuple_GET_ITEM(py_x, i);
    assert(PyTuple_Size(vec) == 3);
    for(j = 0; j < 3; ++j) {
      x[i][j] = PyFloat_AsDouble(PyTuple_GET_ITEM(vec, j));
    }
  }

  result = write_xtc(fp, natoms, step, time,
		     box, x, prec);
  free(x);
  if(result == 0) {
    Py_INCREF(Py_False);
    return Py_False;
  } else {
    assert(result == 1);
    Py_INCREF(Py_True);
    return Py_True;
  }
}

static PyMethodDef _gmx_xtcio_methods[] = {
  {"open_xtc", open_xtc_wrap, METH_VARARGS,
   "open_xtc(name, mode) -> fd\n"
   "\n"
   "name and mode is string, fd is integer\n"},
  {"close_xtc", close_xtc_wrap, METH_VARARGS,
   "close_xtc(fd) -> None\n"
   "\n"
   "fd is the integer return by open_xtc.\n"},
  {"write_xtc", write_xtc_wrap, METH_VARARGS,
   "write_xtc(fd, natoms, step, time, box, coords, prec) -> bool\n"
   "\n"
   "fd is the integer return by open_xtc.\n"
   "natoms is number of atoms, interger.\n"
   "step is interger and time is float.\n"
   "box is 3*3 float tuple.\n"
   "coords is natoms*3 float tuple.\n"
   "prec is a float.\n"},
  {NULL, NULL, 0, NULL}};

PyMODINIT_FUNC
init_gmx_xtcio(void)
{
  (void) Py_InitModule("_gmx_xtcio", _gmx_xtcio_methods);
}
