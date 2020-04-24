from __future__ import unicode_literals
from __future__ import absolute_import
import sys
from future import standard_library
standard_library.install_aliases()
if sys.version_info[0] < 3:
    # from io import StringIO
    from cStringIO import StringIO
else:
    # from .io import StringIO
    from io import StringIO
