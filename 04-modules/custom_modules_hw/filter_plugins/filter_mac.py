#!/usr/bin/python

import re
from ansible.errors import (
    AnsibleFilterTypeError
)


def mac(val):
    if not isinstance(val, str):
        raise AnsibleFilterTypeError("TypeError. Input value must be a sting")

    if re.search('^[\da-f]{12}$', val, re.IGNORECASE) == None:
        raise AnsibleFilterTypeError(
            "TypeError. Input value has a wrong format")

    return re.sub("([\da-f]{2})\B", "\\1:", val, 0, re.IGNORECASE)


class FilterModule(object):
    def filters(self):
        return {
            'mac': mac
        }
