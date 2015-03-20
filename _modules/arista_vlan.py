# -*- coding: utf-8 -*-
'''
Module for managing arista vlans
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
    vlans = _vlans()
    return vlans.getall()

def get(vlanid):
    vlans = _vlans()
    result = vlans.get(vlanid)
    if result == None:
        return False
    return result

def create(vlanid):
    vlans = _vlans()
    if vlans.get(vlanid):
        return "Error: vlan %s already exists" % vlanid
    result = vlans.create(vlanid)
    if result == None:
        return "Error: could not create vlan %s" % vlanid
    return result

def set_name(vlanid,name):
    vlans = _vlans()
    result = vlans.set_name(vlanid,name)
    if result == None:
        return "Error: could not set name for vlan %s" % vlanid
    return result

def delete(vlanid):
    vlans = _vlans()
    if not vlans.get(vlanid):
        return "Error: vlan %s doesn't exist" % vlanid
    result = vlans.delete(vlanid)
    if result == None:
        return "Error: could not delete vlan %s" % vlanid
    return result

def set_name(vlanid,name):
    vlans = _vlans()
    vlan = vlans.get(vlanid)
    if vlan == None:
        vlan = "Error: vlan %s does not exist" % vlanid
    result = vlans.set_name(vlanid,name)
    if result == None:
        result = "Error: Could not set name for vlan %s" % vlanid
    return result

def set_state(vlanid,state):
    vlans = _vlans()
    if state not in ['active','suspend']:
        return "Error: %s is not a valid state for vlan" % state
    vlan = vlans.get(vlanid)
    if vlan == None:
        return "Error: vlan %s does not exist" % vlanid
    result = vlans.set_state(vlanid, value=state)
    if result == False:
        result = "Error: could not set state %s for vlan %s" % (vlanid, state)
    return result

def _conn():
    node = pyeapi.connect_to('veos1')
    return node

def _vlans():
    node = _conn()
    vlans = node.api('vlans')
    vlans.autotrfresh = True
    return vlans
