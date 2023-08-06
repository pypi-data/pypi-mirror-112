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
from rtpPayload_ttml import SUPPORTED_ENCODINGS, utfEncode, utfDecode
from rtpPayload_ttml.utfUtils import BOMS, ENCODING_ALIASES


class TestExtension (TestCase):
    @given(st.text())
    def test_encode_default(self, doc):
        ret = utfEncode(doc)

        self.assertEqual(ret, bytearray(doc, "utf_8"))

    @given(
        st.text(),
        st.sampled_from(SUPPORTED_ENCODINGS),
        st.booleans())
    def test_encode_encodings(self, doc, encoding, bom):
        ret = utfEncode(doc, encoding, bom)

        if bom:
            self.assertTrue(ret.startswith(BOMS[encoding]))
            ret = ret[len(BOMS[encoding]):]

        self.assertEqual(doc, ret.decode(ENCODING_ALIASES[encoding]))

    @given(
        st.text(),
        st.text().filter(lambda x: x not in SUPPORTED_ENCODINGS),
        st.booleans())
    def test_encode_invalid(self, doc, enc, bom):
        with self.assertRaises(AttributeError):
            utfEncode(doc, enc, bom)

    @given(st.tuples(
        st.text(),
        st.sampled_from(SUPPORTED_ENCODINGS),
        st.booleans()))
    def test_decode(self, data):
        doc, encoding, bom = data
        encoded = utfEncode(doc, encoding, bom)
        decoded = utfDecode(encoded, encoding)

        self.assertEqual(doc, decoded)

    @given(st.text())
    def test_decode_utf16(self, doc):
        # UTF-16 can decode both little and big endian
        for enc in ["UTF-16LE", "UTF-16BE"]:
            encoded = utfEncode(doc, enc, True)
            decoded = utfDecode(encoded, "UTF-16")

            self.assertEqual(doc, decoded)

    @given(st.text())
    def test_decode_wrongBom(self, doc):
        for enc, dec in [
           ("UTF-16LE", "UTF-16BE"),
           ("UTF-16LE", "UTF-8"),
           ("UTF-16BE", "UTF-16LE"),
           ("UTF-16BE", "UTF-8"),
           ("UTF-8", "UTF-16BE"),
           ("UTF-8", "UTF-16LE")
           ]:
            encoded = utfEncode(doc, enc, True)

            with self.assertRaises(ValueError):
                utfDecode(encoded, dec)

    @given(
        st.binary(),
        st.text().filter(lambda x: x not in SUPPORTED_ENCODINGS))
    def test_decode_invalid(self, doc, enc):
        with self.assertRaises(AttributeError):
            utfDecode(bytearray(doc), enc)
