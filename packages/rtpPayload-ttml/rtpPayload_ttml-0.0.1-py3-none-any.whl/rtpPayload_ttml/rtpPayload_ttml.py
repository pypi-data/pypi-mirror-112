# James Sandford, copyright BBC 2020
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import annotations
from .utfUtils import SUPPORTED_ENCODINGS, utfEncode, utfDecode


class LengthError(Exception):
    '''
    Data is an invalid length.
    '''

    pass


class RTPPayload_TTML:
    '''
    A data structure for storing TTML RTP payloads as defined by RFC 8759.

    Attributes:
        reserved (bytearray): The reserved bits. MUST be set to ``0``.
        userDataWords (str): The TTML document.
        encoding (str): One of UTF-8, UTF-16, UTF-16LE, and UTF-16BE
        bom (bool): Should encoded documents start with a byte-order mark
    '''

    def __init__(
       self,
       reserved: bytearray = bytearray(b'\x00\x00'),
       userDataWords: str = "",
       encoding: str = "UTF-8",
       bom: bool = False) -> None:
        self._userDataWords: bytearray

        self.reserved = reserved
        self._bom = bom

        if encoding in SUPPORTED_ENCODINGS:
            self._encoding = encoding
        else:
            raise AttributeError("Encoding must be one of {}".format(
                "".join(SUPPORTED_ENCODINGS)))

        self.userDataWords = userDataWords

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, RTPPayload_TTML):
            return NotImplemented

        return (
            (type(self) == type(other)) and
            (self.reserved == other.reserved) and
            (self.userDataWords == other.userDataWords) and
            (self._encoding == other._encoding) and
            (self._bom == other._bom))

    @property
    def reserved(self) -> bytearray:
        return self._reserved

    @reserved.setter
    def reserved(self, p: bytearray) -> None:
        if type(p) != bytearray:
            raise AttributeError("Payload value must be bytearray")
        if p != bytearray(b'\x00\x00'):
            raise ValueError("Reserved bits must be '\x00\x00' under RFC 8759")
        else:
            self._reserved = p

    @property
    def userDataWords(self) -> str:
        return utfDecode(self._userDataWords, self._encoding)

    @userDataWords.setter
    def userDataWords(self, p: str) -> None:
        workingUDW = utfEncode(p, self._encoding, self._bom)

        if (len(workingUDW) >= 2**16):
            raise LengthError(
                "userDataWords must be fewer than 2**16 bytes")
        else:
            self._userDataWords = workingUDW

    def fromBytearray(self, packet: bytearray) -> RTPPayload_TTML:
        '''
        Populate instance from a bytearray.
        '''

        self.reserved = packet[0:2]
        length = int.from_bytes(packet[2:4], byteorder='big')
        self._userDataWords = packet[4:]
        if length != len(self._userDataWords):
            raise LengthError(
                "Length field does not match length of userDataWords")

        return self

    def toBytearray(self) -> bytearray:
        '''
        Encode instance as a bytearray.
        '''

        packetLen = 4 + len(self._userDataWords)

        packet = bytearray(packetLen)

        packet[0:2] = self.reserved
        packet[2:4] = len(self._userDataWords).to_bytes(2, byteorder='big')
        packet[4:] = self._userDataWords

        return packet

    def __bytes__(self) -> bytes:
        return bytes(self.toBytearray())
