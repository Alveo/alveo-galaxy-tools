from galaxy.datatypes.text import Text
from galaxy.datatypes.binary import Binary
from galaxy.datatypes.metadata import MetadataElement, ListParameter, DictParameter
from galaxy import util

import wave
import re

import logging
log = logging.getLogger(__name__)

class WAV( Binary ):
    """RIFF WAV audio file"""

    file_ext = "wav"
    blurb = "RIFF WAV Audio file"
    is_binary = True

    def get_mime(self):
        """Returns the mime type of the datatype"""
        return 'audio/wav'

    def sniff(self, filename):
        try:
            fp = wave.open(filename, 'rb')
            fp.close()
            return True
        except wave.Error:
            return False

Binary.register_sniffable_binary_format('wav', 'wav', WAV)

class TextGrid( Text ):
    """Praat Textgrid file for speech annotations"""

    file_ext = "TextGrid"
    header = 'File type = "ooTextFile"\nObject class = "TextGrid"'

    blurb = "Praat TextGrid file"

    MetadataElement( name="annotations", default=[], desc="Annotation types", param=ListParameter, readonly=True, visible=True, optional=True, no_value=[] )

    def sniff(self, filename):

        with open(filename, 'r') as fd:
            firstline = fd.readline()
            secondline = fd.readline()

            return firstline+secondline == self.header

        return False

class BPF( Text ):
    """Munich BPF annotation format
    https://www.phonetik.uni-muenchen.de/Bas/BasFormatseng.html#Partitur

>>> b = BPF()
>>> b.sniff('test-data/1_1119_2_22_001.par')
True
>>> class DT(object):
...     pass
...
>>> dt = DT()
>>> dt.file_name = 'test-data/1_1119_2_22_001.par'
>>> dt.metadata = DT()
>>> b.set_meta(dt)
>>> dt.metadata.annotations
['ORT', 'KAN']
    """

    file_ext = "par"

    MetadataElement( name="annotations", default=[], desc="Annotation types", param=ListParameter, readonly=True, visible=True, optional=True, no_value=[] )

    def set_meta( self, dataset, overwrite=True, **kwd ):
        """Set the metadata for this dataset from the file contents"""

        types = set()
        with open(dataset.dataset.file_name, 'r') as fd:
            for line in fd:
                match = re.match("([A-Z]+):\s", line)
                if match is None:
                    return False
                types.add(match.group(1))
        dataset.metadata.annotations = list(types)

    def sniff(self, filename):

        with open(filename, 'r') as fd:
            for line in fd:
                match = re.match("([A-Z]+):\s", line)
                return match is not None
        # in case the file is empty
        return False

def _test():
    import doctest
    doctest.testmod()

if __name__ == "__main__":
    _test()
