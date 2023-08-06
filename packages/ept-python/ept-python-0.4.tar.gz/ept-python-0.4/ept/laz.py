

import laspy

from laspy import file


class LAZ(object):

    def __init__(self, bytes):
        d = laspy.file.File(None)
        self.bytes = _bytes
