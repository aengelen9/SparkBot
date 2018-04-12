import dnac
import json

cookie = dnac.login()
hosts = dnac.get_hosts(cookie)
macAddr = ['c8:4c:75:68:b2:c1']

host = dnac.getHost(cookie, macAddr)
switch = dnac.get_nw_device_by_id(cookie, '6d3eaa5d-bb39-4cc4-8881-4a2b2668d2dc')
lineCard = dnac.getModule(cookie, 'feb42c9f-323f-4e17-87d3-c2ea924320cb')
macAddr2 = ['c8', '4c', '75', '68', 'b2', 'c0']

makeitastring = ':'.join(map(str, macAddr2))


pretty = json.dumps(host, indent=4, sort_keys=True)

print (pretty)
#print (makeitastring)
