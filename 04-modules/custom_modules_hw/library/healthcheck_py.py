#!/usr/bin/python3
# -*- coding: utf-8 -*-

import requests
from ansible.module_utils.basic import AnsibleModule

DOCUMENTATION = r'''
---
module: healthcheck
author: Pupkin V.
short_description: healthcheck of site
description:
  - healthcheck of site with or without TLS
version_added: 1.0.0
requirements:
  - requests
  - python >= 3.6
options:
  addr:
    description:
      - Address of site we want to check
      - This is a required parameter
    type: str
  tls:
    description:
      - Whether site using certificates or not
      - Default value is 'True'
    type: bool
'''

EXAMPLES = r'''
- name: Check availability of site
  healthcheck:
    addr: mysite.example
  connection: local

- name: Check availability of site without certs
  healthcheck:
    addr: mysite.example
    tls: false
  connection: local
'''

RETURN = r'''
msg:
  description: Errors if occured
  returned: always
  type: str
  sample: ""
site_status:
  description: State status
  returned: always
  type: str
  sample: Available
rc:
  description: Return code
  returned: always
  type: int
  sample: 200
'''


def healthcheck(addr, tls):
    failed = False
    site_status = ""
    msg = "Success"
    rc = 0

    protocol = "https" if tls else "http"
    url = protocol + "://" + addr

    try:
        response = requests.head(url)
        site_status = response.reason
        rc = response.status_code
    except requests.ConnectionError as e:
        failed = True
        msg = "ConnectionError. Can't connect to %s" % url
        rc = 1

    return (failed, site_status, rc, msg)


def main():
    # Аргументы для модуля
    arguments = dict(
        addr=dict(required=True, type='str'),
        tls=dict(type='bool', default="True")
    )
    # Создаем объект - модуль
    module = AnsibleModule(
        argument_spec=arguments,
        supports_check_mode=False
    )
    # Получаем аргументы
    addr = module.params["addr"]
    tls = module.params["tls"]

    lc_return = healthcheck(addr, tls)

    if lc_return[0]:
        module.fail_json(changed=False,
                         failed=lc_return[0],
                         site_status=lc_return[1],
                         rc=lc_return[2],
                         msg=lc_return[3])
    else:
        module.exit_json(changed=False,
                         failed=lc_return[0],
                         site_status=lc_return[1],
                         rc=lc_return[2],
                         msg=lc_return[3])


if __name__ == "__main__":
    main()
