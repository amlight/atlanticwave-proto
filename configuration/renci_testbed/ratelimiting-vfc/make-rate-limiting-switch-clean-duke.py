import requests
import time

# Disable warnings
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

token = "c73ad6e29773582187c06a1558f8ecc71ea273b3a5ae9e4f03f153d73f6436a619f3c8471205c28e25f9ae62741d5435e54c8a6f33f2b333154430448dd18215"
verify = False
bridge_name = "br20"
port1 = "21"
port2 = "22"
url = "https://192.168.202.30/"


# Make switch, vpws profile
response = requests.post(url+"api/v1/bridges",
                         {'bridge':bridge_name,
                          'subtype':'vpws',
                          'resources':1},
                         headers={'Authorization': token},
                         verify=verify)

bridge = response.json()['links'][bridge_name]
response = requests.get(bridge['href'], 
                       headers={'Authorization': token},
                       verify=verify)
bridge_links = response.json()['links']
bridge_tunnels = bridge_links['tunnels']



# Connect a controller
response = requests.post(bridge_links['controllers']['href'],
                        {'controller':'Eline',
                         'ip':'172.17.2.1',
                         'port':6653},
                        headers={'Authorization': token},
                        verify=verify)
                        

# Set port to c-tag
response = requests.patch(url+"api/v1/ports/"+port1,
                         json=[{'op':'replace',
                                'path':'/tunnel-mode',
                                'value':'ctag'}],
                         headers={'Authorization': token},
                         verify=verify)
response = requests.patch(url+"api/v1/ports/"+port2,
                         json=[{'op':'replace',
                                'path':'/tunnel-mode',
                                'value':'ctag'}],
                         headers={'Authorization': token},
                         verify=verify)

#print response
#print response.json()
#exit()



# Create tunnels and connect each of them.
vlanmin = 1
vlanmax = 98
for vlan in range(vlanmin,vlanmax):
    begin_time = time.time()
    # Tunnel on port1
#    response = requests.post(bridge_tunnels['href'],
#                             {'ofport':vlan, 'physical-port':port1,
#                              'vlan-id':vlan},
#                             headers={'Authorization': token},
#                             verify=verify)                             

    # Tunnel on port2
#    response = requests.post(bridge_tunnels['href'],
#                             {'ofport':vlan+vlanmax, 'physical-port':port2,
#                              'vlan-id':vlan},
#                             headers={'Authorization': token},
#                             verify=verify)                             

    # Create e-line between ports 1 and 2.
    response = requests.post(url+"app/eline/v1/connections",
                             {'connection':str(vlan)+"to"+str(vlan),
                              'ports':[port1+":"+str(vlan),
                                       port2+":"+str(vlan)]},
                             headers={'Authorization': token},
                             verify=verify)
    end_time = time.time()
    #print "%3d : %s" % (vlan, end_time - begin_time)
#    print response
#    print response.json()
