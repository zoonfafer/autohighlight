from __future__ import unicode_literals
from __future__ import absolute_import
import sys
if sys.version_info[0] < 3:
    from cStringIO import StringIO
else:
    from .io import StringIO
