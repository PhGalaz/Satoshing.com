<?php
$db = include('config.php');
$db = $db['db'];
$conn = new mysqli($db['host'], $db['user'], $db['password'], $db['database']);


set_time_limit(0); //Establece el número de segundos que se permite la ejecución de un script.
$lastblock = $_POST['height'];
$total = $_POST['total'];

while(true == true) {	
	$query3    = "SELECT * FROM block_ ORDER BY height_ DESC LIMIT 1";
	$con 	   = $conn->query($query3);
	$ro        = mysqli_fetch_array($con);
	

	usleep(1000000);//1sec
	clearstatcache();
	$newblock  = $ro['height_'];

	if ($newblock != $lastblock) {
		$query       = "SELECT * FROM block_ ORDER BY height_ DESC LIMIT 1";
		$datos_query = $conn->query($query);
		while($row = mysqli_fetch_array($datos_query))
		{
			$ar["modo"]					= 0;
			$ar["height"]          		= $row['height_'];	
			$ar["hash"] 	 		  	= $row['block_'];	
			$ar["winner"] 		        = $row['winner_'];	
			$ar["time"]					= $row['time_'];
		}

		$dato_json = json_encode($ar);

		$previous = $ar['height'] - 1;
		$query = "SELECT * FROM block_ WHERE height_='$previous'";
		$datos_query = $conn->query($query);
		$row = mysqli_fetch_object($datos_query);
		$previous_time = $row->time_;
		$ar["previous_time"]			= $previous_time;

		$dato_json = json_encode($ar);

		echo $dato_json;
		break;
	}

	$query = "SELECT * FROM txs_ ORDER BY id DESC LIMIT 1";
	$datos_query = $conn->query($query);
	$row = mysqli_fetch_object($datos_query);
	$id = $row->id;

	if ($id != $total) {
		$index = $total + 1;
		$query       = "SELECT * FROM txs_ WHERE id='$index'";
		$datos_query = $conn->query($query);
		while($row = mysqli_fetch_array($datos_query))
		{
			$ar["modo"]					= 1;
			$ar["id"]          			= $row['id'];
			$ar["txid"]					= $row['txid_'];
			$ar["wagered"] 	 		  	= $row['totalwagered'];	
			$ar["result"] 	 		  	= $row['result'];	
		}
		$dato_json = json_encode($ar);
		echo $dato_json;
		break;
	}
}

?>