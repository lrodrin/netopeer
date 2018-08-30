<?php

return array(
    'title' => 'BlueSpace SDN/NFV Orchestrator',
    //'utils' => array ( 'Child ABNO' => 'http://10.1.1.81/abno-2.0') ,
    'utils' => array ( 'AS-PCE' => 'http://10.0.2.15:4188/' ) ,
    'image_src' => 'images/adrenaline_transp.png',
    'server' => '10.0.2.15',
    'index_options' => array ( 'CALLS' => '', 'CONNECTIONS' => '', 'STATUS' => '', 'UTILS' => '' ),
    //'index_options' => array ( 'FLOWS' => '', 'VIRTUAL_MACHINES' => '', 'NETWORKS' => '', 'FULLMESH' => '', 'STATUS' => '', 'UTILS' => '' ),    
    'url_topology' => 'http://10.0.2.15:9881/restconf/config/context/topology/0',
    // 'url_topology' => 'http://10.1.7.33:8880/get_topology',
);


