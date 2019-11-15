<html>
<head>
	<meta name="viewport" content="width=device-width, initial-scale=1">
</head>
<body>
	
<?php
$connection= new mysqli("localhost","Spidy_niks","webtech@123","signup");
$sql="select * from bs2";
$result=$connection->query($sql);
if($result->num_rows>0)
{
	echo "<table class='table'>";
	while($row=$result->fetch_assoc())
	{
		echo "<tr>"."<td>" .$row["c_code"] ."</td>"."<td><button>></button></td>"."<td>" . $row["airline"] ."</td>". "<td>". $row["automobile"] ."</td>". "<td>". $row["hyper_market"] ."</td>"."<td>". $row["search_service"] ."</td>"."<td>". $row["steel_producer"] ."</td>"."<td>". $row["quick_resturant"] ."</td>"."<td>". $row["software_service"] ."</td>"."<td>". $row["cement"] ."</td>"."<td>". $row["healthcare"] ."</td>"."<td>". $row["real_estate"] ."</td>"."<td>". $row["retail_jewelry"] ."</td>"."<td>". $row["hotel_chain"] ."</td>"."<td>". $row["financial_service"] ."</td>"."<td>". $row["agricultural_product"] ."</td>". "</tr>";	
	}
	echo "</table>";
}
else
{
	echo "0 results";
}
$connection->close();
?>
</body>