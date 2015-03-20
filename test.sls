vlan_test:
  arista_vlan:
    - present
    - host: veos1
    - vlanid: 2
    - name: johan-test
    - status: active
