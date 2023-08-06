'''
Created on Apr 26, 2019

@author: baumannt
'''

from drever.base_class import Drever
from drever.data_handlers.stream import StreamData


class StreamFilter(Drever):
    '''
    classdocs
    '''

    CLASS_CONFIG = {
        "INPUT_VECTOR_TYPE":  (StreamData, ),
        "OUTPUT_VECTOR_TYPE": (StreamData, )
    }

    # Overwrite this dictionary with your default Drever algorithm parameters.
    DEFAULT_PARAMS = {}

    def run(self):
        self._set_output_data(self.get_input_data())

    @classmethod
    def dump_vectors(cls, path, vectors):
        vectors.save(path, False)
