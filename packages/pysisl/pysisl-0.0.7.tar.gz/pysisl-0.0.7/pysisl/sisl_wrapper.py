# Copyright PA Knowledge Ltd 2021
import construct
from itertools import cycle
import secrets
from pysisl import parser_error
import pysisl
from binascii import unhexlify


class SislWrapper:
    def __init__(self, key_generator=None):
        self.majorVersion = 1
        self.minorVersion = 0
        self.headerLen = 48
        self.encapsulationType = 1
        self.encapsulationConfig = 3
        self.encapsulationDataLen = 8
        self.key = SislWrapper.key_generation() if key_generator is None else key_generator
        self.padding = 0
        self.cloaked_dagger = self._build_cloaked_dagger_header()

    def wraps(self, data):
        return self.cloaked_dagger + SislWrapper._xor_data(self.key, bytes(data, 'utf-8'))

    @staticmethod
    def _xor_data(key, data):
        return bytes([a ^ b for (a, b) in zip(data, cycle(key))])

    @staticmethod
    def unwraps(data):
        key = SislWrapper._extract_key_from_cloaked_dagger_header(data)
        return SislWrapper._xor_data(key, SislWrapper._extract_payload_from_data(data))

    def _build_cloaked_dagger_header(self):
        return CloakDagger.cloak_dagger_bytes().build(
            dict(Major_Version=self.majorVersion,
                 Minor_Version=self.minorVersion,
                 Length=self.headerLen,
                 Encap_Type=self.encapsulationType,
                 Encap_Config=self.encapsulationConfig,
                 Encap_Dlen=self.encapsulationDataLen,
                 Encap_Mask=self.key,
                 Padding=self.padding))

    @staticmethod
    def key_generation():
        key = unhexlify(secrets.token_hex(8))
        if b'\x00' in key:
            key = SislWrapper.key_generation()
        return key

    @staticmethod
    def _extract_key_from_cloaked_dagger_header(data):
        return data[20:28]

    @staticmethod
    def _extract_payload_from_data(data):
        return data[48:]


class CloakDagger:
    @staticmethod
    def cloak_dagger_bytes():
        return construct.Struct("Magic_Number_1" / construct.Const(b'\xd1\xdf\x5f\xff'),
                                "Major_Version" / construct.Int16ub,
                                "Minor_Version" / construct.Int16ub,
                                "Length" / construct.Int32ub,
                                "Encap_Type" / construct.Int32ub,
                                "Encap_Config" / construct.Int16ub,
                                "Encap_Dlen" / construct.Int16ub,
                                "Encap_Mask" / construct.Bytes(8),
                                "RESERVED" / construct.Padding(16),
                                "Magic_Number_2" / construct.Const(b'\xff\x5f\xdf\xd1')
                                )
