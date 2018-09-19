"""
This module implements the steps

Copyright (c) 2018 Laura Rodriguez Navas <laura.rodriguez.navas@cttc.cat>
"""
from ncclient import manager


def connect(host):
    try:
        connection = manager.connect(host=host, port=830, username='root', password='netlabN.', hostkey_verify=False,
                                     device_params={'name': 'default'}, allow_agent=False, look_for_keys=False)
        return connection

    except Exception as e:
        print(e)


def edit(connection, config_file, session, operation):
    try:
        f = open(config_file)
        connection.edit_config(target=session, config=f.read(), default_operation=operation)
        f.close()

    except Exception as e:
        print(e)


def close(connection):
    connection.close_session()


def delete_4(connection, session):
    try:
        template = """<config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
            <transceiver-connectivity xmlns="urn:sliceable-transceiver-sdm-connectivity">
                <slice>
                    <sliceid>1</sliceid>
                        <optical-channel><opticalchannelid>4</opticalchannelid></optical-channel>
                        <optical-channel><opticalchannelid>5</opticalchannelid></optical-channel>
                        <optical-channel><opticalchannelid>6</opticalchannelid></optical-channel>
                        <optical-channel><opticalchannelid>10</opticalchannelid></optical-channel>
                        <optical-channel><opticalchannelid>11</opticalchannelid></optical-channel>
                        <optical-channel><opticalchannelid>12</opticalchannelid></optical-channel>
                </slice>
            </transceiver-connectivity>
        </config>"""
        connection.edit_config(target=session, config=template, default_operation='replace')

    except Exception as e:
        print(e)


# def delete_5(connection, session):
#     try:
#         template = """<config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
#             <transceiver-connectivity xmlns="urn:sliceable-transceiver-sdm-connectivity">
#                 <slice>
#                     <sliceid>1</sliceid>
#                         <optical-channel><opticalchannelid>1</opticalchannelid></optical-channel>
#                         <optical-channel><opticalchannelid>2</opticalchannelid></optical-channel>
#                         <optical-channel><opticalchannelid>3</opticalchannelid></optical-channel>
#                 </slice>
#             </transceiver-connectivity>
#         </config>"""
#         connection.edit_config(target=session, config=template, default_operation='replace')
#
#     except Exception as e:
#         print(e)


if __name__ == '__main__':
    hostRX = '10.1.7.66'
    config_files = ["edit_1.xml", "edit_2.xml", "edit_3.xml", "edit_4.xml", "edit_5.xml"]
    connectionRX = connect(hostRX)
    # STEP 1
    edit(connectionRX, config_files[0], 'running', 'merge')
    # STEP 2
    edit(connectionRX, config_files[1], 'running', 'merge')
    # STEP 3
    edit(connectionRX, config_files[2], 'running', 'merge')
    # STEP 4
    # delete_4(connectionRX, 'running')
    edit(connectionRX, config_files[3], 'running', 'replace')
    # STEP 5
    # delete_5(connectionRX, 'running')
    edit(connectionRX, config_files[4], 'running', 'replace')
    close(connectionRX)
