# -*- coding: utf-8 -*-
'''
Configuration of Arista interfaces
'''

def managed(name,
            host,
            description='',
            shutdown=False):

    ret = {'changes': {},
           'comment': '',
           'name': name,
           'result': True}

    interface = __salt__['arista_interface.get'](name)
    if not interface:
        ret['comment'] = 'interface {0} does not exist on {1}'.format(name,host)
        ret['result'] = False
    else:
        if interface['description'] != description:
            __salt__['arista_interface.set_description'](name,description)
            ret['comment'] += 'Changed description of interface {0} to {1} on {2}'.format(name,description,host)
            ret['changes'][host] = { 'description': description }
        if interface['shutdown'] != shutdown:
            __salt__['arista_interface.set_shutdown'](name,shutdown)
            ret['comment'] += 'Changed shutdown of interface {0} to {1} on {2}'.format(name,shutdown,host)
            ret['changes'][host] = { 'shutdown': shutdown }
        if ret['comment'] == '':
            ret['comment'] = 'interface {0} configured correctly on {1}'.format(name,host)

    return ret
