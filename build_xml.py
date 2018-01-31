"""
This module build a XML file

Copyright (c) 2017-2018 Laura Rodriguez Navas <laura.rodriguez.navas@cttc.cat>
"""
import xml.etree.cElementTree as ET
from xml.dom import minidom

import data as d


def prettify(elem):
    rough_string = ET.tostring(elem, 'utf-8')
    parsed = minidom.parseString(rough_string)
    return parsed.toprettyxml(indent="  ")


if __name__ == '__main__':
    host = '10.1.7.81'
    port = 830
    connection = d.connect(host, port, 'root', 'netlabN.')  # connection to NETCONF server

    module_name = "sdm-node"

    top = ET.Element('config')
    model = ET.SubElement(top, module_name)

    ET.SubElement(model, "node_id").text = "a"
    ET.SubElement(model, "node_id").text = "b"
    ET.SubElement(model, "node_id").text = "c"

    tree = ET.ElementTree(top)
    tree.write("test.xml")
