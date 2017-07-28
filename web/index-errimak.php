<html>
<body>


<form action="index-errimak.php" method="post">
Aurrekoak: <input type="text" name="aur" value="a ai b d g r alb ald alg e eb ed eg er i is iz o oi op ot ok osp ost osk ozp ozt ozk t k R s z x ts tz tx st sk zt zk u" size="99"><br/>
Tartekoak: <input type="text" name="tart" value="ai e i l n m o oi r u s z ts tz tx R" size="75"><br/>
Bukaerakoak: <input type="text" name="buk" value="a ak an ean ian ez ik k ko koak n ra rat rik ta tik tzen z" size="75"><br/>
<br/>
<br/>

<textarea name="bertsoa" rows="16" cols="30" id="bertsoaIdaztekoLekua" style="font-size:24px">
<?php
if ($_POST['bertsoa']=='') {
  echo 'Batetikan korrozka
bestetik herrena
ohea okupatu du
hori da txarrena
ez da pinta kabala
honek dakarrena
kaltzontzilorik gabe
ohean barrena
pixkat gutxigo edan
ezazu hurrena';
}
else {
  echo rtrim($_POST['bertsoa']);
}
?>

</textarea>
<br/>
<br/>
<button type="submit" formmethod="post" formaction="index-errimak.php">Analizatu bertsoa!</button>
</form>

<!--<h2>Analisia:</h2>-->
<?php

function sendRequest ($input, $port) {

   $service_port = $port;

   // Get the IP address for the target host.
   $address = gethostbyname('u014733.si.ehu.es');
//   $address = gethostbyname('basajaun.si.ehu.es');



   //Create a TCP/IP socket.
   $socket = socket_create(AF_INET, SOCK_STREAM, SOL_TCP);
   /*if ($socket === false) {
     echo "socket_create() failed: reason: " . socket_strerror(socket_last_error()) . "\n";
   } else {
     echo "OK.\n";
   }*/
   

   //echo "Attempting to connect to '$address' on port '$service_port'...";
   $result = socket_connect($socket, $address, $service_port);
   /*if ($result === false) {
     echo "socket_connect() failed.\nReason: ($result) " . socket_strerror(socket_last_error($socket)) . "\n";
   } else {
     echo "OK.\n";
   }*/


   $out = '';

//   echo "Sending HTTP HEAD request...\n<br/>";
//   echo "Writing ";
//   echo strlen($input);
//   echo " characters. ";
   socket_write($socket, $input, strlen($input));
//   echo "OK.\n";
   $out = socket_read($socket, 2048);
//   echo $out;
   
//   echo "Closing socket...";
   socket_close($socket);
//   echo "OK.\n\n";

   return $out;
 }

if ($_POST['bertsoa']!='') {
$bertsoaNormal=$_POST['bertsoa'];
$aur=$_POST['aur'];
$tart=$_POST['tart'];
$buk=$_POST['buk'];
$bertsoa=rtrim($bertsoa);
$bertsoa = trim(preg_replace('/\s\s+/', '|', $bertsoa));

$mezua="";
$mezua=$mezua."<mezua>";
$mezua=$mezua."<bertsoa>";
$mezua=$mezua.$bertsoa;
$mezua=$mezua."</bertsoa>";
$mezua=$mezua."<aur>";
$mezua=$mezua.$aur;
$mezua=$mezua."</aur>";
$mezua=$mezua."<tart>";
$mezua=$mezua.$tart;
$mezua=$mezua."</tart>";
$mezua=$mezua."<buk>";
$mezua=$mezua.$buk;
$mezua=$mezua."</buk>";
$mezua=$mezua."</mezua>";


$nafDok=sendRequest($mezua, 5005);
//  echo $pos;
//$nafDok=sendRequest("kaka\n", 5005);


 echo "<h2>".$nafDok."</h2>";

  //http://php.net/manual/en/sockets.examples.php

}

  

?>

</body>
</html>
