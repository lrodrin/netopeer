"""
This module implements a create call for ABNO parent 10.1.7.81

Copyright (c) 2017-2018 Laura Rodriguez Navas <laura.rodriguez.navas@cttc.cat>
"""
import requests
import simplejson as json

opt_post = "POST"
opt_delete = "DELETE"


def create_call(ip, id_call, id_interface, src, dst, eth_src, eth_dst, opt):
    url = "http://%s:9881/restconf/config/calls/call/%s" % (ip, id_call)
    data = {
        "aEnd": {
            "edgeEndId": id_interface,
            "endpointId": src + "_" + id_interface,
            "nodeId": src
        },
        "callId": id_call,
        "contextId": "test",
        "match": {
            "ethSrc": eth_src,
            "ethDst": eth_dst,
            "ipv4Src": "",
            "ipv4Dst": ""
        },
        "trafficParams": {
            "reservedBandwidth": "100000000"
        },
        "transportLayer": {
            "direction": "bidir",
            "layer": "ethernet"
        },
        "zEnd": {
            "edgeEndId": id_interface,
            "endpointId": dst + "_" + id_interface,
            "nodeId": dst
        }
    }
    headers = {'Content-type': 'application/json'}
    if opt == "POST":
        requests.post(url, data=json.dumps(data), headers=headers)

    elif opt == "DELETE":
        requests.delete(url, headers=headers)


if __name__ == '__main__':
    ip_abno = "10.1.7.81"
    id_call = "1"
    id_interface = "5"
    mac_src = "00:00:90:e2:ba:e2:b9:60"
    mac_dst = "00:00:90:e2:ba:cd:80:64"
    eth_src = "b2:2e:f7:fd:2a:85"
    eth_dst = "16:c3:35:7e:55:e2"

    create_call(ip_abno, id_call, id_interface, mac_src, mac_dst, eth_src, eth_dst, opt_post)
