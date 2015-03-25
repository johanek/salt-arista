vlan_test:
  arista_vlan:
    - present
    - host: veos1
    - vlanid: 2
    - name: johan-test
    - status: active
  arista_interface:
    - managed
    - host: veos1
    - name: Ethernet1
    - description: ethernet
    - shutdown: False
