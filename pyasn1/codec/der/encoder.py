#
# This file is part of pyasn1 software.
#
# Copyright (c) 2005-2017, Ilya Etingof <etingof@gmail.com>
# License: http://pyasn1.sf.net/license.html
#
from pyasn1.type import univ
from pyasn1.codec.cer import encoder

__all__ = ['encode']


class BitStringEncoder(encoder.BitStringEncoder):
    def encodeValue(self, value, encodeFun, **options):
        return encoder.BitStringEncoder.encodeValue(
            self, value, encodeFun, **options
        )

class OctetStringEncoder(encoder.OctetStringEncoder):
    def encodeValue(self, value, encodeFun, **options):
        return encoder.OctetStringEncoder.encodeValue(
            self, value, encodeFun, **options
        )

class SetOfEncoder(encoder.SetOfEncoder):
    @staticmethod
    def _sortComponents(components):
        # sort by tags depending on the actual Choice value (dynamic sort)
        return sorted(components, key=lambda x: isinstance(x, univ.Choice) and x.getComponent().tagSet or x.tagSet)

tagMap = encoder.tagMap.copy()
tagMap.update({
    univ.BitString.tagSet: BitStringEncoder(),
    univ.OctetString.tagSet: OctetStringEncoder(),
    # Set & SetOf have same tags
    univ.SetOf.tagSet: SetOfEncoder()
})

typeMap = encoder.typeMap.copy()
typeMap.update({
    univ.BitString.typeId: BitStringEncoder(),
    univ.OctetString.typeId: OctetStringEncoder(),
    # Set & SetOf have same tags
    univ.Set.typeId: SetOfEncoder(),
    univ.SetOf.typeId: SetOfEncoder()
})


class Encoder(encoder.Encoder):
    supportIndefLength = False

    def __call__(self, value, **options):
        if 'defMode' not in options:
            options.update(defMode=True)
        return encoder.Encoder.__call__(self, value, **options)

#: Turns ASN.1 object into DER octet stream.
#:
#: Takes any ASN.1 object (e.g. :py:class:`~pyasn1.type.base.PyAsn1Item` derivative)
#: walks all its components recursively and produces a DER octet stream.
#:
#: Parameters
#: ----------
#  value: any pyasn1 object (e.g. :py:class:`~pyasn1.type.base.PyAsn1Item` derivative)
#:     A pyasn1 object to encode
#:
#: defMode: :py:class:`bool`
#:     If `False`, produces indefinite length encoding
#:
#: maxChunkSize: :py:class:`int`
#:     Maximum chunk size in chunked encoding mode (0 denotes unlimited chunk size)
#:
#: Returns
#: -------
#: : :py:class:`bytes` (Python 3) or :py:class:`str` (Python 2)
#:     Given ASN.1 object encoded into BER octetstream
#:
#: Raises
#: ------
#: : :py:class:`pyasn1.error.PyAsn1Error`
#:     On encoding errors
encode = Encoder(tagMap, typeMap)
