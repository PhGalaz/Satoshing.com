<?php

$db = include('config.php');
$db = $db['db'];
$conn = new mysqli($db['host'], $db['user'], $db['password'], $db['database']);

set_time_limit(0); //Establece el número de segundos que se permite la ejecución de un script.
$id = $_POST['tx'];

$query = "SELECT * FROM txs_ WHERE txid_='$id'";
$datos_query = $conn->query($query);
while($row = mysqli_fetch_array($datos_query))
{
	$ar["block"]				= $row['block_'];
	$ar["amount"]          		= $row['amount_'];	
	$ar["type"] 	 		  	= $row['type_'];
	$ar["prize"]				= $row['price_'];
	$ar["pay_tx"] 		        = $row['pay_tx'];
	$ar["result"] 		        = $row['result'];
}

$dato_json = json_encode($ar);


echo $dato_json;
?>