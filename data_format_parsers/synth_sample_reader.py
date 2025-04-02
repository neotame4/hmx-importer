from . sample_data_reader import *
from .. common import *
from .. readers import *
from .. writers import *

def read_synth_sample(reader, name: str, self) -> None:
    version = reader.int32()
    if version > 1:
        read_metadata(reader, False)
    file = reader.numstring()
    if version < 6:
        looped = reader.milo_bool()
        loop_start_sample = reader.int32()
        if version > 2:
            loop_end_sample = reader.int32()
    read_sample_data(reader, name, self)