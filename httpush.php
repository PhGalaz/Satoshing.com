<?php

$db = include('config.php');
$db = $db['db'];

$conn = new mysqli($db['host'], $db['user'], $db['password'], $db['database']);

set_time_limit(0); //Establece el número de segundos que se permite la ejecución de un script.
$i = 1;
$ar = null;
$blocks = array();

while($i <= 3)
{
$query = "SELECT * FROM block_ ORDER BY height_ DESC LIMIT $i";


$datos_query = $conn->query($query);
while($row = mysqli_fetch_array($datos_query))
{
	$ar["height"]           = $row['height_'];
	$ar["hash"] 	 		= $row['block_'];
	$ar["winner"] 		    = $row['winner_'];
	$ar["time"]				= $row['time_'];
}
$dato_json = json_encode($ar);
$blocks[] = $dato_json;
$i = $i + 1;
}
$dato_json = json_encode($blocks);
echo $dato_json;
?>
