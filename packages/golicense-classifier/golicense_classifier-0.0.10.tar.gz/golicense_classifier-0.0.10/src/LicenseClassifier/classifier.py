import ctypes
from os.path import dirname, exists, join
import json

from LicenseClassifier.error import *


class LicenseClassifier:
    _ROOT = dirname(__file__)

    # Shared Library
    _so = ctypes.cdll.LoadLibrary(join(_ROOT, "compiled/libmatch.so"))
    _match = _so.FindMatch
    _match.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int]
    _match.restype = ctypes.c_bool

    _scanfile = _so.ScanFile
    _scanfile.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
    _scanfile.restype = ctypes.c_char_p

    _setThresh = _so.SetThreshold
    _setThresh.argtypes = [ctypes.c_int]
    _setThresh.restype = ctypes.c_bool

    def __init__(self):
        pass

    def analyze(self, root, output="result.json", maxRoutines=10):
        """Function to find a license match for all files present in `root`"""
        if not exists(root):
            raise FileNotFoundError

        if maxRoutines < 0:
            raise InvalidParameter

        if output == "":
            output = "result.json"

        res = self._match(
            join(LicenseClassifier._ROOT, "classifier/default/").encode("utf-8"),
            root.encode("utf-8"),
            output.encode("utf-8"),
            maxRoutines,
        )
        return res

    def scanFile(self, root):
        if not exists(root):
            raise FileNotFoundError

        jsonRes = self._scanfile(
                join(LicenseClassifier._ROOT, "classifier/default/").encode("utf-8"),
                root.encode("utf-8"),
            ).decode('utf-8')

        # Error-Checking
        if jsonRes[:5] == "Error":
            raise ValueError(jsonRes[7:])

        return json.loads(jsonRes)

    def setThreshold(self, thresh):
        """Set a threshold between `0 - 100`. Default is `80`. Speed Degrades with lower threshold"""
        _ = self._setThresh(thresh)
