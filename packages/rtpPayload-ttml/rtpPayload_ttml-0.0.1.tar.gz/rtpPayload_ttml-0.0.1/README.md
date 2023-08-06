# rtpPayload_ttml

This python library provides a means to decode, encode, and interact with TTML RTP payloads as defined in [RFC 8759](https://datatracker.ietf.org/doc/rfc8759/). It is designed for use with an RTP library such as [RTP](https://github.com/bbc/rd-apmm-python-lib-rtp). It only encodes/decodes the payload bitstreams. It DOES NOT provide a means to render or edit TTML documents. It also doesn't provide any network functionality. To send these payloads over UDP, check out [rtpTTML](https://github.com/bbc/rd-apmm-python-lib-rtpTTML).

## Installation

```bash
pip install rtpPayload-ttml
```

## Example usage
```python
from rtp import RTP, PayloadType, Extension
from rtpPayload_ttml import RTPPayload_TTML
from copy import deepcopy

baseRTP = RTP(
    marker=True,
    payloadType=PayloadType.DYNAMIC_96,
    extension=Extension(
        startBits=getExtStartBits(),
        headerExtension=getExtBody()
        ),
    csrcList=getCSRCList()
)
thisRTPBitstream = baseRTP.toBytearray()

while runing:
    nextRTP = deepcopy(baseRTP)
    nextRTP.sequenceNumber += 1
    nextRTP.timestamp = getNextTimestamp()
    nextRTP.payload = RTPPayload_TTML(userDataWords=getNextDoc())

    transmit(nextRTP)
```

```python
from rtp import RTP
from rtpPayload_ttml import RTPPayload_TTML

decodedPayload = RTPPayload_TTML.fromBytearray(
    RTP().fromBytearray(getNextPacket()).payload)
document = decodedPayload.userDataWords

render(document)
```

## Contributing
We desire that contributors of pull requests have signed, and submitted via email, a [Contributor Licence Agreement (CLA)](http://www.bbc.co.uk/opensource/cla/rfc-8759-cla.docx), which is based on the Apache CLA.

The purpose of this agreement is to clearly define the terms under which intellectual property has been contributed to the BBC and thereby allow us to defend the project should there be a legal dispute regarding the software at some future time.

If you haven't signed and emailed the agreement yet then the project owners will contact you using the contact info with the pull request.

## License 
See [LICENSE](LICENSE).