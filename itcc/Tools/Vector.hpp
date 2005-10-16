// $Id$
#include <cmath>
#include <exception>
#include <ostream>

class Vector{
public:
  double x;
  double y;
  double z;
public:
  Vector(double _x = 0.0,
	 double _y = 0.0,
	 double _z = 0.0);
  Vector(const Vector & rhs);
  Vector & operator=(const Vector & rhs);
  virtual ~Vector();

  Vector operator+(const Vector & rhs) const;
  Vector operator-(const Vector & rhs) const;
  Vector operator-() const;
  Vector & operator+=(const Vector & rhs);
  Vector & operator-=(const Vector & rhs);

  Vector operator/(double scale) const;
  Vector & operator*=(double scale);
  Vector & operator/=(double scale);

  double length() const;
  Vector & normal(double scale = 1.0);
  Vector cross(const Vector & rhs) const;
};

Vector operator*(const Vector & lhs, double rhs);
Vector operator*(double lhs, const Vector & rhs);

std::ostream& operator<<(std::ostream& os, const Vector & v);

// ctor, dtor
inline
Vector::Vector(double _x, double _y, double _z):
  x(_x), y(_y), z(_z)
{
}

inline
Vector::Vector(const Vector & rhs):
  x(rhs.x), y(rhs.y), z(rhs.z)
{
}

inline Vector &
Vector::operator=(const Vector & rhs){
  if(this == &rhs){
    return *this;
  }
  x = rhs.x;
  y = rhs.y;
  z = rhs.z;
  return *this;
}

inline
Vector::~Vector()
{
}

// `add' and `sub'
inline Vector
Vector::operator+(const Vector & rhs) const
{
  return Vector(x+rhs.x, y+rhs.y, z+rhs.z);
}

inline Vector
Vector::operator-(const Vector & rhs) const
{
  return Vector(x-rhs.x, y-rhs.y, z-rhs.z);
}

inline Vector
Vector::operator-() const
{
  return Vector(-x, -y, -z);
}

inline Vector &
Vector::operator+=(const Vector & rhs)
{
  x += rhs.x;
  y += rhs.y;
  z += rhs.z;
  return *this;
}

inline Vector &
Vector::operator-=(const Vector & rhs)
{
  x -= rhs.x;
  y -= rhs.y;
  z -= rhs.z;
  return *this;
}

// `mul' and `div'
inline Vector
Vector::operator/(double scale) const
{
  return Vector(x/scale, y/scale, z/scale);
}

inline Vector
operator*(const Vector & lhs, double scale)
{
  return Vector(lhs.x*scale, lhs.y*scale, lhs.z*scale);
}

inline Vector
operator*(double lhs, const Vector & rhs){
  return rhs * lhs;
}

inline Vector &
Vector::operator*=(double scale)
{
  x *= scale;
  y *= scale;
  z *= scale;
  return *this;
}



inline Vector &
Vector::operator/=(double scale)
{
  x /= scale;
  y /= scale;
  z /= scale;
  return *this;
}

// length, normal, cross
inline double
Vector::length() const
{
  return std::sqrt(x*x + y*y + z*z);
}

inline Vector &
Vector::normal(double scale)
{
  double len = length();
  if(len == 0.0){
    throw std::exception();
  }
  scale /= len;
  (*this) *= scale;
  return *this;
}

inline Vector
Vector::cross(const Vector & rhs) const
{
  return Vector(y * rhs.z - z * rhs.y,
		z * rhs.x - x * rhs.z,
		x * rhs.y - y * rhs.x);
}

// stream
std::ostream&
operator<<(std::ostream& os, const Vector & v)
{
  os << '(' << v.x << ", " << v.y << ", " << v.z << ')';
  return os;
}

