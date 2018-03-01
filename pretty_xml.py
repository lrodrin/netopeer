"""
This module build a pretty print for XML configurations

Copyright (c) 2017-2018 Laura Rodriguez Navas <laura.rodriguez.navas@cttc.cat>
"""
import xml.dom.minidom as md

INDENT = ' ' * 4


def pretty_print_from_file(fh):
    print('\n'.join(line for line in md.parse(fh).toprettyxml(indent=INDENT).split('\n') if line.strip()))


def pretty_print_from_string(fh):
    print('\n'.join(line for line in md.parseString(fh).toprettyxml(indent=INDENT).split('\n') if line.strip()))


if __name__ == '__main__':
    with open("sdm_node_config.xml", 'rb') as f:
        pretty_print_from_file(f)

    data = '''
    <sdm-wdm>
        <wdm-id>01</wdm-id>
        <port>
            <port-id>3000</port-id>
            <signal>
                <signal-id>3001</signal-id>
                <wavelength>3</wavelength>
                <mode>03</mode>
                <core>3</core>
            </signal>
        </port>
    </sdm-wdm>
    '''

    pretty_print_from_string(data)
