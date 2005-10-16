// $Id$

#include <Python.h>
#include <cmath>
#include <cassert>

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
 *      coor         : atom coordinates of the fitted structure (fit 2 to 1)    *
 *      flag         : flag for indicate selected atoms to alignment            *
 *      return value : RMSD                                                     *
*********************************************************************************/

double _rmsd(int n, double coor1[][3], double coor2[][3], double coor[][3], int flag[])
{
  int i, j, k, N=3, lwork=9, ok;
	double r, R1[3][3], R[3][3], RT[9], w[3], work[9], A[3][3], B[3][3], U[3][3];
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
	for (i=0; i<3; i++)
		for (j=0; j<3; j++) {
			R1[i][j] = 0;
			for (k=0; k<n; k++)
				if ( flag[k] ) R1[i][j] += tmp1[k][i] * tmp2[k][j];
			r += R1[i][j] * R1[i][j];
		}

	r = sqrt(r/3);

	for (i=0; i<3; i++)
		for (j=0; j<3; j++)
			R1[i][j] /= r;

	for (i=0; i<3; i++)
		for (j=0; j<3; j++) {
			R[i][j] = 0;
			for (k=0; k<3; k++)
				R[i][j] += R1[k][i] * R1[k][j];
		}

	for (i=0; i<3; i++)
		for (j=0; j<3; j++)
			RT[j+3*i] = R[j][i];

	dsyev_ (&jobz, &uplo, &N, RT, &N, w, work, &lwork, &ok);

	for (i=0; i<3; i++)
		for (j=0; j<3; j++)
			A[i][j] = RT[3*i+j];
	
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
	
	for (i=0; i<n; i++)
		for (j=0; j<3; j++) {
			coor[i][j] = 0;
			for (k=0; k<3; k++)
				coor[i][j] += U[j][k] * tmp2[i][k];
			coor[i][j] += c1[j];
		}
	d = 0;
	for (i=0; i<n; i++)
		for (j=0; j<3; j++)
			d += (coor[i][j] - coor1[i][j]) * (coor[i][j] - coor1[i][j]);
	d = sqrt(d / (n - 1));
	return d;
}

extern "C" {

  static PyObject *
  rmsd(PyObject* self, PyObject* args)
  {
    PyObject* mol1, *mol2;
  
    if(!PyArg_ParseTuple(args, "OO", &mol1, &mol2))
      {
	return NULL;
      }
    assert(PyObject_HasAttrString(mol1, "coords"));
    assert(PyObject_HasAttrString(mol2, "coords"));
    PyObject* coords1 = PyObject_GetAttrString(mol1, "coords");
    PyObject* coords2 = PyObject_GetAttrString(mol2, "coords");
    assert(PySequence_Check(coords1));
    assert(PySequence_Check(coords2));
    int len = PySequence_Size(coords1);
    assert(PySequence_Size(coords2) == len);

    double (*coor1)[3] = new double[len][3];
    double (*coor2)[3] = new double[len][3];
    double (*coor)[3] = new double[len][3];
    int *flag = new int[len];
    for(int i = 0; i < len; ++i)
      {
	PyObject* vec1 = PySequence_GetItem(coords1, i);
	vec1 = PySequence_List(vec1);
	for(int j = 0; j < 3; ++j)
	  {
	    coor1[i][j] = PyFloat_AsDouble(PySequence_GetItem(vec1, j));
	  }

	PyObject* vec2 = PySequence_GetItem(coords2, i);
	vec2 = PySequence_List(vec2);
	for(int j = 0; j < 3; ++j)
	  {
	    coor2[i][j] = PyFloat_AsDouble(PySequence_GetItem(vec2, j));
	  }

	flag[i] = 1;
      }
    double result = _rmsd(len, coor1, coor2, coor, flag);
    delete []coor1;
    delete []coor2;
    delete []coor;
    delete []flag;
    return Py_BuildValue("d", result);
  }

  static PyMethodDef _rmsdMethods[] = {
    {"rmsd", rmsd, METH_VARARGS,
     "Caculate the RMSD of two mol"},
    {NULL, NULL, 0, NULL}       
  };

  PyMODINIT_FUNC
  init_rmsd(void)
  {
    (void) Py_InitModule("_rmsd", _rmsdMethods);
  }
}
