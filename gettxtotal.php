<?php

$db = include('config.php');
$db = $db['db'];
$conn = new mysqli($db['host'], $db['user'], $db['password'], $db['database']);

set_time_limit(0); //Establece el número de segundos que se permite la ejecución de un script.






$query = "SELECT * FROM txs_ ORDER BY id DESC LIMIT 1";
$datos_query = $conn->query($query);
$row = mysqli_fetch_object($datos_query);
$ar["total"]           = $row->id;



$query = "SELECT totalwagered FROM txs_ ORDER BY id DESC LIMIT 1";
$datos_query = $conn->query($query);
$row = mysqli_fetch_object($datos_query);
$ar["wagered"]           = $row->totalwagered;


$dato_json = json_encode($ar);

echo $dato_json;
?>