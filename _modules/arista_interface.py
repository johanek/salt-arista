# -*- coding: utf-8 -*-
'''
Module for managing arista interfaces
'''
from __future__ import absolute_import

# Import python libs
import logging
import os
import re

# Import salt libs
import salt.utils
import salt.utils.decorators as decorators

log = logging.getLogger(__name__)

try:
    import pyeapi
    HAS_PYEAPI = True
except ImportError:
    HAS_PYEAPI = False

def __virtual__():
    '''
    Only work on POSIX-like systems
    '''
    if salt.utils.is_windows() or HAS_PYEAPI == False:
        return False
    return True

def getall():
    interfaces = _interfaces()
    return interfaces.getall()

def get(interface):
    interfaces = _interfaces()
    result = interfaces.get(interface)
    if result == None:
        return False
    return result

def set_description(interface, description):
    interfaces = _interfaces()
    if not interfaces.get(interface):
        log.warn("Error: interface %s doesn't exist" % interface)
        return False
    result = interfaces.set_description(interface, description)
    if result == False:
        log.warn("Error: could not set description for interface %s" % interface)
    return result

def set_shutdown(interface, shutdown):
    interfaces = _interfaces()
    if shutdown not in [True, False, None]:
        log.warn("Error: %s is not a valid shutdown for interface" % shutdown)
        return False
    if not interfaces.get(interface):
        log.warn("Error: interface %s doesn't exist" % interface)
        return False
    result = interfaces.set_shutdown(interface, shutdown)
    if result == False:
        log.warn("Error: could not set state %s for vlan %s" % (vlanid, state))
    return result

def _conn():
    node = pyeapi.connect_to('veos1')
    return node

def _interfaces():
    node = _conn()
    interfaces = node.api('interfaces')
    return interfaces
