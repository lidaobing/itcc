// $Id$

#include <Python.h>

#include <algorithm>
#include <cmath>
#include <cassert>

using namespace std;

extern "C" {
  void dsyev_(char* jobz,
              char* uplo,
              int* n,
              double* a,
              int* lda,
              double* w,
              double* work,
              int* lwork,
              int* info);
}

/* _rmsd function is provided by Chen Hao */

/********************************************************************************
 *  double rmsd(int n, double coor1[][3], double coor2[][3], double coor[][3])  *
 *      n            : number of atoms                                          *
 *      coor1        : atom coordinates of the first structure                  *
 *      coor2        : atom coordinates of the second structure                 *
 *      coor         : transformation matrix U*(coor2)' -> (coor1)'             *
 *      return value : RMSD                                                     *
 *********************************************************************************/

double _rmsd(int n, double coor1[][3], double coor2[][3], double (&U) [4][4])
{
  if(n == 1) {
    fill_n(U[0], 4*4, 0.0);
    for(int i = 0; i < 4; ++i) {
      U[i][i] = 1.0;
    }
    for(int i = 0; i < 3; ++i) {
      U[i][3] = coor1[0][i] - coor2[0][i];
    }
    return 0.0;
  }

  int i, j, k, N=3, lwork=9, ok;
  double r, R1[3][3], R[3][3], RT[9], w[3], work[9], A[3][3], B[3][3];
  char jobz='V', uplo='U';
  double c1[3], c2[3], tmp1[n][3], tmp2[n][3], d;

  for (i=0; i<3; i++) c1[i] = c2[i] = 0;
  for (i=0; i<n; i++) {
    c1[0] += coor1[i][0];
    c1[1] += coor1[i][1];
    c1[2] += coor1[i][2];
    c2[0] += coor2[i][0];
    c2[1] += coor2[i][1];
    c2[2] += coor2[i][2];
  }
  for (i=0; i<3; i++) {
    c1[i] /= n;
    c2[i] /= n;
  }
  for (i=0; i<n; i++) {
    tmp1[i][0] = coor1[i][0] - c1[0];
    tmp1[i][1] = coor1[i][1] - c1[1];
    tmp1[i][2] = coor1[i][2] - c1[2];
    tmp2[i][0] = coor2[i][0] - c2[0];
    tmp2[i][1] = coor2[i][1] - c2[1];
    tmp2[i][2] = coor2[i][2] - c2[2];
  }

  r = 0;
  for (i=0; i<3; i++) {
    for (j=0; j<3; j++) {
      R1[i][j] = 0;
      for (k=0; k<n; k++) {
        R1[i][j] += tmp1[k][i] * tmp2[k][j];
      }
      r += R1[i][j] * R1[i][j];
    }
  }

  r = sqrt(r/3);

  for (i=0; i<3; i++)
    for (j=0; j<3; j++)
      R1[i][j] /= r;

  for (i=0; i<3; i++) {
    for (j=0; j<3; j++) {
      R[i][j] = 0;
      for (k=0; k<3; k++) {
        R[i][j] += R1[k][i] * R1[k][j];
      }
    }
  }

  for (i=0; i<3; i++) {
    for (j=0; j<3; j++) {
      RT[j+3*i] = R[j][i];
    }
  }

  dsyev_ (&jobz, &uplo, &N, RT, &N, w, work, &lwork, &ok);

  for (i=0; i<3; i++) {
    for (j=0; j<3; j++) {
      A[i][j] = RT[3*i+j];
    }
  }

  A[0][0] = A[2][1] * A[1][2] - A[2][2] * A[1][1];
  A[0][1] = A[2][2] * A[1][0] - A[2][0] * A[1][2];
  A[0][2] = A[2][0] * A[1][1] - A[2][1] * A[1][0];

  B[2][0] = R1[0][0] * A[2][0] + R1[0][1] * A[2][1] + R1[0][2] * A[2][2];
  B[2][1] = R1[1][0] * A[2][0] + R1[1][1] * A[2][1] + R1[1][2] * A[2][2];
  B[2][2] = R1[2][0] * A[2][0] + R1[2][1] * A[2][1] + R1[2][2] * A[2][2];

  r = sqrt(w[2]);
  B[2][0] /= r; B[2][1] /= r; B[2][2] /=r;

  B[1][0] = R1[0][0] * A[1][0] + R1[0][1] * A[1][1] + R1[0][2] * A[1][2];
  B[1][1] = R1[1][0] * A[1][0] + R1[1][1] * A[1][1] + R1[1][2] * A[1][2];
  B[1][2] = R1[2][0] * A[1][0] + R1[2][1] * A[1][1] + R1[2][2] * A[1][2];

  r = sqrt(w[1]);
  B[1][0] /= r; B[1][1] /= r; B[1][2] /=r;

  B[0][0] = B[2][1] * B[1][2] - B[2][2] * B[1][1];
  B[0][1] = B[2][2] * B[1][0] - B[2][0] * B[1][2];
  B[0][2] = B[2][0] * B[1][1] - B[2][1] * B[1][0];

  
  for (i=0; i<3; i++)
    for (j=0; j<3; j++)
      U[i][j] = B[0][i] * A[0][j] + B[1][i] * A[1][j] + B[2][i] * A[2][j];

  for(int i = 0; i < 3; ++i) {
    U[i][3] = c1[i];
    for(int j = 0; j < 3; ++j) {
      U[i][3] -= U[i][j] * c2[j];
    }
  }
  U[3][0] = U[3][1] = U[3][2] = 0.0;
  U[3][3] = 1.0;

  double coor[n][3];
  for (i=0; i<n; i++)
    for (j=0; j<3; j++) {
      coor[i][j] = 0;
      for (k=0; k<3; k++)
        coor[i][j] += U[j][k] * coor2[i][k];
      coor[i][j] += U[j][3];
    }
  d = 0;
  for (i=0; i<n; i++)
    for (j=0; j<3; j++)
      d += (coor[i][j] - coor1[i][j]) * (coor[i][j] - coor1[i][j]);
  d = sqrt(d / (n - 1));
  return d;
}


