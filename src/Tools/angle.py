# $Id$

from itcc.Tools.periodnumber import genPNclass

__revision__ = '$Rev$'
__all__ = ['Angle']

Angle = genPNclass(-180.0, 180.0)
Angle.__name__ = 'Angle'       
