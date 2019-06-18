<?php
	require_once('easybitcoin.php');
	$node = include('config.php');
	$node = $node['node'];
	set_time_limit(0); //Establece el número de segundos que se permite la ejecución de un script.
	$mode = $_POST['name'];
	$bitcoin = new Bitcoin($node['user'], $node['password'], $node['host'], $node['port']);
	$address = $bitcoin->getnewaddress($mode);
	echo $address;
?>