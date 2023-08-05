"""
Validation functions that are useful in more than one packet type,
but not every packet type.
"""

from .base import PacketInvalidData


def _validate_resource_list(pkt):
    """
    ResourceLists must only have one element in them.
    A bit weird, yes, but that's the spec.
    """
    rlist = pkt._required_data.get('ResourceList')
    if rlist is not None:
        if not isinstance(rlist, list):
            raise PacketInvalidData("ResourceList must be a list")
        if len(rlist) != 1:
            raise PacketInvalidData("ResourceList must have exactly one element")

    return True
