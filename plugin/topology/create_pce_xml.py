#!/usr/bin/python
# -*- coding: utf-8 -*-

# WARNING: WTF IS THIS!!

import socket

__author__ = 'amll'

#### WRITING TED FILE ###############
header_1 = \
    '''\t<local_ip_addrs>
\t\t<count>0</count>
\t\t<item_version>0</item_version>
\t</local_ip_addrs>
\t<remote_ip_addrs>
\t\t<count>0</count>
\t\t<item_version>0</item_version>
\t</remote_ip_addrs>
'''

header_2 = \
    '''\t<max_bw>0</max_bw>
\t<max_resv_bw>1.5625e+14</max_resv_bw>
\t<unresv_bw>
\t\t<count>8</count>
\t\t<item_version>0</item_version>
\t\t<item>1.5625e+14</item>
\t\t<item>1.5625e+14</item>
\t\t<item>1.5625e+14</item>
\t\t<item>1.5625e+14</item>
\t\t<item>1.5625e+14</item>
\t\t<item>1.5625e+14</item>
\t\t<item>1.5625e+14</item>
\t\t<item>1.5625e+14</item>
\t</unresv_bw>
\t<admin_group>0</admin_group>
'''

header_3 = \
    '''\t<prot_type>0</prot_type>
\t<srlg>
\t\t<count>1</count>
\t\t<item_version>0</item_version>
\t\t<item>0</item>
\t</srlg>
\t<delay>0</delay>
\t<local_domainid>0</local_domainid>
\t<remote_domainid>0</remote_domainid>
\t<iscd>
\t\t<count>1</count>
\t\t<item_version>0</item_version>
\t\t<item>
'''

header_4 = \
    '''\t\t\t<max_lsp_bw>
\t\t\t\t<count>8</count>
\t\t\t\t<item_version>0</item_version>
\t\t\t\t<item>1.5625e+09</item>
\t\t\t\t<item>1.5625e+09</item>
\t\t\t\t<item>1.5625e+09</item>
\t\t\t\t<item>1.5625e+09</item>
\t\t\t\t<item>1.5625e+09</item>
\t\t\t\t<item>1.5625e+09</item>
\t\t\t\t<item>1.5625e+09</item>
\t\t\t\t<item>1.5625e+09</item>
\t\t\t</max_lsp_bw>
\t\t</item>
\t</iscd>
\t<iacd>
\t\t<count>0</count>
\t\t<item_version>0</item_version>
\t</iacd>
\t<plr>0</plr>\n'''

header_5 = \
    '''\t<osnr_db>41.161057</osnr_db>
\t<osnr_local>42</osnr_local>
\t<osnr_remote>38.549999</osnr_remote>
'''


def create(topology):
    xml = '<?xml version="1.0" encoding="UTF-8" standalone="yes" ?>\n'
    xml += \
        '''<!DOCTYPE boost_serialization>
<boost_serialization signature="serialization::archive" version="10">
'''
    xml += '<g>\n'
    if hasattr(topology, 'nodes'):
        xml += '<V>' + str(len(topology.nodes)) + '</V>\n'
    else:
        xml += '<V>' + str(0) + '</V>\n'

    if hasattr(topology, 'nodes'):
        xml += '<E>' + str(len(topology.edges)) + '</E>\n'
    else:
        xml += '<E>' + str(0) + '</E>\n'

    for node in topology.nodes:
        xml += '<node>\n'
        if is_valid_ipv4_address(topology.nodes[node].nodeId):
            xml += '\t<name>' + topology.nodes[node].nodeId \
                   + '</name>\n'
            xml += '\t<id>' + topology.nodes[node].nodeId + '</id>\n'
        else:
            xml += '\t<name>' \
                   + change_datapathId(topology.nodes[node].nodeId) \
                   + '</name>\n'
            xml += '\t<id>' \
                   + change_datapathId(topology.nodes[node].nodeId) \
                   + '</id>\n'

        xml += \
            '''\t<regen_pools>
\t\t<count>0</count>
\t\t<item_version>0</item_version>
\t</regen_pools>
\t<osnr_db>0</osnr_db>
\t<osnr>
\t\t<count>0</count>
\t\t<item_version>0</item_version>
\t</osnr>
'''
        xml += '</node>\n'
    edge_cnt = 0
    for edge in topology.edges:
        if topology.edges[edge].switchingCap == 'sdm':
            ### Getting core and modes from source port
            #### print (topology.nodes[topology.edges[edge].source].edgeEnd[topology.edges[edge].localIfid])
            node_src = topology.nodes[topology.edges[edge].source].edgeEnd[topology.edges[edge].localIfid]
            for core in node_src.availableCore:
                xml += get_edge_xml(topology.edges[edge], core, 'AA')
                edge_cnt += 1
        else:
            xml += get_edge_xml(topology.edges[edge])
            edge_cnt += 1
    xml += '</g>\n</boost_serialization>'

    # TODO Modify edge count
    if edge_cnt != len(topology.edges):
        xml = xml.replace('<E>' + str(len(topology.edges)) + '</E>\n', '<E>' + str(edge_cnt) + '</E>\n')

    return xml


