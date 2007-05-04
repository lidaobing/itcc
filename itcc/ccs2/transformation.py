import numpy

class RotationTranslation:

    """Combined translational and rotational transformation.

    This is a subclass of Transformation.

    Objects of this class are not created directly, but can be the
    result of a composition of rotations and translations.
    """

    def __init__(self, tensor, vector):
	self.tensor = tensor.copy()
	self.vector = vector.copy()

    is_rotation_translation = 1

    def __mul__(self, other):
	if hasattr(other, 'is_rotation'):
	    return RotationTranslation(numpy.dot(self.tensor, other.tensor),
				       self.vector)
	elif hasattr(other, 'is_translation'):
	    return RotationTranslation(self.tensor,
				       numpy.dot(self.tensor, other.vector)+self.vector)
	elif hasattr(other, 'is_rotation_translation'):
	    return RotationTranslation(numpy.dot(self.tensor, other.tensor),
				       numpy.dot(self.tensor, other.vector)+self.vector)
	else:
	    raise ValueError, 'incompatible object'

    def __call__(self, vector):
	return numpy.dot(self.tensor, vector) + self.vector

    def inverse(self):

        return RotationTranslation(numpy.transpose(self.tensor),
                                   numpy.dot(numpy.transpose(self.tensor),
                                             -self.vector))
