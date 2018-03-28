"""
This module generate XML configuration

Copyright (c) 2017-2018 Laura Rodriguez Navas <laura.rodriguez.navas@cttc.cat>
"""
import xml.dom.minidom as md

from lxml import etree

from data import pretty_print

INDENT = ' ' * 4

modes = ["LP01", "LP11a", "LP11b", "LP21a", "LP21b", "LP02"]
cores = ["Core19", "Core18", "Core17", "Core16", "Core15",
         "Core14", "Core13", "Core12", "Core11", "Core10",
         "Core9", "Core8", "Core7", "Core6", "Core5",
         "Core4", "Core3", "Core2", "Core1"]


def pretty_print_from_string(fh):
    return '\n'.join(line for line in md.parseString(fh).toprettyxml(indent=INDENT).split('\n') if line.strip())


def generate(filename, id_slice):
    config = etree.Element('config', xmlns="urn:ietf:params:xml:ns:netconf:base:1.0")
    transceiver = etree.Element('transceiver', xmlns="urn:sliceable-transceiver-sdm")
    slice = etree.Element('slice')
    sliceid = etree.Element('sliceid')
    sliceid.text = '%s' % id_slice
    slice.append(sliceid)
    counter = 1
    for c in range(0, len(cores)):
        for m in range(0, len(modes)):
            optical_channel = etree.Element('optical-channel')
            # optical_channels parameters
            opticalchannelid = etree.Element('opticalchannelid')
            opticalchannelid.text = '%s' % counter
            optical_channel.append(opticalchannelid)
            coreid = etree.Element('coreid')
            coreid.text = '%s' % cores[c]
            optical_channel.append(coreid)
            modeid = etree.Element('modeid')
            modeid.text = '%s' % modes[m]
            optical_channel.append(modeid)

            frequency_slot = etree.Element('frequency-slot')
            # frequency_slot parameters
            ncf = etree.Element('ncf')
            ncf.text = '39'
            frequency_slot.append(ncf)
            slot_width = etree.Element('slot-width')
            slot_width.text = '1'
            frequency_slot.append(slot_width)
            optical_channel.append(frequency_slot)

            counter += 1
            slice.append(optical_channel)

    for i in range(1, len(cores) * len(modes) + 1):
        optical_signal = etree.Element('optical-signal')
        # optical_signal parameters
        opticalchannelid = etree.Element('opticalchannelid')
        opticalchannelid.text = '%s' % i
        optical_signal.append(opticalchannelid)
        constellation = etree.Element('constellation')
        constellation.text = 'qam16'
        optical_signal.append(constellation)
        bandwidth = etree.Element('bandwidth')
        bandwidth.text = '12000000000'
        optical_signal.append(bandwidth)
        fec = etree.Element('fec')
        fec.text = 'sd-fec'
        optical_signal.append(fec)

        equalization = etree.Element('equalization')
        # equalization parameters
        equalizationid = etree.Element('equalizationid')
        equalizationid.text = '1'
        equalization.append(equalizationid)
        mimo = etree.Element('mimo')
        mimo.text = 'true'
        equalization.append(mimo)
        num_taps = etree.Element('num_taps')
        num_taps.text = '500'
        equalization.append(num_taps)
        optical_signal.append(equalization)

        slice.append(optical_signal)
    transceiver.append(slice)
    config.append(transceiver)
    # pretty string
    xml = etree.tostring(config)
    pretty_xml = pretty_print(xml)
    with open(filename, "w") as f:
        f.write(pretty_xml)


if __name__ == '__main__':
    generate("slice1_add.xml", 1)
