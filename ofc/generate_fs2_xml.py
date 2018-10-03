"""
This module generate XML configuration for step 3

Copyright (c) 2018 Laura Rodriguez Navas <laura.rodriguez.navas@cttc.cat>
"""
import xml.dom.minidom as md

from lxml import etree

INDENT = ' ' * 4

modes = ["LP01", "LP11a", "LP11b", "LP21a", "LP21b", "LP02"]
channels = ["39", "41"]


def pretty_print(s):
    return '\n'.join(line for line in md.parseString(s).toprettyxml(indent=INDENT).split('\n') if line.strip())


def generate(filename, bw, qam, mm, taps, num_modes):
    config = etree.Element('config', xmlns="urn:ietf:params:xml:ns:netconf:base:1.0")
    transceiver = etree.SubElement(config, 'transceiver-connectivity',
                                   xmlns="urn:sliceable-transceiver-sdm-connectivity")
    slice = etree.SubElement(transceiver, 'slice')
    sliceid = etree.SubElement(slice, 'sliceid')
    sliceid.text = '1'
    counter = 1
    for j in range(0, len(channels)):
        for i in range(1, num_modes + 1):
            optical_channel = etree.SubElement(slice, 'optical-channel')
            opticalchannelid = etree.SubElement(optical_channel, 'opticalchannelid')
            opticalchannelid.text = '%s' % counter
            coreid = etree.SubElement(optical_channel, 'coreid')
            coreid.text = 'Core19'
            modeid = etree.SubElement(optical_channel, 'modeid')
            modeid.text = '%s' % modes[i - 1]

            frequency_slot = etree.SubElement(optical_channel, 'frequency-slot')
            ncf = etree.SubElement(frequency_slot, 'ncf')
            ncf.text = '%s' % channels[j]
            slot_width = etree.SubElement(frequency_slot, 'slot-width')
            slot_width.text = '1'
            frequency_slot.append(slot_width)
            counter += 1

    for i in range(1, len(channels) * num_modes + 1):
        optical_signal = etree.SubElement(slice, 'optical-signal')
        opticalchannelid = etree.SubElement(optical_signal, 'opticalchannelid')
        opticalchannelid.text = '%s' % i
        constellation = etree.SubElement(optical_signal, 'constellation')
        constellation.text = '%s' % qam
        bandwidth = etree.SubElement(optical_signal, 'bandwidth')
        bandwidth.text = '%s' % bw
        fec = etree.SubElement(optical_signal, 'fec')
        fec.text = 'sd-fec'

        equalization = etree.SubElement(optical_signal, 'equalization')
        equalizationid = etree.SubElement(equalization, 'equalizationid')
        if mm == "LMS 6x6" and taps == 200:
            equalizationid.text = '1'
        elif mm == "LMS 12x12" and taps == 500:
            equalizationid.text = '2'
        mimo = etree.SubElement(equalization, 'mimo')
        mimo.text = '%s' % mm
        num_taps = etree.SubElement(equalization, 'num_taps')
        num_taps.text = '%s' % taps

        monitor = etree.SubElement(optical_signal, 'monitor')
        osnr = etree.SubElement(monitor, 'osnr')
        osnr.text = '29.875'
        ber = etree.SubElement(monitor, 'ber')
        ber.text = '0.0'

    xml = etree.tostring(config)
    pretty_xml = pretty_print(xml)
    with open(filename, "w") as f:
        f.write(pretty_xml)


if __name__ == '__main__':
    generate("edit_3.xml", 12000000000, "qam16", "LMS 12x12", 201, 6)
