# Copyright PA Knowledge Ltd 2021

from . import sisl_decoder
from . import sisl_encoder
from . import sisl_splitter
from . import sisl_joiner
from . import sisl_wrapper


def loads(sisl, schema=None):
    return sisl_decoder.SislDecoder().loads(sisl, schema)


def dumps(dict_to_encode, **kwargs):
    if kwargs.get('max_length'):
        return sisl_splitter.SplitSisl(kwargs.get('max_length')).split_sisl(dict_to_encode)
    else:
        return sisl_encoder.SislEncoder.dumps(dict_to_encode)


def wraps(data):
    return sisl_wrapper.SislWrapper().wraps(data)


def unwraps(data):
    return sisl_wrapper.SislWrapper().unwraps(data)