def get_edge_xml(edge, coreId='', modeId=''):
    xml = ''
    xml += '<link>\n'
    if is_valid_ipv4_address(edge.source):
        xml += '\t<source>' + edge.source \
               + '</source>\n'
    else:
        xml += '\t<source>' \
               + change_datapathId(edge.source) \
               + '</source>\n'
    xml += '\t<type>1</type>\n'
    if is_valid_ipv4_address(edge.target):
        xml += '\t<target>' + edge.target \
               + '</target>\n'
    else:
        xml += '\t<target>' \
               + change_datapathId(edge.target) \
               + '</target>\n'

    xml += header_1
    xml += '\t<te_metric>' + str(edge.metric) + '</te_metric>\n'
    xml += '\t<sdm_coreid>' + coreId + '</sdm_coreid>\n'
    xml += '\t<sdm_modeid>' + modeId + '</sdm_modeid>\n'
    xml += '\t<max_bw>0</max_bw>\n'
    xml += '\t<max_resv_bw>' + str(edge.maxResvBw) + '</max_resv_bw>\n'
    xml += '\t<unresv_bw>\n'
    count = 8
    xml += '\t\t<count>' + str(count) + '</count>\n'
    xml += '\t\t<item_version>0</item_version>\n'
    for i in range(0, count):
        xml += '\t\t<item>' + str(edge.unreservBw) + '</item>\n'
    xml += '\t</unresv_bw>\n'
    xml += '\t<admin_group>0</admin_group>\n'

    xml += '\t<local_ifid>' + str(edge.localIfid) \
           + '</local_ifid>\n'
    xml += '\t<remote_ifid>' + str(edge.remoteIfid) \
           + '</remote_ifid>\n'
    xml += header_3
    xml += \
        get_switching_cap_encoding(edge.switchingCap)
    xml += header_4
    if edge.edgeType.get() == 1:
        xml += get_channels_xml(edge.channels)
    else:
        xml += get_channels_xml(channels=[])

    xml += header_5
    xml += '</link>\n'

    return xml


def get_channels_xml(channels=None):
    if channels is None:
        xml = \
            '''\t<channels>
\t\t<count>0</count>
\t\t<item_version>0</item_version>
\t</channels>
'''
    else:
        xml = '\t<channels>\n\t\t<count>' + str(len(channels)) \
              + '''</count>
\t\t<item_version>0</item_version>
'''
        for channel in channels:
            xml += '\t\t<item>\n\t\t\t<g694_id>' \
                   + str(channels[channel].g694Id) \
                   + '</g694_id>\n\t\t\t<state>' + str(channels[channel].state) \
                   + '''</state>
\t\t\t<protected_srlgs>
\t\t\t\t<count>0</count>
\t\t\t\t<item_version>0</item_version>
\t\t\t</protected_srlgs>
\t\t</item>
'''
        xml += '\t</channels>\n'
    return xml


def get_switching_cap_encoding(link_type):
    if link_type == 'psc':
        return '''\t\t\t<switching_cap>1</switching_cap>
\t\t\t<encoding>1</encoding>
'''
    elif link_type == 'lsc':
        return '''\t\t\t<switching_cap>150</switching_cap>
\t\t\t<encoding>8</encoding>
'''
    elif link_type == 'sdm':
        return '''\t\t\t<switching_cap>160</switching_cap>
\t\t\t<encoding>8</encoding>
'''
    else:
        return '''\t\t\t<switching_cap>1</switching_cap>
\t\t\t<encoding>1</encoding>
'''


def is_valid_ipv4_address(address):
    try:
        socket.inet_pton(socket.AF_INET, address)
    except AttributeError:

        # no inet_pton here, sorry

        try:
            socket.inet_aton(address)
        except socket.error:
            return False
        return address.count('.') == 3
    except socket.error:

        # not a valid address

        return False

    return True


def change_datapathId(value):
    value2 = []
    value2[:0] = str(value)
    for char in value2:
        if char == ':':
            value2[value2.index(char)] = '-'

    return ''.join(value2)
