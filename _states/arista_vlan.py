# -*- coding: utf-8 -*-
'''
Configuration of Arista Vlans
'''

def present(vlanid, 
            host, 
            name, 
            status='active'):

    ret = {'changes': {},
           'comment': '',
           'name': name,
           'result': True}

    vlan = __salt__['arista_vlan.get'](vlanid)
    if not vlan:
        __salt__['arista_vlan.create'](vlanid)
        __salt__['arista_vlan.set_name'](vlanid,name)
        __salt__['arista_vlan.set_state'](vlanid,status)
        ret['comment'] = 'Vlan {0} ID {1} added to {2}'.format(name,vlanid,host)
        ret['changes'] = {host: {'id': vlanid, 'name': name, 'state': status}}
    else:
        if vlan['name'] != name:
            __salt__['arista_vlan.set_name'](vlanid,name)
            ret['comment'] += 'Changed name of vlan {0} to {1} on {2}'.format(vlanid,name,host)
            ret['changes'][host] = { 'id': vlanid }
        if vlan['state'] != status:
            __salt__['arista_vlan.set_state'](vlanid,status)
            ret['comment'] += 'Changed state of vlan {0} to {1} on {2}'.format(vlanid,status,host)
            ret['changes'][host] = { 'state': status}
        if ret['comment'] == '':
            ret['comment'] = 'Vlan {0} configured correctly on {1}'.format(vlanid,host)

    return ret
