#!/usr/bin/python
#
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

from unittest import TestCase
from hypothesis import given, strategies as st  # type: ignore
from rtpPayload_ttml import (RTPPayload_TTML, LengthError, SUPPORTED_ENCODINGS,
                             utfEncode)


class TestExtension (TestCase):
    def setUp(self):
        self.thisP = RTPPayload_TTML()

    @given(st.tuples(
        st.text(),
        st.sampled_from(SUPPORTED_ENCODINGS),
        st.booleans()).filter(
            lambda x: len(utfEncode(x[0], x[1], x[2])) < 2**16))
    def test_init(self, data):
        doc, encoding, bom = data
        reservedBits = bytearray(b'\x00\x00')
        newP = RTPPayload_TTML(reservedBits, doc, encoding, bom)

        self.assertEqual(newP.reserved, reservedBits)
        self.assertEqual(newP.userDataWords, doc)
        self.assertEqual(newP._encoding, encoding)
        self.assertEqual(newP._bom, bom)

    @given(
        st.text(),
        st.text().filter(lambda x: x not in SUPPORTED_ENCODINGS),
        st.booleans())
    def test_init_invalidEnc(self, doc, enc, bom):
        reservedBits = bytearray(b'\x00\x00')

        with self.assertRaises(AttributeError):
            RTPPayload_TTML(reservedBits, doc, enc, bom)

    def test_reserved_default(self):
        self.assertEqual(self.thisP.reserved, bytearray(b'\x00\x00'))

    def test_reserved_notBytes(self):
        with self.assertRaises(AttributeError):
            self.thisP.reserved = ""

    @given(st.binary().filter(lambda x: x != bytearray(b'\x00\x00')))
    def test_reserved_invalid(self, value):
        with self.assertRaises(ValueError):
            self.thisP.reserved = bytearray(value)

    def test_userDataWords_default(self):
        self.assertEqual(self.thisP.userDataWords, "")

    @given(st.text().filter(lambda x: len(utfEncode(x, "UTF-8")) < 2**16))
    def test_userDataWords(self, doc):
        self.thisP.userDataWords = doc
        self.assertEqual(self.thisP.userDataWords, doc)

    def test_userDataWords_invalidType(self):
        with self.assertRaises(AttributeError):
            self.thisP.userDataWords = 0

    def test_userDataWords_tooLong(self):
        doc = ""
        for x in range(2**16):
            doc += "a"
        with self.assertRaises(LengthError):
            self.thisP.userDataWords = doc

    @given(st.tuples(
        st.text(),
        st.sampled_from(SUPPORTED_ENCODINGS),
        st.booleans()).filter(
            lambda x: len(utfEncode(x[0], x[1], x[2])) < 2**16))
    def test_userDataWords_encodings(self, data):
        doc, encoding, bom = data
        payload = RTPPayload_TTML(
            userDataWords=doc, encoding=encoding, bom=bom)
        self.assertEqual(payload.userDataWords, doc)
        self.assertEqual(payload._userDataWords, utfEncode(doc, encoding, bom))

    def test_eq(self):
        reservedBits = bytearray(b'\x00\x00')
        newP = RTPPayload_TTML(reservedBits, "")

        self.assertEqual(newP, self.thisP)

    def test_bytearray_default(self):
        expected = bytearray(4)
        self.assertEqual(bytes(self.thisP), expected)

        newP = RTPPayload_TTML().fromBytearray(expected)
        self.assertEqual(newP, self.thisP)

    @given(st.binary(min_size=2, max_size=2).filter(
        lambda x: x != b'\x00\x00'))
    def test_fromBytearray_invalidLen(self, length):
        bArray = bytearray(4)
        bArray[2:4] = length

        with self.assertRaises(LengthError):
            RTPPayload_TTML().fromBytearray(bArray)

    @given(st.text())
    def test_toBytearray(self, doc):
        self.thisP.userDataWords = doc

        bDoc = utfEncode(doc)
        expected = bytearray(2)
        expected += int(len(bDoc)).to_bytes(2, byteorder='big')
        expected += bDoc

        self.assertEqual(expected, self.thisP.toBytearray())

    @given(st.text())
    def test_fromBytearray(self, doc):
        expected = RTPPayload_TTML(userDataWords=doc)

        bDoc = utfEncode(doc)
        bArray = bytearray(2)
        bArray += int(len(bDoc)).to_bytes(2, byteorder='big')
        bArray += bDoc

        self.thisP.fromBytearray(bArray)

        self.assertEqual(expected, self.thisP)
