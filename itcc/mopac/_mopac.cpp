// $Id$

#include <mopac7/libmopac7.h>
#include <boost/python.hpp>

using namespace boost::python;


extern "C" void lm7start_(void);
extern "C" void lm7stop_(void);
extern "C" int lm7iniplt_(void);

extern "C" int getesp_(void);
extern "C" int geteldens_(void);
extern "C" int getorb_(void);

/* the rest are from libmopac7.c :
   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ */
extern "C" void lm7_ini_full_xyz(void);

extern "C" int lm7_get_atom_count(void);
extern "C" int lm7_get_electron_count(void);

extern "C" void lm7_set_atom_crd(int, double *);		/* unit is nm */

extern "C" void lm7_call_compfg(double *, double *, int);
extern "C" void lm7_get_atom_grad(int, double *);		/* unit is kJ/mol nm^2 ??? */

extern "C" int lm7_get_orbital_count(void);
extern "C" void lm7_set_plots_orbital_index(int);
extern "C" double lm7_get_orbital_energy(int);			/* unit is ??? */

extern "C" void lm7_set_num_potesp(int);
extern "C" void lm7_set_crd_potesp(int, double *);
extern "C" double lm7_get_val_potesp(int);

BOOST_PYTHON_MODULE(_mopac) {
  def("lm7start", lm7start_);
  def("lm7stop", lm7stop_);
  def("lm7iniplt", lm7iniplt_);
  def("getesp", getesp_);
  def("geteldens", geteldens_);
  def("getorb", getorb_);
  def("lm7_ini_full_xyz", lm7_ini_full_xyz);
  def("lm7_get_atom_count", lm7_get_atom_count);
  def("lm7_get_electron_count", lm7_get_electron_count);
  def("lm7_set_atom_crd", lm7_set_atom_crd);
  def("lm7_call_compfg", lm7_call_compfg);
  def("lm7_get_atom_grad", lm7_get_atom_grad);
  def("lm7_get_orbital_count", lm7_get_orbital_count);
  def("lm7_set_plots_orbital_index", lm7_set_plots_orbital_index);
  def("lm7_get_orbital_energy", lm7_get_orbital_energy);
  def("lm7_set_num_potesp", lm7_set_num_potesp);
  def("lm7_set_crd_potesp", lm7_set_crd_potesp);
  def("lm7_get_val_potesp", lm7_get_val_potesp);
}
