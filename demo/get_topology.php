<?php $configs = include('config.php'); ?>
<?php 
//$nombre_fichero ='/var/www/html/abno/topology3.json'; // comment if from controller
//$gestor = fopen($nombre_fichero, 'r'); // comment if from controller
//$topology = trim(rtrim(fread($gestor, filesize($nombre_fichero)))); // comment if from controller
//$topology = substr($topology, 0, -1); // comment if from controller
//fclose($gestor); // comment if from controller
?>

<?php include 'header.php' ?>
<div id="right">
	<div id="mynetwork"></div>
	<div id="info" class="info"><pre id="eventSpan"></pre></div>
</div>
<script type="text/javascript" src="libs/jQuery-scroll/jquery.scrollbar.min.js"></script>
<script type="text/javascript">
function startNetwork(data){

	var container = document.getElementById('mynetwork');
	var options = {interaction:{zoomView:true}};
	var network = new vis.Network(container, data, options);

	network.on("click", function (params) {
		var url = "<?php print $configs['url_topology']?>";
		//params.event = "[original event]";
		httpGetAsync(url,filterInfo,params)
	});
}

jQuery(document.getElementById('info')).ready(function(){
    jQuery('.info').scrollbar();
});

function httpGetAsync(theUrl, callback, params)
{
	var xmlHttp = new XMLHttpRequest();
	xmlHttp.onreadystatechange = function() { 
	    if (xmlHttp.readyState == 4 && xmlHttp.status == 200){
			if (params != null)
	        	callback(xmlHttp.responseText, params);
			else
				callback(xmlHttp.responseText);
		}
	}
	xmlHttp.open("GET", theUrl, true); // true for asynchronous 
	xmlHttp.send();
}
function filterInfo(rawTopology, params){
	var json_data = JSON.parse(rawTopology);
	var json_nodes = json_data.nodes;
	var json_edges = json_data.edges;
	if (params.nodes != ''){
		for (j=0; j<json_nodes.length; j++){
			if (json_nodes[j].nodeId == params.nodes){
				document.getElementById('eventSpan').innerHTML ='<h2>'+json_nodes[j].nodeId+'</h2>' + JSON.stringify(json_nodes[j], null, 4);
			}
		}
	}
	else if(params.edges != ''){
		for (j=0; j<json_edges.length; j++){
			if (json_edges[j].edgeId == params.edges || json_edges[j].edgeId.substr(0, (json_edges[j].edgeId.length - 6)) == params.edges){
				document.getElementById('eventSpan').innerHTML ='<h4>'+json_edges[j].edgeId+'</h4>' + JSON.stringify(json_edges[j], null, 4);
			}
		}
	}
}


function composeDataSet(rawTopology)
{ 	
	var json_data = JSON.parse(rawTopology);
    //window.alert(json_data);
	var json_nodes = json_data.nodes;
	var json_edges = json_data.edges;
	var _nodes = new vis.DataSet();

	for (i=0; i<json_nodes.length;i++){
		var label = json_nodes[i].nodeId;
		if (json_nodes[i].nodetype=='GMPLS'){
			_nodes.add({id:json_nodes[i].nodeId, label:label, shape: 'image', image: 'images/oxc.png'});
		}
		else if (json_nodes[i].nodetype=='OF-W'){
			_nodes.add({id:json_nodes[i].nodeId, label:label, shape: 'image', image: 'images/w-switch.png'});
		}
		else if (json_nodes[i].nodetype=='ABSTRACT'){
			_nodes.add({id:json_nodes[i].nodeId, label:label, shape: 'image', image: 'images/abstract_node.png'});
		}
		else if (json_nodes[i].nodetype=='OF-IOT'){
			_nodes.add({id:json_nodes[i].nodeId, label:label, shape: 'image', image: 'images/iot.png'});
		}
		else if (json_nodes[i].nodetype=='HOST'){
			_nodes.add({id:json_nodes[i].nodeId, label:label, shape: 'image', image: 'images/computer.png'});
		}
		else{
			_nodes.add({id:json_nodes[i].nodeId, label:label, shape: 'image', image: 'images/switch.png'});
		}	
	}
  // create an array with edges
	var _edges = new vis.DataSet();
        if (json_edges){
		for (i=0; i<json_edges.length;i++){
            if (json_edges[i].edgeType=='sdm_edge'){
			    _edges.add({id:json_edges[i].edgeId,from:json_edges[i].source, to:json_edges[i].target, color:'blue'});
            }
            else {
                _edges.add({id:json_edges[i].edgeId,from:json_edges[i].source, to:json_edges[i].target, color:'red'});
            }
		}
	}
	var data = {
	  nodes: _nodes,
	  edges: _edges
	};

	startNetwork(data);
}
var url = "<?php print $configs['url_topology']?>";
//var rawTopology = <?php echo '\''.$topology.'\';' ?> // comment if from controller
//var data = composeDataSet(rawTopology); // comment if from controller
var data = httpGetAsync(url, composeDataSet);

</script>
<?php include 'footer.php' ?>

