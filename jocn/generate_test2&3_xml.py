"""
This module generate XML configuration for test2 and test3

Copyright (c) 2018 Laura Rodriguez Navas <laura.rodriguez.navas@cttc.cat>
"""

from lxml import etree

from kddi.data import pretty_print

INDENT = ' ' * 4

modes = ["LP01", "LP11a", "LP11b", "LP21a", "LP21b", "LP02"]
cores = ["Core19", "Core18", "Core17", "Core16", "Core15",
         "Core14", "Core13", "Core12", "Core11", "Core10",
         "Core9", "Core8", "Core7", "Core6", "Core5",
         "Core4", "Core3", "Core2", "Core1"]

channels_test2 = ["55", "53", "51", "49", "47", "45", "43", "41"]
channels_test3 = ["37", "35", "33", "31", "29", "27", "25"]


def generate(filename, id_slice, conste, fs, bw, channels):
    config = etree.Element('config', xmlns="urn:ietf:params:xml:ns:netconf:base:1.0")
    transceiver = etree.SubElement(config, 'transceiver-connectivity',
                                   xmlns="urn:sliceable-transceiver-sdm-connectivity")
    slice = etree.SubElement(transceiver, 'slice')
    sliceid = etree.SubElement(slice, 'sliceid')
    sliceid.text = '%s' % id_slice
    counter = 1
    for k in range(0, len(cores)):
        for i in range(0, len(modes)):
            for j in range(0, len(channels)):
                optical_channel = etree.SubElement(slice, 'optical-channel')
                # optical_channels parameters
                opticalchannelid = etree.SubElement(optical_channel, 'opticalchannelid')
                opticalchannelid.text = '%s' % counter
                coreid = etree.SubElement(optical_channel, 'coreid')
                coreid.text = '%s' % cores[k]
                modeid = etree.SubElement(optical_channel, 'modeid')
                modeid.text = '%s' % modes[i]

                frequency_slot = etree.SubElement(optical_channel, 'frequency-slot')
                # frequency_slot parameters
                ncf = etree.SubElement(frequency_slot, 'ncf')
                ncf.text = '%s' % channels[j]
                slot_width = etree.SubElement(frequency_slot, 'slot-width')
                slot_width.text = '%s' % fs
                frequency_slot.append(slot_width)
                counter += 1

    for i in range(1, len(channels) * len(modes) * len(cores) + 1):
        optical_signal = etree.SubElement(slice, 'optical-signal')
        # optical_signal parameters
        opticalchannelid = etree.SubElement(optical_signal, 'opticalchannelid')
        opticalchannelid.text = '%s' % i
        constellation = etree.SubElement(optical_signal, 'constellation')
        constellation.text = '%s' % conste
        bandwidth = etree.SubElement(optical_signal, 'bandwidth')
        bandwidth.text = '%s' % bw
        fec = etree.SubElement(optical_signal, 'fec')
        fec.text = 'sd-fec'

        equalization = etree.SubElement(optical_signal, 'equalization')
        # equalization parameters
        equalizationid = etree.SubElement(equalization, 'equalizationid')
        equalizationid.text = '%s' % i
        mimo = etree.SubElement(equalization, 'mimo')
        mimo.text = 'true'
        num_taps = etree.SubElement(equalization, 'num_taps')
        num_taps.text = '500'

    xml = etree.tostring(config)
    pretty_xml = pretty_print(xml)
    with open(filename, "w") as f:
        f.write(pretty_xml)


if __name__ == '__main__':
    # sliceid_test2 = 2
    # sliceid_test3 = 3
    qam = 'qam64'
    m = 2
    bw = '12000000000'
    generate("test2.xml", 1, qam, m, bw, channels_test2)
    generate("test3.xml", 1, qam, m, bw, channels_test3)
