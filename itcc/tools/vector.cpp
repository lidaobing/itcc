// $Id$
#include "vector.hpp"
#include <boost/python.hpp>
#include <boost/python/overloads.hpp>
using namespace boost::python;

BOOST_PYTHON_MEMBER_FUNCTION_OVERLOADS(Vector_normal_overloads, normal, 0, 1)

BOOST_PYTHON_MODULE(Vector)
{
  class_<Vector>("Vector", init<optional<double, double, double> >())
    .def(init<const Vector &>())
    .def_readwrite("x", &Vector::x)
    .def_readwrite("y", &Vector::y)
    .def_readwrite("z", &Vector::z)
    .def(self + self)
    .def(self - self)
    .def(-self)
    .def(self += self)
    .def(self -= self)
    .def(self / double())
    .def(self *= double())
    .def(self /= double())
    .def("length", &Vector::length)
    //.def("normal", &Vector::normal, Vector_normal_overloads())
    .def("cross", &Vector::cross)
    .def(self * double())
    .def(double() * self)
    //.def(str(self))
    ;
}