double
rmsd_common(PyObject* self, PyObject* args,
            double (&U) [4][4], int& len)
{
  PyObject* mol1_coords = NULL;
  PyObject* mol2_coords = NULL;

  PyObject* mol1, *mol2;
  if(!PyArg_ParseTuple(args, "OO", &mol1, &mol2)) {
    return -1.0;
  }

  if(PyObject_HasAttrString(mol1, "coords")) {
    mol1_coords = PyObject_GetAttrString(mol1, "coords");
  }
  if(PyObject_HasAttrString(mol2, "coords")) {
    mol2_coords = PyObject_GetAttrString(mol2, "coords");
  }
  PyObject* coords1 = PySequence_Fast((mol1_coords?mol1_coords:mol1), "");
  PyObject* coords2 = PySequence_Fast((mol2_coords?mol2_coords:mol2), "");

  len = PySequence_Size(coords1);
  assert(PySequence_Size(coords2) == len);

  double (*coor1)[3] = new double[len][3];
  double (*coor2)[3] = new double[len][3];
  for(int i = 0; i < len; ++i)
  {
    PyObject* vec1 = PySequence_Fast(PySequence_Fast_GET_ITEM(coords1, i), "");
    for(int j = 0; j < 3; ++j)
    {
      coor1[i][j] = PyFloat_AsDouble(PySequence_Fast_GET_ITEM(vec1, j));
    }
    Py_XDECREF(vec1);

    PyObject* vec2 = PySequence_Fast(PySequence_Fast_GET_ITEM(coords2, i), "");
    for(int j = 0; j < 3; ++j)
    {
      coor2[i][j] = PyFloat_AsDouble(PySequence_Fast_GET_ITEM(vec2, j));
    }
    Py_XDECREF(vec2);
  }
  double res = _rmsd(len, coor1, coor2, U);
  delete []coor1;
  delete []coor2;
  Py_XDECREF(coords1);
  Py_XDECREF(coords2);
  Py_XDECREF(mol1_coords);
  Py_XDECREF(mol2_coords);
  return res;
}

extern "C" {
  PyObject*
  rmsd(PyObject* self, PyObject* args) {
    double U[4][4];
    int len;
    double res = rmsd_common(self, args, U, len);
    if(res < 0.0) return NULL;
    return Py_BuildValue("d", res);
  }

  PyObject*
  rmsd2(PyObject* self, PyObject* args) {
    double U[4][4];
    int len;
    double res = rmsd_common(self, args, U, len);
    if(res < 0.0) return NULL;
    PyObject* py_U = PyTuple_New(4);
    for(int i = 0; i < 4; ++i) {
      PyTuple_SetItem(py_U, i, Py_BuildValue("(dddd)", U[i][0], U[i][1], U[i][2], U[i][3]));
    }
    return Py_BuildValue("(dN)", res, py_U);
  }


  static PyMethodDef _rmsdMethods[] = {
    {"rmsd", rmsd, METH_VARARGS,
      "Caculate the RMSD of two mol"},
    {"rmsd2", rmsd2, METH_VARARGS,
      "Caculate the RMSD of two mol, return a tuple of the rmsd and the transformation matrix"},
    {NULL, NULL, 0, NULL} };

  PyMODINIT_FUNC
  init_rmsd(void)
  {
    (void) Py_InitModule("_rmsd", _rmsdMethods);
  }
}
