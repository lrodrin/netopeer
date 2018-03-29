"""
This module generate XML configuration

Copyright (c) 2017-2018 Laura Rodriguez Navas <laura.rodriguez.navas@cttc.cat>
"""

from lxml import etree

from kddi.data import pretty_print

INDENT = ' ' * 4

modes = ["LP01", "LP11a", "LP11b", "LP21a", "LP21b", "LP02"]
cores = ["Core19", "Core18", "Core17", "Core16", "Core15",
         "Core14", "Core13", "Core12", "Core11", "Core10",
         "Core9", "Core8", "Core7", "Core6", "Core5",
         "Core4", "Core3", "Core2", "Core1"]


def generate(filename, id_slice, conste, fs, bw):
    config = etree.Element('config', xmlns="urn:ietf:params:xml:ns:netconf:base:1.0")
    transceiver = etree.SubElement(config, 'transceiver', xmlns="urn:sliceable-transceiver-sdm")
    slice = etree.SubElement(transceiver, 'slice')
    sliceid = etree.SubElement(slice, 'sliceid')
    sliceid.text = '%s' % id_slice
    counter = 1
    for c in range(0, len(cores)):
        for m in range(0, len(modes)):
            optical_channel = etree.SubElement(slice, 'optical-channel')
            # optical_channels parameters
            opticalchannelid = etree.SubElement(optical_channel, 'opticalchannelid')
            opticalchannelid.text = '%s' % counter
            coreid = etree.SubElement(optical_channel, 'coreid')
            coreid.text = '%s' % cores[c]
            modeid = etree.SubElement(optical_channel, 'modeid')
            modeid.text = '%s' % modes[m]

            frequency_slot = etree.SubElement(optical_channel, 'frequency-slot')
            # frequency_slot parameters
            ncf = etree.SubElement(frequency_slot, 'ncf')
            ncf.text = '41'
            slot_width = etree.SubElement(frequency_slot, 'slot-width')
            slot_width.text = '%s' % fs
            frequency_slot.append(slot_width)
            counter += 1

    for i in range(1, len(cores) * len(modes) + 1):
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
        equalizationid.text = '1'
        mimo = etree.SubElement(equalization, 'mimo')
        mimo.text = 'true'
        num_taps = etree.SubElement(equalization, 'num_taps')
        num_taps.text = '200'

        monitor = etree.SubElement(optical_signal, 'monitor')
        # monitor parameters
        ber = etree.SubElement(monitor, 'ber')
        ber.text = 'ber'
        channel_power = etree.SubElement(monitor, 'channel-power')
        channel_power.text = 'channel-power'
        noise_level = etree.SubElement(monitor, 'noise-level')
        noise_level.text = 'noise-level'
        osnr = etree.SubElement(monitor, 'osnr')
        osnr.text = 'osnr'


    xml = etree.tostring(config)
    pretty_xml = pretty_print(xml)
    with open(filename, "w") as f:
        f.write(pretty_xml)


if __name__ == '__main__':
    generate("test1_edit_config.xml", 1, 'qam16', 1, '12000000000')

    # generate("test5_edit_config.xml", 1, 'qam16', 1, '12000000000')
