"""
This module generate node topology XML configuration

Copyright (c) 2017-2018 Laura Rodriguez Navas <laura.rodriguez.navas@cttc.cat>
"""

from lxml import etree

from data import pretty_print


def generate(filename, id_node, number_of_ports, number_of_cores):
    config = etree.Element('config', xmlns="urn:ietf:params:xml:ns:netconf:base:1.0")
    node = etree.SubElement(config, 'node', xmlns="urn:node-topology")
    nodeid = etree.SubElement(node, 'node-id')
    nodeid.text = '%s' % id_node
    for i in range(0, number_of_ports):  # list of ports
        port = etree.SubElement(node, 'port')
        # port parameters
        portid = etree.SubElement(port, 'port-id')
        # portid.text = '%s' % i
        portid.text = '%s' % i
        layer_protocol_name = etree.SubElement(port, 'layer-protocol-name')
        layer_protocol_name.text = 'sdm'

        for j in range(0, number_of_cores):  # list of available-core
            available_core = etree.SubElement(port, 'available-core')
            # available_core parameters
            coreid = etree.SubElement(available_core, 'core-id')
            coreid.text = '%s' % j
            for i in range(0, 1):  # list of available-frequency-slot
                available_frequency_slot = etree.SubElement(available_core, 'available-frequency-slot')
                frequency_slot_parameters(available_frequency_slot, i)
            for i in range(0, 1):  # list of occupied-frequency-slot
                occupied_frequency_slot = etree.SubElement(available_core, 'occupied-frequency-slot')
                frequency_slot_parameters(occupied_frequency_slot, i)

        # available_transceiver = etree.SubElement(port, 'available-transceiver')
        # # available_transceiver parameters
        # transceiverid = etree.SubElement(available_transceiver, 'transceiver-id')
        # transceiverid.text = '%s' % i
        # transceiver_type = etree.SubElement(available_transceiver, 'transceiver-type')
        # transceiver_type.text = 'transceiver_type'
        #
        # supported_modulation_format = etree.SubElement(available_transceiver, 'supported-modulation-format')
        # # supported_modulation_format parameters
        # modulation_id = etree.SubElement(supported_modulation_format, 'modulation-id')
        # modulation_id.text = '%s' % i
        # mod_type = etree.SubElement(supported_modulation_format, 'mod-type')
        # mod_type.text = 'mod_type'
        #
        # supported_center_frequency_range = etree.SubElement(available_transceiver, 'supported-center-frequency-range')
        # # supported_modulation_format parameters
        # max_cf = etree.SubElement(supported_center_frequency_range, 'max-cf')
        # max_cf.text = 'max_cf'
        # min_cf = etree.SubElement(supported_center_frequency_range, 'min-cf')
        # min_cf.text = 'min_cf'
        #
        # supported_bandwidth = etree.SubElement(available_transceiver, 'supported-bandwidth')
        # # supported_bandwidth parameters
        # max_bw = etree.SubElement(supported_bandwidth, 'max-bw')
        # max_bw.text = 'max_bw'
        # min_bw = etree.SubElement(supported_bandwidth, 'min-bw')
        # min_bw.text = 'min_bw'
        #
        # supported_FEC = etree.SubElement(available_transceiver, 'supported-FEC')
        # supported_FEC.text = 'supported_FEC'
        # supported_equalization = etree.SubElement(available_transceiver, 'supported-equalization')
        # supported_equalization.text = 'supported_equalization'
        # supported_monitoring = etree.SubElement(available_transceiver, 'supported-monitoring')
        # supported_monitoring.text = 'supported_monitoring'

    xml = etree.tostring(config)
    pretty_xml = pretty_print(xml)
    with open(filename, "w") as f:
        f.write(pretty_xml)


def frequency_slot_parameters(available_frequency_slot, i):
    slotid = etree.SubElement(available_frequency_slot, 'slot-id')
    slotid.text = '%s' % i
    nominal_central_frequency = etree.SubElement(available_frequency_slot, 'nominal-central-frequency')
    # nominal_central_frequency parameters
    nominal_central_frequency_parameters(nominal_central_frequency)
    slot_width_number = etree.SubElement(available_frequency_slot, 'slot-width-number')
    slot_width_number.text = 'slot_width_number'


def nominal_central_frequency_parameters(nominal_central_frequency):
    grid_type = etree.SubElement(nominal_central_frequency, 'grid-type')
    grid_type.text = 'grid-type'
    adjustment_granularity = etree.SubElement(nominal_central_frequency, 'adjustment-granularity')
    adjustment_granularity.text = 'adjustment-granularity'
    channel_number = etree.SubElement(nominal_central_frequency, 'channel-number')
    channel_number.text = 'channel-number'


if __name__ == '__main__':
    nodeid = '10.1.7.84'
    numports = 8
    numcores = 2
    generate("node_topology_config.xml", nodeid, numports, numcores)
